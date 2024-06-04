from datetime import date, timedelta


def test_fetch_surveys(api, inventories):
    route = '/survey/surveys'

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


def test_search_bounds(api, inventory):
    route = '/survey/surveys/search'

    r = api.get(
        route,
        params={
            'north_bound': (-inventory.lat_south)+1,
            'south_bound': (-inventory.lat_north)-1,
            'west_bound': inventory.long_east-1,
            'east_bound': inventory.long_west+1,
        }
    )

    json = r.json()

    assert r.status_code == 200

    assert len(json['items']) == 1

    assert json['items'][0]['id'] == inventory.survey_id

    r = api.get(
        route,
        params={
            'north_bound': (-inventory.lat_north) + 1,
            'south_bound': (-inventory.lat_south) - 1,
            'west_bound': inventory.long_west - 1,
            'east_bound': inventory.long_east + 1,
            'exclusive_region': True
        }
    )

    json = r.json()

    assert r.status_code == 200

    assert len(json['items']) == 1

    assert json['items'][0]['id'] == inventory.survey_id


def test_search_interval(api, inventory):
    route = '/survey/surveys/search'

    start_date = (inventory.date_end - timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = (inventory.date_start + timedelta(days=1)).strftime("%Y-%m-%d")

    r = api.get(
        route,
        params={
            'start_date': start_date,
            'end_date': end_date
        }
    )

    json = r.json()

    assert r.status_code == 200

    assert len(json['items']) == 1

    assert json['items'][0]['id'] == inventory.survey_id

    start_date = (inventory.date_start - timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = (inventory.date_end + timedelta(days=1)).strftime("%Y-%m-%d")

    r = api.get(
        route,
        params={
            'start_date': start_date,
            'end_date': end_date,
            'exclusive_interval': True
        }
    )

    json = r.json()

    assert r.status_code == 200

    assert len(json['items']) == 1

    assert json['items'][0]['id'] == inventory.survey_id


def test_search_sampling_device(api, survey):
    sampling_device_code = survey.stations[0].sedphy_list[0].device_code

    route = '/survey/surveys/search'

    r = api.get(
        route,
        params={
            'sampling_device_code': sampling_device_code
        }
    )

    json = r.json()

    assert r.status_code == 200

    assert len(json['items']) > 0


def test_search_survey_type(api, inventory):
    survey_type = inventory.survey_type

    route = '/survey/surveys/search'

    r = api.get(
        route,
        params={
            'survey_type_code': survey_type.code
        }
    )

    json = r.json()

    assert r.status_code == 200

    assert len(json['items']) > 0

    for item in json['items']:
        assert item['survey_type'] == survey_type.name

    for fetched_survey_type in json['survey_types']:
        assert fetched_survey_type['code'] == survey_type.code


def test_fetch_hydro_survey(api, survey):
    route = '/survey/hydro/{}'.format(survey.survey_id)

    r = api.get(route)
    json = r.json()

    assert r.status_code == 200

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


def test_fetch_currents_survey(api, current_mooring):
    route = '/survey/currents/{}'.format(current_mooring.survey_id)

    r = api.get(route)
    json = r.json()

    assert r.status_code == 200

    current_depths = json['mooring_details']

    assert len(current_depths) == len(current_mooring.cur_depths)



