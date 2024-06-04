import sadco.api
from random import randint, choice

from test.factories import Watchem1Factory, Watchem2Factory, Watpol1Factory, Watpol2Factory, WatcurrentsFactory, \
    WatnutFactory, WatphyFactory, StationFactory, SurveyFactory, InventoryFactory, SedphyFactory, Sedchem2Factory, \
    Sedchem1Factory, Sedpol2Factory, Sedpol1Factory, PlanamFactory, InstitutesFactory, ScientistsFactory, \
    WeatherFactory, CurrentsFactory, CurrentMooringFactory, CurrentDepthFactory, CurrentDataFactory

from starlette.testclient import TestClient
import pytest


@pytest.fixture
def api():
    api_client = TestClient(app=sadco.api.app)
    api_client.headers = {
        'Accept': 'application/json'
    }
    return api_client


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
    return InventoryFactory.create(survey=None, cur_moorings=None)


@pytest.fixture
def survey(inventory):
    survey = SurveyFactory.create(survey_id=inventory.survey_id, stations=None, inventory=inventory)
    set_station_batch(survey)
    return survey


@pytest.fixture
def current_mooring(inventory):
    current_mooring = CurrentMooringFactory.create(inventory=inventory)
    set_current_depth_batch(current_mooring)
    return current_mooring


def set_station_batch(survey):
    for _ in range(randint(2, 5)):
        station = StationFactory.create(watphy_list=None, survey=survey)
        set_watphy_batch(station)
        set_sedphy_batch(station)
        WeatherFactory(station=station)
        CurrentsFactory(station=station)


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


def set_current_depth_batch(current_mooring):
    for _ in range(randint(1, 5)):
        current_depth = CurrentDepthFactory.create(cur_mooring=current_mooring)
        set_current_data_batch(current_depth)


def set_current_data_batch(current_depth):
    for _ in range(randint(1, 10)):
        CurrentDataFactory.create(cur_depth=current_depth)


