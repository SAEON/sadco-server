from decimal import Decimal

from sadco.db.models import (Survey, Inventory, Watphy, Station, Sedphy, Watnut, Watchem1, Watchem2, Watpol1, Watpol2,
                             Watchl, Watcurrents, SamplingDevice, Sedpol1, Sedpol2, Sedchem1, Sedchem2, InvStats,
                             CurMooring, CurDepth, CurData, CurWatphy, EDMInstrument2, WetStation, WetPeriod,
                             WetPeriodCounts, WetData, WavStation, WavData, WavPeriod, VosMain, VosMain2, VosMain68,
                             VosArch, VosArch2)
from test.factories import InventoryFactory
from test import TestSession
from factory.faker import faker
import factory


def test_create_read_marine():
    created_inventory = InventoryFactory()

    assert_inventory_data(created_inventory)

    assert_hydro_data(created_inventory)

    assert_current_data(created_inventory)

    assert_weather_data(created_inventory)

    assert_waves_data(created_inventory)


def assert_inventory_data(created_inventory):
    fetched_inventory = TestSession.query(Inventory).filter(Inventory.survey_id == created_inventory.survey_id).first()

    assert_model_equality(created_inventory, fetched_inventory)

    created_inventory_stats = created_inventory.inv_stats

    fetched_inventory_stats = TestSession.query(InvStats).filter(
        InvStats.survey_id == created_inventory.survey_id).first()

    assert_model_equality(created_inventory_stats, fetched_inventory_stats)


def assert_hydro_data(created_inventory):
    created_survey = created_inventory.survey

    fetched_survey = TestSession.query(Survey).filter(Survey.survey_id == created_survey.survey_id).first()

    assert_model_equality(created_survey, fetched_survey)

    created_station = created_survey.stations[0]

    fetched_station = TestSession.query(Station).filter(Station.station_id == created_station.station_id).first()

    assert_model_equality(created_station, fetched_station)

    created_watphy = created_station.watphy_list[0]

    fetched_watphy = TestSession.query(Watphy).filter(Watphy.code == created_watphy.code).first()

    assert_model_equality(created_watphy, fetched_watphy)

    created_watnut = created_watphy.watnut

    fetched_watnut = TestSession.query(Watnut).filter(Watnut.watphy_code == created_watnut.watphy_code).first()

    assert_model_equality(created_watnut, fetched_watnut)

    created_watchem1 = created_watphy.watchem1

    fetched_watchem1 = TestSession.query(Watchem1).filter(Watchem1.watphy_code == created_watchem1.watphy_code).first()

    assert_model_equality(created_watchem1, fetched_watchem1)

    created_watchem2 = created_watphy.watchem2

    fetched_watchem2 = TestSession.query(Watchem2).filter(Watchem2.watphy_code == created_watchem2.watphy_code).first()

    assert_model_equality(created_watchem2, fetched_watchem2)

    created_watpol1 = created_watphy.watpol1

    fetched_watpol1 = TestSession.query(Watpol1).filter(Watpol1.watphy_code == created_watpol1.watphy_code).first()

    assert_model_equality(created_watpol1, fetched_watpol1)

    created_watpol2 = created_watphy.watpol2

    fetched_watpol2 = TestSession.query(Watpol2).filter(Watpol2.watphy_code == created_watpol2.watphy_code).first()

    assert_model_equality(created_watpol2, fetched_watpol2)

    created_watchl = created_watphy.watchl

    fetched_watchl = TestSession.query(Watchl).filter(Watchl.watphy_code == created_watchl.watphy_code).first()

    assert_model_equality(created_watchl, fetched_watchl)

    created_watcurrents = created_watphy.watcurrents

    fetched_watcurrents = TestSession.query(Watcurrents).filter(
        Watcurrents.watphy_code == created_watcurrents.watphy_code).first()

    assert_model_equality(created_watcurrents, fetched_watcurrents)

    created_sampling_device = created_watphy.sampling_device

    fetched_sampling_device = TestSession.query(SamplingDevice).filter(
        SamplingDevice.code == created_watphy.device_code).first()

    assert_model_equality(created_sampling_device, fetched_sampling_device)

    created_sedphy = created_station.sedphy_list[0]

    fetched_sedphy = TestSession.query(Sedphy).filter(Sedphy.code == created_sedphy.code).first()

    assert_model_equality(created_sedphy, fetched_sedphy)

    created_sedpol1 = created_sedphy.sedpol1

    fetched_sedpol1 = TestSession.query(Sedpol1).filter(Sedpol1.sedphy_code == created_sedpol1.sedphy_code).first()

    assert_model_equality(created_sedpol1, fetched_sedpol1)

    created_sedpol2 = created_sedphy.sedpol2

    fetched_sedpol2 = TestSession.query(Sedpol2).filter(Sedpol2.sedphy_code == created_sedpol2.sedphy_code).first()

    assert_model_equality(created_sedpol2, fetched_sedpol2)

    created_sedchem1 = created_sedphy.sedchem1

    fetched_sedchem1 = TestSession.query(Sedchem1).filter(Sedchem1.sedphy_code == created_sedchem1.sedphy_code).first()

    assert_model_equality(created_sedchem1, fetched_sedchem1)

    created_sedchem2 = created_sedphy.sedchem2

    fetched_sedchem2 = TestSession.query(Sedchem2).filter(Sedchem2.sedphy_code == created_sedchem2.sedphy_code).first()

    assert_model_equality(created_sedchem2, fetched_sedchem2)


