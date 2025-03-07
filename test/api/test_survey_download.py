import os
import zipfile
from datetime import date

import pytest
import pandas as pd
import io

from sadco.db.models import VosMain, VosMain2, VosMain68, VosArch, VosArch2, vos
from test.factories import (SurveyFactory, StationFactory, WatphyFactory, Watchem1Factory, Watchem2Factory,
                            Watpol1Factory, Watpol2Factory, WatnutFactory, InventoryFactory, WatchlFactory,
                            CurrentsFactory, WeatherFactory,
                            SedphyFactory, Sedpol1Factory, Sedpol2Factory, Sedchem1Factory, Sedchem2Factory,
                            CurrentMooringFactory,
                            CurrentDepthFactory, EDMInstrument2Factory, CurrentDataFactory, CurrentWatphyFactory,
                            WetStationFactory, WetPeriodFactory, WetDataFactory, WavStationFactory, WavDataFactory)

from sadco.const import SADCOScope
from test.api import assert_forbidden
from test import TestSession

TEST_SURVEY_ID: str = '1999/0001'


@pytest.fixture
def hydro_survey_download():
    inventory = InventoryFactory.create(survey_id=TEST_SURVEY_ID, survey=None, cur_moorings=None, wet_stations=None)
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


@pytest.fixture
def currents_survey_download():
    inventory = InventoryFactory.create(survey_id=TEST_SURVEY_ID, survey=None, cur_moorings=None, wet_stations=None)
    cur_mooring = CurrentMooringFactory.create(
        inventory=inventory,
        survey_id=inventory.survey_id,
        cur_depths=None
    )

    set_current_depth(cur_mooring)
    return cur_mooring


def set_current_depth(cur_mooring):
    ed_instrument2 = EDMInstrument2Factory.create(
        code=1,
        name='Waverider',
        cur_depth=None
    )

    current_depth = CurrentDepthFactory.create(
        cur_mooring=cur_mooring,
        survey_id=cur_mooring.survey_id,
        cur_data_list=None,
        edm_instrument2=ed_instrument2,
        spldep=250,
        time_interval=30,
        passkey='123ABC',
        parameters='Y',
    )

    set_current_data_and_watphy_records(current_depth)


def set_current_data_and_watphy_records(current_depth):
    current_data_record_1 = CurrentDataFactory.create(
        cur_depth=current_depth,
        cur_watphy=None,
        depth_code=current_depth.code,
        datetime='1999/01/01',
        speed=45,
        direction=None,
        temperature=17,
        vert_velocity=None,
        f_speed_9=12,
        f_direction_9=None,
        f_speed_14=55,
        f_direction_14=None,
        pressure=11.6,
    )

    CurrentWatphyFactory(
        cur_data=current_data_record_1,
        ph=None,
        salinity=2.4,
        dis_oxy=None
    )

    current_data_record_2 = CurrentDataFactory.create(
        cur_depth=current_depth,
        cur_watphy=None,
        depth_code=current_depth.code,
        datetime='1999/01/02',
        speed=None,
        direction=12,
        temperature=None,
        vert_velocity=23,
        f_speed_9=None,
        f_direction_9=68,
        f_speed_14=None,
        f_direction_14=14,
        pressure=None,
    )

    CurrentWatphyFactory(
        cur_data=current_data_record_2,
        ph=7.8,
        salinity=None,
        dis_oxy=17.2
    )


@pytest.fixture
def weather_survey_download():
    inventory = InventoryFactory.create(survey_id=TEST_SURVEY_ID, survey=None, cur_moorings=None, wet_stations=None,
                                        wav_stations=None)
    wet_station = WetStationFactory.create(
        survey_id=inventory.survey_id,
        inventory=inventory,
        wet_periods=None,
        latitude=30,
        longitude=70,
        name='MarionWeather'
    )

    set_wet_periods(wet_station)
    return wet_station


def set_wet_periods(wet_station):
    wet_period = WetPeriodFactory.create(
        wet_station=wet_station,
        wet_data_list=None,
        height_surface=10.5,
        height_msl=3.2
    )

    set_wet_data(wet_period)


