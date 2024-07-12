from datetime import timedelta

import pytest

from sadco.const import SADCOScope
from test.api import assert_forbidden


@pytest.mark.require_scope(SADCOScope.SURVEYS_READ)
def test_fetch_surveys(api, inventories, scopes):
    authorized = SADCOScope.SURVEYS_READ in scopes

    route = '/survey/surveys'

    r = api(scopes).get(route)

    if not authorized:
        assert_forbidden(r)
    else:
        assert_surveys_result(r, inventories)


def assert_surveys_result(response, inventories):
    assert response.status_code == 200

    json = response.json()

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
                        created_inventory.scientist_1.f_name.strip() + ' ' +
                        created_inventory.scientist_1.surname.strip()).strip()

            if check_empty_institute:
                assert item['institute'] == ''


@pytest.mark.require_scope(SADCOScope.SURVEYS_READ)
def test_search_bounds(api, inventory, scopes):
    authorized = SADCOScope.SURVEYS_READ in scopes

    route = '/survey/surveys/search'

    r = api(scopes).get(
        route,
        params={
            'north_bound': (-inventory.lat_south) + 1,
            'south_bound': (-inventory.lat_north) - 1,
            'west_bound': inventory.long_east - 1,
            'east_bound': inventory.long_west + 1,
        }
    )

    if not authorized:
        assert_forbidden(r)
    else:
        assert_search_bounds_result(r, inventory)


@pytest.mark.require_scope(SADCOScope.SURVEYS_READ)
def test_search_exclusive_bounds(api, inventory, scopes):
    authorized = SADCOScope.SURVEYS_READ in scopes

    route = '/survey/surveys/search'

    r = api(scopes).get(
        route,
        params={
            'north_bound': (-inventory.lat_north) + 1,
            'south_bound': (-inventory.lat_south) - 1,
            'west_bound': inventory.long_west - 1,
            'east_bound': inventory.long_east + 1,
            'exclusive_region': True
        }
    )

    if not authorized:
        assert_forbidden(r)
    else:
        assert_search_bounds_result(r, inventory)


def assert_search_bounds_result(response, inventory):
    json = response.json()

    assert response.status_code == 200

    assert len(json['items']) == 1

    assert json['items'][0]['id'] == inventory.survey_id