def assert_current_data(created_inventory):
    created_cur_mooring = created_inventory.cur_moorings[0]

    fetched_cur_mooring = TestSession.query(CurMooring).filter(CurMooring.code == created_cur_mooring.code).first()

    assert_model_equality(created_cur_mooring, fetched_cur_mooring)

    created_cur_depth = created_cur_mooring.cur_depths[0]

    fetched_cur_depth = TestSession.query(CurDepth).filter(CurDepth.code == created_cur_depth.code).first()

    assert_model_equality(created_cur_depth, fetched_cur_depth)

    created_cur_data = created_cur_depth.cur_data_list[0]

    fetched_cur_data = TestSession.query(CurData).filter(CurData.code == created_cur_data.code).first()

    assert_model_equality(created_cur_data, fetched_cur_data)

    created_cur_watphy = created_cur_data.cur_watphy

    fetched_cur_watphy = TestSession.query(CurWatphy).filter(
        CurWatphy.data_code == created_cur_watphy.data_code).first()

    assert_model_equality(created_cur_watphy, fetched_cur_watphy)

    created_edm_instrument2 = created_cur_depth.edm_instrument2

    fetched_edm_instrument2 = TestSession.query(EDMInstrument2).filter(
        EDMInstrument2.code == created_cur_depth.instrument_number).first()

    assert_model_equality(created_edm_instrument2, fetched_edm_instrument2)


def assert_weather_data(created_inventory):
    created_wet_station = created_inventory.wet_stations[0]

    fetched_wet_station = TestSession.query(WetStation).filter(
        WetStation.station_id == created_wet_station.station_id).first()

    assert_model_equality(created_wet_station, fetched_wet_station)

    created_wet_period = created_wet_station.wet_periods[0]

    fetched_wet_period = TestSession.query(WetPeriod).filter(
        WetPeriod.code == created_wet_period.code
    ).first()

    assert_model_equality(created_wet_period, fetched_wet_period)

    created_wet_period_counts = created_wet_station.wet_period_counts[0]

    fetched_wet_period_counts = TestSession.query(WetPeriodCounts).filter(
        WetPeriodCounts.station_id == created_wet_period.station_id
    ).first()

    assert_model_equality(created_wet_period_counts, fetched_wet_period_counts)

    created_wet_data = created_wet_period.wet_data_list[0]

    fetched_wet_data = TestSession.query(WetData).filter(
        WetData.period_code == created_wet_data.period_code
    ).first()

    assert_model_equality(created_wet_data, fetched_wet_data)


def assert_waves_data(created_inventory):
    created_wav_station = created_inventory.wav_stations[0]

    fetched_wav_station = TestSession.query(WavStation).filter(
        WavStation.station_id == created_wav_station.station_id).first()

    assert_model_equality(created_wav_station, fetched_wav_station)

    created_wav_data = created_wav_station.wav_data_list[0]

    fetched_wav_data = TestSession.query(WavData).filter(
        WavData.code == created_wav_data.code).first()

    assert_model_equality(created_wav_data, fetched_wav_data)

    created_wav_period = created_wav_station.wav_periods[0]

    fetched_wav_period = TestSession.query(WavPeriod).filter(
        WavPeriod.station_id == created_wav_period.station_id).first()

    assert_model_equality(created_wav_period, fetched_wav_period)