def set_wet_data(wet_period):
    WetDataFactory(
        wet_period=wet_period,
        date_time='1999/01/02',
        air_temp_ave=12.4,
        air_temp_min=None,
        air_temp_min_time='1999/01/02 05:22',
        air_temp_max=None,
        air_temp_max_time='1999/01/02 14:07',
        barometric_pressure=None,
        fog=60.3,
        rainfall=None,
        relative_humidity=70.4,
        solar_radiation=None,
        solar_radiation_max=60,
        wind_dir=None,
        wind_speed_ave=12,
        wind_speed_min=None,
        wind_speed_max=26,
        wind_speed_max_time=None,
        wind_speed_max_length=3,
        wind_speed_max_dir=None,
        wind_speed_std=76,
    )

    WetDataFactory(
        wet_period=wet_period,
        date_time='1991/01/01',
        air_temp_ave=None,
        air_temp_min=6.3,
        air_temp_min_time=None,
        air_temp_max=25.2,
        air_temp_max_time=None,
        barometric_pressure=102.5,
        fog=None,
        rainfall=124,
        relative_humidity=None,
        solar_radiation=57,
        solar_radiation_max=None,
        wind_dir=32,
        wind_speed_ave=None,
        wind_speed_min=3,
        wind_speed_max=None,
        wind_speed_max_time='1999/01/02 13:04',
        wind_speed_max_length=None,
        wind_speed_max_dir=33.2,
        wind_speed_std=None,
    )


@pytest.fixture
def waves_survey_download():
    inventory = InventoryFactory.create(survey_id=TEST_SURVEY_ID, survey=None, cur_moorings=None, wet_stations=None,
                                        wav_stations=None)
    wav_station = WavStationFactory.create(
        survey_id=inventory.survey_id,
        inventory=inventory,
        wav_data_list=None,
        latitude=30,
        longitude=70,
        instrument_depth=150,
        water_depth=1030,
        name='MarionWeather'
    )

    set_wav_data(wav_station)

    return wav_station


def set_wav_data(wav_station):
    WavDataFactory(
        wav_station=wav_station,
        date_time='1990/01/01',
        number_readings=104,
        record_length=None,
        deltaf=12.8,
        deltat=None,
        frequency=45.37,
        qp=None,
        tb=12.6,
        te=None,
        wap=77.3,
        eps=None,
        hmo=23.4,
        h1=None,
        hs=65.2,
        hmax=None,
        tc=8.5,
        tp=None,
        tz=3.7,
        ave_direction=None,
        ave_spreading=12.6,
        instrument_code=None,
        mean_direction=36,
        mean_spreading=None
    )

    WavDataFactory(
        wav_station=wav_station,
        date_time='1991/01/01',
        number_readings=None,
        record_length=2.5,
        deltaf=None,
        deltat=34.98,
        frequency=None,
        qp=0.23,
        tb=None,
        te=18,
        wap=None,
        eps=97.3,
        hmo=None,
        h1=24.6,
        hs=None,
        hmax=3.2,
        tc=None,
        tp=90,
        tz=None,
        ave_direction=33,
        ave_spreading=None,
        instrument_code=4,
        mean_direction=None,
        mean_spreading=16.8
    )


@pytest.fixture
def vos_data():
    bounds = dict(
        north_bound=-30,
        south_bound=-40,
        east_bound=-5,
        west_bound=-15,
        start_date=date(1997, 1, 1),
        end_date=date(1999, 1, 1),
    )

    vos_data = dict(
        latitude=35,
        longitude=-10,
        date_time='01/01/1998',
        daynull='M',
        callsign='AD35',
        country='ZA',
        platform='D',
        data_id='CM',
        quality_control='Y',
        source1='Q',
        load_id=9934,
        dupflag='N',
        atmospheric_pressure=112.3,
        surface_temperature=23.4,
        surface_temperature_type='K',
        drybulb=1.4,
        wetbulb=21.2,
        wetbulb_ice='E',
        dewpoint=1.4,
        cloud_amount='H',
        cloud1='E',
        cloud2='D',
        cloud3='C',
        cloud4='H',
        cloud5='D',
        visibility_code='V',
        weather_code='R',
        swell_direction=20,
        swell_height=2.3,
        swell_period=101,
        wave_height=1.3,
        wave_period=206,
        wind_direction=22,
        wind_speed=42.6,
        wind_speed_type='K',
    )

    TestSession.add(VosMain(**vos_data))
    TestSession.add(VosMain2(**vos_data))
    TestSession.add(VosMain68(**vos_data))
    TestSession.add(VosArch(**vos_data))
    TestSession.add(VosArch2(**vos_data))
    TestSession.commit()

    return bounds


@pytest.mark.require_scope(SADCOScope.HYDRO_DOWNLOAD)
def test_download_all_hydro_data_types(api, hydro_survey_download, scopes, hydro_data_type):
    authorized = SADCOScope.HYDRO_DOWNLOAD in scopes

    route = '/survey/download/hydro/{}'.format(hydro_survey_download.survey_id.replace('/', '-'))

    r = api(scopes).get(
        route,
        params={
            'data_type': hydro_data_type
        }
    )

    if not authorized:
        assert_forbidden(r)
    else:
        assert_download_result(r, f'hydro_{hydro_data_type}')


