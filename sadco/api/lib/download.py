from fastapi.responses import StreamingResponse
from io import StringIO, BytesIO
import pandas as pd
import zipfile


def get_zipped_csv_response(items, survey_id, data_variant) -> StreamingResponse:
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

    with zipfile.ZipFile(zip_buffer, mode="w") as zip_archive:
        stream.seek(0)
        zip_archive.writestr(f"survey_{survey_id}.csv", stream.read())

    response = StreamingResponse(iter([zip_buffer.getvalue()]), media_type="application/zip")
    response.headers["Content-Disposition"] = f"attachment; filename=survey_{survey_id}_{data_variant}.zip"

    return response