def test_create_read_vos():
    fake = faker.Faker()
    vos_data = dict(
        latitude=fake.latitude().quantize(Decimal('0.00001')),
        longitude=fake.longitude().quantize(Decimal('0.00001')),
        date_time=fake.date_time(),
        daynull=fake.lexify(text='?', letters='MTWTFSS'),
        callsign=fake.lexify(text='????????', letters='12345ABCDE'),
        country=fake.lexify(text='??', letters='ABCDEFGHIJ'),
        platform=fake.lexify(text='?', letters='ABCDEFGHIJ'),
        data_id=fake.lexify(text='??', letters='ABCDEFGHIJ'),
        quality_control=fake.lexify(text='?', letters='YN'),
        source1=fake.lexify(text='?', letters='ABCDEFGHIJ'),
        load_id=fake.random_number(digits=8),
        dupflag=fake.lexify(text='?', letters='YN'),
        atmospheric_pressure=fake.pydecimal(left_digits=4, right_digits=1),
        surface_temperature=fake.pydecimal(left_digits=2, right_digits=1),
        surface_temperature_type=fake.lexify(text='?', letters='ABCDEFGHIJ'),
        drybulb=fake.pydecimal(left_digits=2, right_digits=1),
        wetbulb=fake.pydecimal(left_digits=2, right_digits=1),
        wetbulb_ice=fake.lexify(text='?', letters='ABCDEFGHIJ'),
        dewpoint=fake.pydecimal(left_digits=2, right_digits=1),
        cloud_amount=fake.lexify(text='?', letters='ABCDEFGHIJ'),
        cloud1=fake.lexify(text='?', letters='ABCDEFGHIJ'),
        cloud2=fake.lexify(text='?', letters='ABCDEFGHIJ'),
        cloud3=fake.lexify(text='?', letters='ABCDEFGHIJ'),
        cloud4=fake.lexify(text='?', letters='ABCDEFGHIJ'),
        cloud5=fake.lexify(text='?', letters='ABCDEFGHIJ'),
        visibility_code=fake.lexify(text='??', letters='ABCDEFGHIJ'),
        weather_code=fake.lexify(text='??', letters='ABCDEFGHIJ'),
        swell_direction=fake.random_number(digits=8),
        swell_height=fake.pydecimal(left_digits=2, right_digits=1),
        swell_period=fake.random_number(digits=8),
        wave_height=fake.pydecimal(left_digits=2, right_digits=1),
        wave_period=fake.random_number(digits=8),
        wind_direction=fake.random_number(digits=8),
        wind_speed=fake.pydecimal(left_digits=2, right_digits=1),
        wind_speed_type=fake.lexify(text='?', letters='ABCDEFGHIJ'),
    )

    TestSession.add(VosMain(**vos_data))
    TestSession.add(VosMain2(**vos_data))
    TestSession.add(VosMain68(**vos_data))
    TestSession.add(VosArch(**vos_data))
    TestSession.add(VosArch2(**vos_data))
    TestSession.commit()

    fetched_vos_main = TestSession.query(VosMain).first()
    fetched_vos_main_2 = TestSession.query(VosMain2).first()
    fetched_vos_main_68 = TestSession.query(VosMain68).first()
    fetched_vos_arch = TestSession.query(VosArch).first()
    fetched_vos_arch_2 = TestSession.query(VosArch2).first()

    assert_model_equality(fetched_vos_main, VosMain(**vos_data))
    assert_model_equality(fetched_vos_main_2, VosMain2(**vos_data))
    assert_model_equality(fetched_vos_main_68, VosMain68(**vos_data))
    assert_model_equality(fetched_vos_arch, VosArch(**vos_data))
    assert_model_equality(fetched_vos_arch_2, VosArch2(**vos_data))


def assert_model_equality(model1, model2):
    """Compares all attributes of two SQLAlchemy models for equality."""

    for attr in model1.__table__.columns:
        assert getattr(model1, attr.name) == getattr(model2, attr.name)
