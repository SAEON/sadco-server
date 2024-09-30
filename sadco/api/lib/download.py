from fastapi.responses import StreamingResponse
from fastapi import Request
from datetime import datetime, timezone
from io import StringIO, BytesIO
from sadco.api.lib.auth import Authorized
from sadco.db.models import DownloadAudit
import pandas as pd
import hashlib
import zipfile


def get_csv_data(items, survey_id, data_variant) -> dict:
    """
    Converts a list of dictionary items to a streaming response of a zipped folder containing a csv file
    :param items: A list of dictionaries that contain the information for each row of the csv
    :param survey_id: The id of the applicable survey for file naming purposes
    :param data_variant: The variant of the data for file naming purposes
    """
    data_frame = pd.DataFrame(items)

    stream = StringIO()

    data_frame.to_csv(stream, index=False)

    zip_buffer = BytesIO()

    file_info = get_file_stream_info(stream)

    with zipfile.ZipFile(zip_buffer, mode="w") as zip_archive:
        stream.seek(0)
        zip_archive.writestr(f"survey_{survey_id}.csv", stream.read())

    response = StreamingResponse(iter([zip_buffer.getvalue()]), media_type="application/zip")
    response.headers["Content-Disposition"] = f"attachment; filename=survey_{survey_id}_{data_variant}.zip"

    return {
        'zipped_response': response,
        'file_info': file_info
    }


def get_file_stream_info(stream: StringIO) -> dict:
    stream_value = stream.getvalue()
    return {
        'checksum': hashlib.md5(stream_value.encode()).hexdigest(),
        'size': len(stream_value),
    }


def get_table_data(fetched_model, fields_to_ignore: list = []) -> dict:
    """
    Builds and returns a dictionary of the fields from an api model and its respective db value.
    :param fetched_model: fetched db model whose values will be used.
    :param fields_to_ignore: fields from the model to be ignored.
    """
    if not fetched_model:
        return dict()

    table_data_dict = fetched_model.__dict__.copy()
    del table_data_dict['_sa_instance_state']
    for field_to_ignore in fields_to_ignore:
        del table_data_dict[field_to_ignore]

    return table_data_dict


def audit_download_request(auth: Authorized, file_info: dict, survey_type: str, **request_params):
    DownloadAudit(
        timestamp=datetime.now(timezone.utc),
        client_id=auth.client_id,
        user_id=auth.user_id,
        survey_type=survey_type,
        parameters=request_params.__str__(),
        download_file_size=file_info.get('size'),
        download_file_checksum=file_info.get('checksum')
    ).save()