@pytest.mark.require_scope(SADCOScope.UTR_DOWNLOAD)
def test_download_utr_data(api, currents_survey_download, scopes):
    authorized = SADCOScope.UTR_DOWNLOAD in scopes

    route = '/survey/download/utr/{}'.format(currents_survey_download.survey_id.replace('/', '-'))

    r = api(scopes).get(
        route,
        params={
            'data_type': None
        }
    )

    if not authorized:
        assert_forbidden(r)
    else:
        assert_download_result(r, 'currents')


@pytest.mark.require_scope(SADCOScope.CURRENTS_DOWNLOAD)
def test_download_currents_data(api, currents_survey_download, scopes):
    authorized = SADCOScope.CURRENTS_DOWNLOAD in scopes

    route = '/survey/download/currents/{}'.format(currents_survey_download.survey_id.replace('/', '-'))

    r = api(scopes).get(
        route,
        params={
            'data_type': None
        }
    )

    if not authorized:
        assert_forbidden(r)
    else:
        assert_download_result(r, 'currents')


@pytest.mark.require_scope(SADCOScope.WEATHER_DOWNLOAD)
def test_download_weather_data(api, weather_survey_download, scopes):
    authorized = SADCOScope.WEATHER_DOWNLOAD in scopes

    route = '/survey/download/weather/{}'.format(weather_survey_download.survey_id.replace('/', '-'))

    r = api(scopes).get(
        route,
        params={
            'data_type': None
        }
    )

    if not authorized:
        assert_forbidden(r)
    else:
        assert_download_result(r, 'weather')


@pytest.mark.require_scope(SADCOScope.WAVES_DOWNLOAD)
def test_download_waves_data(api, waves_survey_download, scopes):
    authorized = SADCOScope.WAVES_DOWNLOAD in scopes

    route = '/survey/download/waves/{}'.format(waves_survey_download.survey_id.replace('/', '-'))

    r = api(scopes).get(
        route,
        params={
            'data_type': None
        }
    )

    if not authorized:
        assert_forbidden(r)
    else:
        assert_download_result(r, 'waves')


@pytest.mark.require_scope(SADCOScope.VOS_DOWNLOAD)
def test_download_vos_data(api, vos_data, scopes):
    authorized = SADCOScope.VOS_DOWNLOAD in scopes

    route = '/vos_survey/download/'

    r = api(scopes).get(
        route,
        params={
            'north_bound': vos_data['north_bound'],
            'south_bound': vos_data['south_bound'],
            'east_bound': vos_data['east_bound'],
            'west_bound': vos_data['west_bound']
        }
    )

    if not authorized:
        assert_forbidden(r)
    else:
        assert_download_result(r, 'survey', 'VOS')


@pytest.fixture(params=['temporal_extent', 'geographical_extent'])
def download_vos_data(api, request, vos_data):
    download_params = {}

    match request.param:
        case 'temporal_extent':
            download_params = {
                'start_date': vos_data['start_date'],
                'end_date': vos_data['end_date']
            }
        case 'geographical_extent':
            download_params = {
                'north_bound': vos_data['north_bound'],
                'south_bound': vos_data['south_bound'],
                'east_bound': vos_data['east_bound'],
                'west_bound': vos_data['west_bound']
            }

    route = '/vos_survey/download/'

    api([SADCOScope.VOS_DOWNLOAD]).get(
        route,
        params=download_params
    )

    return download_params


@pytest.mark.require_scope(SADCOScope.DOWNLOAD_READ)
def test_download_vos_audit(api, scopes, download_vos_data):
    authorized = SADCOScope.DOWNLOAD_READ in scopes

    download_params = download_vos_data

    route = '/downloads/my_downloads/'

    r = api(scopes).get(
        route
    )

    if not authorized:
        assert_forbidden(r)
    else:
        for item in r.json()['items']:
            download_audit_params = item['parameters']
            for key, value in download_vos_data.items():
                if key in download_audit_params:
                    assert download_params[key] == value
                else:
                    assert not value


def assert_download_result(response, compare_file_name, file_unique_name: str = TEST_SURVEY_ID.replace('/', '-')):
    assert response.status_code == 200

    current_dir = os.getcwd()

    zipped_data = response.content

    downloaded_csv_file_name = 'survey_{}.csv'.format(file_unique_name)

    downloaded_csv_data_frame = get_csv_from_zipped_file(zipped_data, downloaded_csv_file_name)

    compare_csv_file_path = '{}/api/data-extractions/{}_{}.csv'.format(
        current_dir,
        compare_file_name,
        file_unique_name
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
