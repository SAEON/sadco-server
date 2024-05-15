import os
import zipfile

import pytest

from sadco.const import DataType
import pandas as pd
import io

from test.factories import SurveyFactory, StationFactory, WatphyFactory, Watchem1Factory, Watchem2Factory, \
    Watpol1Factory, Watpol2Factory, WatnutFactory, InventoryFactory, WatchlFactory, CurrentsFactory, WeatherFactory, \
    SedphyFactory, Sedpol1Factory, Sedpol2Factory, Sedchem1Factory, Sedchem2Factory

TEST_SURVEY_ID: str = '1999/0001'


@pytest.fixture
def survey_download():
    inventory = InventoryFactory.create(survey_id=TEST_SURVEY_ID, survey=None)
    survey = SurveyFactory.create(
        survey_id=inventory.survey_id,
        stations=None,
        inventory=inventory,
        planam='ArcticXP'
    )
    set_download_station(survey)
    return survey


def set_download_station(survey):
    station = StationFactory.create(
        watphy_list=None,
        sedphy_list=None,
        survey=survey,
        station_id='22BG',
        latitude=30,
        longitude=72,
        date_start='1999-01-01 00:00:00',
        stnnam='UW',
        max_spldep=50
    )
    set_current_records(station)
    set_weather_records(station)
    set_watphy_records(station)
    set_sedphy_record(station)
    return survey


def set_current_records(station):
    CurrentsFactory(
        station=station,
        subdes='UCUR',
        spldattim='1999-01-02 00:00:00',
        spldep=20.2,
        current_dir=None,
        current_speed=13,
        perc_good=None,
    )

    CurrentsFactory(
        station=station,
        subdes=None,
        spldattim='1999-01-01 00:00:00',
        spldep=18.6,
        current_dir=22,
        current_speed=None,
        perc_good='WQEC',
    )


def set_weather_records(station):
    WeatherFactory(
        station=station,
        nav_equip_type='SCP',
        atmosph_pres=12.2,
        surface_tmp=16.1,
        drybulb=0.86,
        wetbulb=1.12,
        cloud='AWP',
        vis_code='MO',
        weather_code='VC',
        water_color=255,
        transparency=0.76,
        wind_dir=186,
        wind_speed=16.4,
        swell_dir=184,
        swell_height=1.13,
        swell_period=16.4,
        dupflag='N',
    )


def set_watphy_records(station):
    watphy = WatphyFactory.create(
        watchem1=None,
        watchem2=None,
        watpol1=None,
        watpol2=None,
        watcurrents=None,
        watnut=None,
        watchl=None,
        station=station,
        subdes='08',
        spldattim='1982-01-01 00:00:00',
        spldep=0.5,
        filtered='Y',
        disoxygen=1.2,
        salinity=33.4,
        temperature=12.4,
        sound_flag='U',
        soundv=6.4,
        turbidity=0.78,
        pressure=11.6,
        fluorescence=0.08
    )

    watphy_2 = WatphyFactory.create(
        watchem1=None,
        watchem2=None,
        watpol1=None,
        watpol2=None,
        watcurrents=None,
        watnut=None,
        watchl=None,
        station=station,
        subdes='34',
        spldattim='1982-01-01 00:00:00',
        spldep=0.8,
        filtered='Y',
        disoxygen=2.1,
        salinity=3.4,
        temperature=4.4,
        sound_flag='U',
        soundv=9.4,
        turbidity=0.32,
        pressure=13.6,
        fluorescence=0.18
    )

    Watchem1Factory(
        watphy=watphy,
        dic=0.4,
        doc=None,
        fluoride=44.6,
        iodene=None,
        iodate=8.7,
        kjn=None,
        nh3=9.8,
        nitrogen=None,
        oxa=7.5,
        ph=None,
    )

    Watchem1Factory(
        watphy=watphy_2,
        dic=None,
        doc=3.3,
        fluoride=None,
        iodene=3.2,
        iodate=None,
        kjn=6.67,
        nh3=None,
        nitrogen=2.14,
        oxa=None,
        ph=11,
    )

    Watchem2Factory(
        watphy=watphy,
        calcium=3.22,
        cesium=None,
        hydrocarbons=2.6,
        magnesium=None,
        pah=6,
        potassium=None,
        rubidium=2.66,
        sodium=None,
        strontium=5.54,
        so4=None,
        sussol=7,
    )

    Watchem2Factory(
        watphy=watphy_2,
        calcium=None,
        cesium=6.7,
        hydrocarbons=None,
        magnesium=9.77,
        pah=None,
        potassium=1.2,
        rubidium=None,
        sodium=8.5,
        strontium=None,
        so4=4.3,
        sussol=None,
    )

    Watpol1Factory(
        watphy=watphy,
        arsenic=None,
        cadmium=0.87,
        chromium=None,
        cobalt=0.55,
        copper=None,
        iron=78.8,
        lead=None,
        manganese=6,
        mercury=None,
        nickel=6.7,
        selenium=None,
        zinc=4.14,
    )

    Watpol1Factory(
        watphy=watphy_2,
        arsenic=0.66,
        cadmium=None,
        chromium=0.54,
        cobalt=None,
        copper=4.76,
        iron=None,
        lead=4.1,
        manganese=None,
        mercury=8.99,
        nickel=None,
        selenium=2.98,
        zinc=None,
    )

    Watpol2Factory(
        watphy=watphy,
        aluminium=3.7,
        antimony=None,
        bismuth=9.98,
        molybdenum=None,
        silver=5.21,
        titanium=None,
        vanadium=6.22,
    )

    Watpol2Factory(
        watphy=watphy_2,
        aluminium=None,
        antimony=1.8,
        bismuth=None,
        molybdenum=7.3,
        silver=None,
        titanium=9.6,
        vanadium=None,
    )

    WatnutFactory(
        watphy=watphy,
        no2=None,
        no3=8.11,
        p=None,
        po4=3.8,
        ptot=None,
        sio3=5.3,
        sio4=None,
    )

    WatnutFactory(
        watphy=watphy_2,
        no2=2.35,
        no3=None,
        p=9.7,
        po4=None,
        ptot=1.12,
        sio3=None,
        sio4=2,
    )

    WatchlFactory(
        watphy=watphy,
        chla=102.2
    )

    WatchlFactory(
        watphy=watphy_2,
        chla=None
    )


