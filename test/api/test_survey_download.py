def test_download_hydro_water_nutrient_survey(api, survey):
    route = '/survey/download/hydro/{}'.format(survey.survey_id)

    r = api.get(
        route,
        params={
            'data_type': 'watnut'
        }
    )

    assert r.status_code == 200

    assert len(r.content) > 0
