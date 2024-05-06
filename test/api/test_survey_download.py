from sadco.const import DataType


def test_download_all_data_types(api, survey):
    route = '/survey/download/hydro/{}'.format(survey.survey_id)

    for data_type in DataType:
        r = api.get(
            route,
            params={
                'data_type': data_type.value
            }
        )

        assert r.status_code == 200

        assert len(r.content) > 0