@pytest.mark.require_scope(SADCOScope.SURVEYS_READ)
def test_search_interval(api, inventory, scopes):
    authorized = SADCOScope.SURVEYS_READ in scopes

    route = '/survey/surveys/search'

    start_date = (inventory.date_end - timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = (inventory.date_start + timedelta(days=1)).strftime("%Y-%m-%d")

    r = api(scopes).get(
        route,
        params={
            'start_date': start_date,
            'end_date': end_date
        }
    )

    if not authorized:
        assert_forbidden(r)
    else:
        assert_search_interval_result(r, inventory)


@pytest.mark.require_scope(SADCOScope.SURVEYS_READ)
def test_search_exclusive_interval(api, inventory, scopes):
    authorized = SADCOScope.SURVEYS_READ in scopes

    route = '/survey/surveys/search'

    start_date = (inventory.date_start - timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = (inventory.date_end + timedelta(days=1)).strftime("%Y-%m-%d")

    r = api(scopes).get(
        route,
        params={
            'start_date': start_date,
            'end_date': end_date,
            'exclusive_interval': True
        }
    )

    if not authorized:
        assert_forbidden(r)
    else:
        assert_search_interval_result(r, inventory)


def assert_search_interval_result(response, inventory):
    json = response.json()

    assert response.status_code == 200

    assert len(json['items']) == 1

    assert json['items'][0]['id'] == inventory.survey_id


@pytest.mark.require_scope(SADCOScope.SURVEYS_READ)
def test_search_sampling_device(api, survey, scopes):
    authorized = SADCOScope.SURVEYS_READ in scopes

    sampling_device_code = survey.stations[0].sedphy_list[0].device_code

    route = '/survey/surveys/search'

    r = api(scopes).get(
        route,
        params={
            'sampling_device_code': sampling_device_code
        }
    )

    if not authorized:
        assert_forbidden(r)
    else:
        assert r.status_code == 200

        assert len(r.json()['items']) > 0


@pytest.mark.require_scope(SADCOScope.SURVEYS_READ)
def test_search_survey_type(api, inventory, scopes):
    authorized = SADCOScope.SURVEYS_READ in scopes

    survey_type = inventory.survey_type

    route = '/survey/surveys/search'

    r = api(scopes).get(
        route,
        params={
            'survey_type_code': survey_type.code
        }
    )

    if not authorized:
        assert_forbidden(r)
    else:
        json = r.json()

        assert r.status_code == 200

        assert len(json['items']) > 0

        for item in json['items']:
            assert item['survey_type'] == survey_type.name

        for fetched_survey_type in json['survey_types']:
            assert fetched_survey_type['code'] == survey_type.code


@pytest.mark.require_scope(SADCOScope.HYDRO_READ)
def test_fetch_hydro_survey(api, survey, scopes):
    authorized = SADCOScope.HYDRO_READ in scopes

    route = '/survey/hydro/{}'.format(survey.survey_id)

    r = api(scopes).get(route)

    if not authorized:
        assert_forbidden(r)
    else:
        assert_fetch_hydro_survey_result(r, survey)


def assert_fetch_hydro_survey_result(response, survey):
    json = response.json()

    assert response.status_code == 200

    water_data_type = json['data_types']['water']
    sediment_data_type = json['data_types']['sediment']
    inventory_stats = survey.inventory.inv_stats

    assert (inventory_stats.watphy_cnt,
            max(inventory_stats.watchem1_cnt, inventory_stats.watchem2_cnt),
            max(inventory_stats.watpol1_cnt, inventory_stats.watpol2_cnt),
            inventory_stats.watcurrents_cnt,
            inventory_stats.watnut_cnt) == \
           (water_data_type['record_count'],
            water_data_type['water_chemistry']['record_count'],
            water_data_type['water_pollution']['record_count'],
            water_data_type['water_currents']['record_count'],
            water_data_type['water_nutrients']['record_count'])

    assert (inventory_stats.sedphy_cnt,
            max(inventory_stats.sedchem1_cnt, inventory_stats.sedchem2_cnt),
            max(inventory_stats.sedpol1_cnt, inventory_stats.sedpol2_cnt)) == \
           (sediment_data_type['record_count'],
            sediment_data_type['sediment_chemistry']['record_count'],
            sediment_data_type['sediment_pollution']['record_count'])


@pytest.mark.require_scope(SADCOScope.CURRENTS_READ)
def test_fetch_currents_survey(api, current_mooring, scopes):
    authorized = SADCOScope.CURRENTS_READ in scopes

    route = '/survey/currents/{}'.format(current_mooring.survey_id)

    r = api(scopes).get(route)

    if not authorized:
        assert_forbidden(r)
    else:
        json = r.json()

        assert r.status_code == 200

        current_depths = json['mooring_details']

        assert len(current_depths) == len(current_mooring.cur_depths)


@pytest.mark.require_scope(SADCOScope.WEATHER_READ)
def test_fetch_weather_survey(api, weather_station, scopes):
    authorized = SADCOScope.WEATHER_READ in scopes

    route = '/survey/weather/{}'.format(weather_station.survey_id)

    r = api(scopes).get(route)

    if not authorized:
        assert_forbidden(r)
    else:
        json = r.json()

        assert r.status_code == 200

        weather_period_counts = json['period_counts']

        assert len(weather_period_counts) == len(weather_station.wet_period_counts)


@pytest.mark.require_scope(SADCOScope.WAVES_READ)
def test_fetch_waves_survey(api, wave_station, scopes):
    authorized = SADCOScope.WAVES_READ in scopes

    route = '/survey/waves/{}'.format(wave_station.survey_id)

    r = api(scopes).get(route)

    if not authorized:
        assert_forbidden(r)
    else:
        json = r.json()

        assert r.status_code == 200

        wave_periods = json['period_counts']

        assert len(wave_periods) == len(wave_station.wav_periods)


@pytest.mark.require_scope(SADCOScope.UTR_READ)
def test_fetch_utr_survey(api, current_mooring, scopes):
    authorized = SADCOScope.UTR_READ in scopes

    route = '/survey/utr/{}'.format(current_mooring.survey_id)

    r = api(scopes).get(route)

    if not authorized:
        assert_forbidden(r)
    else:
        json = r.json()

        assert r.status_code == 200

        current_depths = json['mooring_details']

        assert len(current_depths) == len(current_mooring.cur_depths)


@pytest.mark.require_scope(SADCOScope.ECHO_SOUNDING_READ)
def test_fetch_echo_sounding_survey(api, echo_sounding_inventory, scopes):
    authorized = SADCOScope.ECHO_SOUNDING_READ in scopes

    route = '/survey/echo-sounding/{}'.format(echo_sounding_inventory.survey_id)

    r = api(scopes).get(route)

    if not authorized:
        assert_forbidden(r)
    else:
        json = r.json()

        assert r.status_code == 200

        assert json['project_name'] == echo_sounding_inventory.project_name
        assert json['date_start'] == echo_sounding_inventory.date_start.strftime('%Y-%m-%d')
        assert json['date_end'] == echo_sounding_inventory.date_end.strftime('%Y-%m-%d')
        assert json['survey_type'] == echo_sounding_inventory.survey_type.name


@pytest.mark.require_scope(SADCOScope.UNKNOWN_READ)
def test_fetch_unknown_survey(api, unknown_inventory, scopes):
    authorized = SADCOScope.UNKNOWN_READ in scopes

    route = '/survey/unknown/{}'.format(unknown_inventory.survey_id)

    r = api(scopes).get(route)

    if not authorized:
        assert_forbidden(r)
    else:
        json = r.json()

        assert r.status_code == 200

        assert json['project_name'] == unknown_inventory.project_name
        assert json['date_start'] == unknown_inventory.date_start.strftime('%Y-%m-%d')
        assert json['date_end'] == unknown_inventory.date_end.strftime('%Y-%m-%d')
        assert json['survey_type'] == unknown_inventory.survey_type.name
