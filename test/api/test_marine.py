from random import randint, choice

import pytest

from test.factories import Watchem1Factory, Watchem2Factory, Watpol1Factory, Watpol2Factory, WatcurrentsFactory, \
    WatnutFactory, WatphyFactory, StationFactory, SurveyFactory, InventoryFactory, SedphyFactory, Sedchem2Factory, \
    Sedchem1Factory, Sedpol2Factory, Sedpol1Factory, PlanamFactory, InstitutesFactory, ScientistsFactory


@pytest.fixture(params=[True, False])
def planam(request):
    if request.param:
        return PlanamFactory()

    return None


@pytest.fixture(params=[True, False])
def institute(request):
    if request.param:
        return InstitutesFactory()

    return None


@pytest.fixture
def inventories(planam, institute):
    return InventoryFactory.create_batch(randint(2, 5), survey=None, planam=planam, institute=institute)


@pytest.fixture
def inventory():
    return InventoryFactory.create(survey=None)


@pytest.fixture
def survey(inventory):
    survey = SurveyFactory.create(survey_id=inventory.survey_id, stations=None, inventory=inventory)
    set_station_batch(survey)
    return survey


def set_station_batch(survey):
    for _ in range(randint(2, 5)):
        station = StationFactory.create(watphy_list=None, survey=survey)
        set_watphy_batch(station)
        set_sedphy_batch(station)


def set_watphy_batch(station):
    for _ in range(randint(1, 10)):
        watphy = WatphyFactory.create(watchem1=None, watchem2=None, watpol1=None, watpol2=None, watcurrents=None,
                                      watnut=None, station=station)

        Watchem1Factory(watphy=watphy) if choice([True, False]) else None
        Watchem2Factory(watphy=watphy) if choice([True, False]) else None
        Watpol1Factory(watphy=watphy) if choice([True, False]) else None
        Watpol2Factory(watphy=watphy) if choice([True, False]) else None
        WatcurrentsFactory(watphy=watphy) if choice([True, False]) else None
        WatnutFactory(watphy=watphy) if choice([True, False]) else None


def set_sedphy_batch(station):
    for _ in range(randint(1, 10)):
        sedphy = SedphyFactory.create(sedchem1=None, sedchem2=None, sedpol1=None, sedpol2=None, station=station)

        Sedpol1Factory(sedphy=sedphy) if choice([True, False]) else None
        Sedpol2Factory(sedphy=sedphy) if choice([True, False]) else None
        Sedchem1Factory(sedphy=sedphy) if choice([True, False]) else None
        Sedchem2Factory(sedphy=sedphy) if choice([True, False]) else None


def get_data_counts(station_list: list[StationFactory]) -> dict:
    sud_data_counts: dict = {
        'watchem': 0,
        'watpol': 0,
        'watcurrents': 0,
        'watnut': 0,
        'sedchem': 0,
        'sedpol': 0
    }

    for station in station_list:
        for watphy in station.watphy_list:
            if watphy.watchem1 or watphy.watchem2:
                sud_data_counts['watchem'] += 1

            if watphy.watpol1 or watphy.watpol2:
                sud_data_counts['watpol'] += 1

            if watphy.watcurrents:
                sud_data_counts['watcurrents'] += 1

            if watphy.watnut:
                sud_data_counts['watnut'] += 1

        for sedphy in station.sedphy_list:
            if sedphy.sedchem1 or sedphy.sedchem2:
                sud_data_counts['sedchem'] += 1

            if sedphy.sedpol1 or sedphy.sedpol2:
                sud_data_counts['sedpol'] += 1

    return sud_data_counts


def test_data_type_counts(api, survey):
    route = f'/marine/surveys/{survey.survey_id}'

    r = api.get(route)
    json = r.json()

    data_counts = get_data_counts(survey.stations)

    water_data_types = json['data_types']['water']

    sediment_data_types = json['data_types']['sediment']

    assert r.status_code == 200

    assert ((water_data_types['water_chemistry']['record_count'], water_data_types['water_pollution']['record_count'],
             water_data_types['water_currents']['record_count'], water_data_types['water_nutrients']['record_count'])
            == (data_counts['watchem'], data_counts['watpol'], data_counts['watcurrents'],
                data_counts['watnut']))

    assert ((sediment_data_types['sediment_pollution']['record_count'],
             sediment_data_types['sediment_chemistry']['record_count'])
            == (data_counts['sedpol'], data_counts['sedchem']))


def test_fetch_surveys(api, inventories):
    route = '/marine/surveys'

    r = api.get(route)
    json = r.json()

    assert r.status_code == 200

    assert len(inventories) == len(json['items'])

    for created_inventory in inventories:
        check_empty_planam = False if created_inventory.planam else True
        check_empty_scientist = False if created_inventory.scientist_1 else True
        check_empty_institute = False if created_inventory.institute else True

        for item in json['items']:
            if item['id'] != created_inventory.survey_id:
                continue

            if check_empty_planam:
                assert item['platform_name'] == ''

            if check_empty_scientist:
                assert item['chief_scientist'] == ''
            else:
                assert item['chief_scientist'] == (
                        created_inventory.scientist_1.f_name.strip() + ' ' + created_inventory.scientist_1.surname.strip()).strip()

            if check_empty_institute:
                assert item['institute'] == ''