def set_sedphy_record(station):
    sedphy = SedphyFactory.create(
        sedchem1=None,
        sedchem2=None,
        sedpol1=None,
        sedpol2=None,
        station=station,
        subdes=5.5,
        spldattim='1990-01-01 00:00:00',
        spldep=None,
        spldis=10.6,
        splvol=None,
        sievsz=6.7,
        kurt=None,
        skew=1.1,
        meanpz=None,
        medipz=4.9,
        pctsat=None,
        pctsil=9.81,
        permty=None,
        porsty=5.51,
        dwf=None,
        cod=17,
    )

    sedphy_2 = SedphyFactory.create(
        sedchem1=None,
        sedchem2=None,
        sedpol1=None,
        sedpol2=None,
        station=station,
        subdes=5.5,
        spldattim='1990-01-01 00:00:00',
        spldep=12.2,
        spldis=None,
        splvol=2.33,
        sievsz=None,
        kurt=26.7,
        skew=None,
        meanpz=67.7,
        medipz=None,
        pctsat=2.7,
        pctsil=None,
        permty=3.6,
        porsty=None,
        dwf=45.2,
        cod=None,
    )

    Sedpol1Factory(
        sedphy=sedphy,
        arsenic=None,
        cadmium=43.1,
        chromium=None,
        cobalt=32.8,
        copper=None,
        iron=59.2,
        lead=None,
        manganese=80.6,
        mercury=None,
        nickel=78.3,
        selenium=None,
        zinc=15.9,
    )

    Sedpol1Factory(
        sedphy=sedphy_2,
        arsenic=18.9,
        cadmium=None,
        chromium=67.5,
        cobalt=None,
        copper=91.4,
        iron=None,
        lead=12.7,
        manganese=None,
        mercury=25.1,
        nickel=None,
        selenium=40.2,
        zinc=None,
    )

    Sedpol2Factory(
        sedphy=sedphy,
        aluminium=64.1,
        antimony=None,
        bismuth=21.2,
        molybdenum=None,
        silver=56.3,
        titanium=None,
        vanadium=72.8,
    )

    Sedpol2Factory(
        sedphy=sedphy_2,
        aluminium=None,
        antimony=39.5,
        bismuth=None,
        molybdenum=87.9,
        silver=None,
        titanium=10.4,
        vanadium=None,
    )

    Sedchem1Factory(
        sedphy=sedphy,
        fluoride=35.7,
        kjn=None,
        oxa=82.1,
        toc=None,
        ptot=90.5,
    )

    Sedchem1Factory(
        sedphy=sedphy_2,
        fluoride=None,
        kjn=14.2,
        oxa=None,
        toc=61.8,
        ptot=None,
    )

    Sedchem2Factory(
        sedphy=sedphy,
        calcium=75.2,
        magnesium=None,
        potassium=29.1,
        sodium=None,
        strontium=53.8,
        so3=None,
    )

    Sedchem2Factory(
        sedphy=sedphy_2,
        calcium=None,
        magnesium=48.6,
        potassium=None,
        sodium=17.3,
        strontium=None,
        so3=60.9,
    )


def test_download_all_data_types(api, survey_download):
    route = '/survey/download/hydro/{}'.format(survey_download.survey_id.replace('/', '-'))

    data_types = [
        DataType.WATER.value,
        DataType.WATERNUTRIENTS.value,
        DataType.WATERCHEMISTRY.value,
        DataType.WATERPOLLUTION.value,
        DataType.WATERNUTRIENTSANDCHEMISTRY.value,
        DataType.CURRENTS.value,
        DataType.WEATHER.value,
        DataType.SEDIMENT.value,
        DataType.SEDIMENTCHEMISTRY.value,
        DataType.SEDIMENTPOLLUTION.value
    ]

    for data_type in data_types:
        r = api.get(
            route,
            params={
                'data_type': data_type
            }
        )

        assert r.status_code == 200

        current_dir = os.getcwd()

        zipped_data = r.content

        downloaded_csv_file_name = 'survey_{}.csv'.format(TEST_SURVEY_ID.replace('/', '-'))

        downloaded_csv_data_frame = get_csv_from_zipped_file(zipped_data, downloaded_csv_file_name)

        compare_csv_file_path = '{}/api/data-extractions/hydro_{}_{}.csv'.format(
            current_dir,
            data_type,
            TEST_SURVEY_ID.replace('/', '-')
        )

        compare_csv_data_frame = pd.read_csv(compare_csv_file_path)

        differences = compare_csv_data_frame.compare(downloaded_csv_data_frame)

        assert differences.empty


def get_csv_from_zipped_file(zipped_data, csv_file_name):
    data_stream = io.BytesIO(zipped_data)
    downloaded_csv_file = None
    with zipfile.ZipFile(data_stream, mode='r') as zipped_file:
        if csv_file_name in zipped_file.namelist():
            with zipped_file.open(csv_file_name) as csv_file:
                downloaded_csv_file = csv_file.read()

    data_frame = pd.read_csv(io.BytesIO(downloaded_csv_file))
    return data_frame
