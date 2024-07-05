from random import randint, choice

import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker
from sqlalchemy.orm import scoped_session, sessionmaker

import sadco.db
from sadco.db.models import (Inventory, Survey, Planam, Institutes, SurveyType, Scientists, Station, StatusMode, Watphy,
                             SamplingDevice, Watnut, Watchem2, Watchem1, Watpol1, Watpol2, Watchl, Watcurrents, Sedphy,
                             Sedchem1, Sedchem2, Sedpol1, Sedpol2, InvStats, Weather, Currents, CurDepth, CurMooring,
                             CurData, CurWatphy, EDMInstrument2, WetStation, WetPeriod, WetPeriodCounts, WetData,
                             WavStation, WavData, WavPeriod)

FactorySession = scoped_session(sessionmaker(
    bind=sadco.db.engine,
    autocommit=False,
    autoflush=False,
    future=True,
))

fake = Faker()


class SADCOModelFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = FactorySession
        sqlalchemy_session_persistence = 'commit'


class ScientistsFactory(SADCOModelFactory):
    class Meta:
        model = Scientists

    code = factory.Sequence(lambda n: fake.random_number(digits=8) + n)
    surname = factory.LazyFunction(lambda: fake.name()[:20])
    f_name = factory.LazyFunction(lambda: fake.name()[:20])
    title = fake.random_element(elements=('Mrs', 'Ms', 'Dr', 'Mr'))
    instit_code = fake.random_number(digits=randint(0, 37))


class InstitutesFactory(SADCOModelFactory):
    class Meta:
        model = Institutes

    code = factory.Sequence(lambda n: f'{fake.random_number(digits=randint(1, 7))}{n}')
    name = factory.LazyFunction(lambda: fake.company())
    address = factory.LazyFunction(lambda: fake.address()[:50])


class PlanamFactory(SADCOModelFactory):
    class Meta:
        model = Planam

    code = factory.Sequence(lambda n: fake.random_number(digits=7) + n)
    name = factory.LazyFunction(lambda: fake.name())
    platform_code = factory.LazyFunction(lambda: fake.random_number(digits=randint(0, 38)))
    callsign = ''.join(fake.random_uppercase_letter() for _ in range(0, randint(0, 7)))
    nodc_country_code = ''.join(fake.random_uppercase_letter() for _ in range(0, randint(0, 2)))
    nodc_ship_code = ''.join(fake.random_uppercase_letter() for _ in range(0, randint(0, 2)))
    wod_code = factory.LazyFunction(lambda: fake.random_number(digits=randint(0, 38)))


class SurveyTypeFactory(SADCOModelFactory):
    class Meta:
        model = SurveyType

    code = factory.Sequence(lambda n: fake.random_number(digits=8) + n)
    name = factory.LazyFunction(
        lambda: choice(('Unknown', 'Hydro', 'Weather', 'UTR', 'VOS', 'Waves', 'Currents', 'Echo-Sounding'))
    )
    description = fake.text(max_nb_chars=100)


class SamplingDeviceFactory(SADCOModelFactory):
    class Meta:
        model = SamplingDevice

    code = factory.Sequence(lambda n: fake.random_number(digits=7) + n)
    name = factory.LazyFunction(lambda: fake.name()[:25])


class StatusModeFactory(SADCOModelFactory):
    class Meta:
        model = StatusMode

    code = factory.Sequence(lambda n: fake.random_number(digits=7) + n)
    flagging = factory.Faker('random_element', elements=('closed', 'open'))
    quality = factory.Faker('random_element',
                            elements=('unchecked', 'checked', 'bad', 'unknown', 'good', 'bad', 'unknown', 'good'))


class EDMInstrument2Factory(SADCOModelFactory):
    class Meta:
        model = EDMInstrument2

    code = factory.Sequence(lambda n: fake.random_number(digits=8) + n)
    name = factory.LazyFunction(lambda: fake.name()[:30])

    # cur_depth = factory.RelatedFactory('factories.CurrentDepthFactory', factory_related_name='edm_instrument2')
    # wet_period = factory.RelatedFactory('factories.WetPeriodFactory', factory_related_name='edm_instrument2')


class WavPeriodFactory(SADCOModelFactory):
    class Meta:
        model = WavPeriod

    station_id = factory.SelfAttribute('wav_station.station_id')
    yearp = factory.Sequence(lambda n: fake.random_number(digits=4) + n)
    m01 = factory.Faker('random_number', digits=randint(1, 30))
    m02 = factory.Faker('random_number', digits=randint(1, 30))
    m03 = factory.Faker('random_number', digits=randint(1, 30))
    m04 = factory.Faker('random_number', digits=randint(1, 30))
    m05 = factory.Faker('random_number', digits=randint(1, 30))
    m06 = factory.Faker('random_number', digits=randint(1, 30))
    m07 = factory.Faker('random_number', digits=randint(1, 30))
    m08 = factory.Faker('random_number', digits=randint(1, 30))
    m09 = factory.Faker('random_number', digits=randint(1, 30))
    m10 = factory.Faker('random_number', digits=randint(1, 30))
    m11 = factory.Faker('random_number', digits=randint(1, 30))
    m12 = factory.Faker('random_number', digits=randint(1, 30))

    wav_station = factory.SubFactory('factories.WavStationFactory', wav_periods=None)


class WavDataFactory(SADCOModelFactory):
    class Meta:
        model = WavData

    code = factory.Sequence(lambda n: fake.random_number(digits=8) + n)
    station_id = factory.SelfAttribute('wav_station.station_id')
    date_time = factory.Faker("date_time")
    number_readings = factory.Faker("pyint")
    record_length = factory.Faker('pydecimal', left_digits=3, right_digits=1)
    deltaf = factory.Faker('pydecimal', left_digits=2, right_digits=6)
    deltat = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    frequency = factory.Faker('pydecimal', left_digits=2, right_digits=6)
    qp = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    tb = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    te = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    wap = factory.Faker('pydecimal', left_digits=6, right_digits=2)
    eps = factory.Faker('pydecimal', left_digits=2, right_digits=3)
    hmo = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    h1 = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    hs = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    hmax = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    tc = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    tp = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    tz = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    ave_direction = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    ave_spreading = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    instrument_code = factory.Faker("pyint")
    mean_direction = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    mean_spreading = factory.Faker('pydecimal', left_digits=4, right_digits=2)

    wav_station = factory.SubFactory('factories.WavStationFactory', wav_data_list=None)


class WavStationFactory(SADCOModelFactory):
    class Meta:
        model = WavStation

    station_id = factory.Faker('lexify', text='????', letters='ABCDE-12345')
    survey_id = factory.SelfAttribute('inventory.survey_id')
    latitude = factory.Faker('pydecimal', left_digits=3, right_digits=5)
    longitude = factory.Faker('pydecimal', left_digits=3, right_digits=5)
    instrument_depth = factory.Faker('random_number', digits=randint(1, 30))
    name = factory.LazyFunction(lambda: fake.name()[:30])
    water_depth = factory.Faker('random_number', digits=randint(1, 30))

    inventory = factory.SubFactory('factories.InventoryFactory', wav_stations=None)
    wav_data_list = factory.RelatedFactory(WavDataFactory, factory_related_name='wav_station')
    wav_periods = factory.RelatedFactory(WavPeriodFactory, factory_related_name='wav_station')


class WetDataFactory(SADCOModelFactory):
    class Meta:
        model = WetData

    station_id = factory.Faker('lexify', text='????', letters='ABCDE-12345')
    period_code = factory.SelfAttribute('wet_period.code')
    date_time = factory.Faker("date_time")
    air_temp_ave = factory.Faker('pydecimal', left_digits=3, right_digits=4)
    air_temp_min = factory.Faker('pydecimal', left_digits=3, right_digits=4)
    air_temp_min_time = factory.Faker("date_time")
    air_temp_max = factory.Faker('pydecimal', left_digits=3, right_digits=4)
    air_temp_max_time = factory.Faker("date_time")
    barometric_pressure = factory.Faker('pydecimal', left_digits=5, right_digits=2)
    fog = factory.Faker('pydecimal', left_digits=4, right_digits=1)
    rainfall = factory.Faker('pydecimal', left_digits=4, right_digits=1)
    relative_humidity = factory.Faker('pydecimal', left_digits=3, right_digits=1)
    solar_radiation = factory.Faker('pydecimal', left_digits=5, right_digits=2)
    solar_radiation_max = factory.Faker('pydecimal', left_digits=5, right_digits=2)
    wind_dir = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    wind_speed_ave = factory.Faker('pydecimal', left_digits=3, right_digits=4)
    wind_speed_min = factory.Faker('pydecimal', left_digits=3, right_digits=4)
    wind_speed_max = factory.Faker('pydecimal', left_digits=3, right_digits=4)
    wind_speed_max_time = factory.Faker("date_time")
    wind_speed_max_length = factory.Faker("pyint")
    wind_speed_max_dir = factory.Faker('pydecimal', left_digits=3, right_digits=1)
    wind_speed_std = factory.Faker('pydecimal', left_digits=3, right_digits=2)

    # wet_station = factory.SubFactory('factories.WetStationFactory', wet_data_list=None)
    wet_period = factory.SubFactory('factories.WetPeriodFactory', wet_data_list=None)


class WetPeriodFactory(SADCOModelFactory):
    class Meta:
        model = WetPeriod

    code = factory.Sequence(lambda n: fake.random_number(digits=8) + n)
    station_id = factory.SelfAttribute('wet_station.station_id')
    instrument_code = factory.SelfAttribute('edm_instrument2.code')
    height_surface = factory.Faker('pydecimal', left_digits=9, right_digits=1)
    height_msl = factory.Faker('pydecimal', left_digits=9, right_digits=1)
    speed_corr_factor = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    speed_aver_method = factory.Faker('lexify', text='??????', letters='ABCDE-12345')
    dir_aver_method = factory.Faker('lexify', text='??????', letters='ABCDE-12345')
    wind_sampling_interval = factory.Faker('random_number', digits=randint(1, 9))
    start_date = factory.Faker('date')
    end_date = factory.Faker('date')
    sample_interval = factory.Faker('random_number', digits=randint(1, 9))
    number_records = factory.Faker('random_number', digits=randint(1, 9))
    number_null_records = factory.Faker('random_number', digits=randint(1, 9))
    load_date = factory.Faker('date')

    wet_data_list = factory.RelatedFactory(WetDataFactory, factory_related_name='wet_period')
    wet_station = factory.SubFactory('factories.WetStationFactory', wet_periods=None)
    edm_instrument2 = factory.SubFactory(EDMInstrument2Factory, wet_period=None)


class WetPeriodCountsFactory(SADCOModelFactory):
    class Meta:
        model = WetPeriodCounts

    station_id = factory.SelfAttribute('wet_station.station_id')
    yearp = factory.Faker('random_number', digits=randint(1, 4))
    m01 = factory.Faker('random_number', digits=randint(1, 30))
    m02 = factory.Faker('random_number', digits=randint(1, 30))
    m03 = factory.Faker('random_number', digits=randint(1, 30))
    m04 = factory.Faker('random_number', digits=randint(1, 30))
    m05 = factory.Faker('random_number', digits=randint(1, 30))
    m06 = factory.Faker('random_number', digits=randint(1, 30))
    m07 = factory.Faker('random_number', digits=randint(1, 30))
    m08 = factory.Faker('random_number', digits=randint(1, 30))
    m09 = factory.Faker('random_number', digits=randint(1, 30))
    m10 = factory.Faker('random_number', digits=randint(1, 30))
    m11 = factory.Faker('random_number', digits=randint(1, 30))
    m12 = factory.Faker('random_number', digits=randint(1, 30))

    wet_station = factory.SubFactory('factories.WetStationFactory', wet_period_counts=None)


class WetStationFactory(SADCOModelFactory):
    class Meta:
        model = WetStation

    station_id = factory.Faker('lexify', text='????', letters='ABCDE-12345')
    survey_id = factory.SelfAttribute('inventory.survey_id')
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')
    name = factory.LazyFunction(lambda: fake.name()[:30])
    client_code = factory.Faker('random_number', digits=randint(1, 30))

    inventory = factory.SubFactory('factories.InventoryFactory', wet_stations=None)
    wet_periods = factory.RelatedFactory(WetPeriodFactory, factory_related_name='wet_station')
    # wet_data_list = factory.RelatedFactory(WetDataFactory, factory_related_name='wet_station')
    wet_period_counts = factory.RelatedFactory(WetPeriodCountsFactory, factory_related_name='wet_station')


class CurrentWatphyFactory(SADCOModelFactory):
    class Meta:
        model = CurWatphy

    depth_code = factory.SelfAttribute('cur_data.depth_code')
    data_code = factory.SelfAttribute('cur_data.code')
    ph = factory.Faker('pydecimal', left_digits=2, right_digits=2)
    salinity = factory.Faker('pydecimal', left_digits=2, right_digits=4)
    dis_oxy = factory.Faker('pydecimal', left_digits=2, right_digits=2)

    cur_data = factory.SubFactory('factories.CurrentDataFactory', cur_watphy=None)


class CurrentDataFactory(SADCOModelFactory):
    class Meta:
        model = CurData

    code = factory.Sequence(lambda n: fake.random_number(digits=8) + n)
    depth_code = factory.SelfAttribute('cur_depth.code')
    datetime = factory.Faker('date')
    speed = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    direction = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    temperature = factory.Faker('pydecimal', left_digits=2, right_digits=4)
    vert_velocity = factory.Faker('pydecimal', left_digits=2, right_digits=2)
    f_speed_9 = factory.Faker('pydecimal', left_digits=2, right_digits=2)
    f_direction_9 = factory.Faker('pydecimal', left_digits=4, right_digits=1)
    f_speed_14 = factory.Faker('pydecimal', left_digits=2, right_digits=2)
    f_direction_14 = factory.Faker('pydecimal', left_digits=4, right_digits=1)
    pressure = factory.Faker('pydecimal', left_digits=4, right_digits=4)

    cur_depth = factory.SubFactory('factories.CurrentDepthFactory', cur_data_list=None)
    cur_watphy = factory.RelatedFactory(CurrentWatphyFactory, factory_related_name='cur_data')


class CurrentDepthFactory(SADCOModelFactory):
    class Meta:
        model = CurDepth

    survey_id = factory.SelfAttribute('cur_mooring.survey_id')
    code = factory.Sequence(lambda n: fake.random_number(digits=8) + n)
    spldep = factory.Faker('random_number', digits=randint(1, 4))
    instrument_number = factory.SelfAttribute('edm_instrument2.code')
    deployment_number = factory.Faker('lexify', text='?????', letters='ABCDE-12345')
    date_time_start = factory.Faker('date')
    date_time_end = factory.Faker('date')
    time_interval = factory.Faker('random_number', digits=randint(1, 30))
    number_of_records = factory.Faker('random_number', digits=randint(1, 30))
    passkey = factory.Faker('lexify', text='?????', letters='ABCDE-12345')
    date_loaded = factory.Faker('date')
    parameters = factory.Faker('lexify', text='?????', letters='ABCDE-12345')

    cur_mooring = factory.SubFactory('factories.CurrentMooringFactory', cur_depths=None)
    cur_data_list = factory.RelatedFactory(CurrentDataFactory, factory_related_name='cur_depth')
    edm_instrument2 = factory.SubFactory(EDMInstrument2Factory, cur_depth=None)


class CurrentMooringFactory(SADCOModelFactory):
    class Meta:
        model = CurMooring

    code = factory.Sequence(lambda n: fake.random_number(digits=8) + n)
    client_code = factory.Faker('random_number', digits=randint(1, 30))
    planam_code = factory.Faker('random_number', digits=randint(1, 30))
    stnnam = factory.Faker('random_number', digits=randint(1, 30))
    arenam = factory.Faker('random_number', digits=randint(1, 30))
    description = factory.Faker('text', max_nb_chars=70)
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')
    stndep = factory.Faker('random_number', digits=randint(1, 5))
    date_time_start = factory.Faker('date')
    date_time_end = factory.Faker('date')
    number_of_depths = factory.Faker('random_number', digits=randint(1, 30))
    publication_ref = factory.Faker('random_number', digits=randint(1, 30))
    survey_id = factory.SelfAttribute('inventory.survey_id')
    prjnam = factory.Faker('text', max_nb_chars=100)

    cur_depths = factory.RelatedFactory(CurrentDepthFactory, factory_related_name='cur_mooring')
    inventory = factory.SubFactory('factories.InventoryFactory', cur_moorings=None)


class CurrentsFactory(SADCOModelFactory):
    class Meta:
        model = Currents

    subdes = factory.Faker('text', max_nb_chars=10)
    spldattim = factory.Faker('date')
    spldep = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    current_dir = factory.Faker('random_number', digits=randint(1, 38))
    current_speed = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    perc_good = factory.Faker('text', max_nb_chars=20)

    station = factory.SubFactory('factories.StationFactory', sedphy_list=None)


class WeatherFactory(SADCOModelFactory):
    class Meta:
        model = Weather

    nav_equip_type = factory.Faker('text', max_nb_chars=10)
    atmosph_pres = factory.Faker('pydecimal', left_digits=4, right_digits=1)
    surface_tmp = factory.Faker('pydecimal', left_digits=2, right_digits=1)
    drybulb = factory.Faker('pydecimal', left_digits=2, right_digits=1)
    wetbulb = factory.Faker('pydecimal', left_digits=2, right_digits=1)
    cloud = factory.Faker('text', max_nb_chars=5)
    vis_code = factory.Faker('lexify', text='??', letters='ABCDE-12345')
    weather_code = factory.Faker('lexify', text='??', letters='ABCDE-12345')
    water_color = factory.Faker('random_number', digits=randint(1, 38))
    transparency = factory.Faker('random_number', digits=randint(1, 38))
    wind_dir = factory.Faker('random_number', digits=randint(1, 38))
    wind_speed = factory.Faker('pydecimal', left_digits=2, right_digits=1)
    swell_dir = factory.Faker('random_number', digits=randint(1, 38))
    swell_height = factory.Faker('pydecimal', left_digits=2, right_digits=1)
    swell_period = factory.Faker('random_number', digits=randint(1, 38))
    dupflag = factory.LazyFunction(lambda: choice(('Y', 'N')))

    station = factory.SubFactory('factories.StationFactory', sedphy_list=None)


class Sedpol1Factory(SADCOModelFactory):
    class Meta:
        model = Sedpol1

    arsenic = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    cadmium = factory.Faker('pydecimal', left_digits=3, right_digits=3)
    chromium = factory.Faker('pydecimal', left_digits=5, right_digits=3)
    cobalt = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    copper = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    iron = factory.Faker('pydecimal', left_digits=6, right_digits=3)
    lead = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    manganese = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    mercury = factory.Faker('pydecimal', left_digits=3, right_digits=4)
    nickel = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    selenium = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    zinc = factory.Faker('pydecimal', left_digits=4, right_digits=3)

    sedphy = factory.SubFactory('factories.SedphyFactory', sedpol1=None)


class Sedpol2Factory(SADCOModelFactory):
    class Meta:
        model = Sedpol2

    aluminium = factory.Faker('random_number', digits=5)
    antimony = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    bismuth = factory.Faker('pydecimal', left_digits=2, right_digits=1)
    molybdenum = factory.Faker('pydecimal', left_digits=0, right_digits=2)
    silver = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    titanium = factory.Faker('random_number', digits=4)
    vanadium = factory.Faker('pydecimal', left_digits=2, right_digits=2)

    sedphy = factory.SubFactory('factories.SedphyFactory', sedpol2=None)


class Sedchem1Factory(SADCOModelFactory):
    class Meta:
        model = Sedchem1

    fluoride = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    kjn = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    oxa = factory.Faker('pydecimal', left_digits=3, right_digits=3)
    toc = factory.Faker('pydecimal', left_digits=3, right_digits=3)
    ptot = factory.Faker('pydecimal', left_digits=3, right_digits=3)

    sedphy = factory.SubFactory('factories.SedphyFactory', sedchem1=None)


class Sedchem2Factory(SADCOModelFactory):
    class Meta:
        model = Sedchem2

    calcium = factory.Faker('pydecimal', left_digits=6, right_digits=3)
    magnesium = factory.Faker('pydecimal', left_digits=5, right_digits=2)
    potassium = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    sodium = factory.Faker('pydecimal', left_digits=5, right_digits=2)
    strontium = factory.Faker('pydecimal', left_digits=5, right_digits=3)
    so3 = factory.Faker('pydecimal', left_digits=3, right_digits=3)

    sedphy = factory.SubFactory('factories.SedphyFactory', sedchem2=None)


class SedphyFactory(SADCOModelFactory):
    class Meta:
        model = Sedphy

    code = factory.Sequence(lambda n: fake.random_number(digits=7) + n)
    device_code = factory.Faker('random_number', digits=randint(1, 8))
    method_code = factory.Faker('random_number', digits=randint(1, 8))
    standard_code = factory.Faker('random_number', digits=randint(1, 8))
    subdes = factory.Faker('text', max_nb_chars=5)
    spldattim = factory.Faker('date_time')
    spldep = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    spldis = factory.Faker('random_number', digits=randint(1, 38))
    splvol = factory.Faker('pydecimal', left_digits=3, right_digits=1)
    sievsz = factory.Faker('pydecimal', left_digits=6, right_digits=1)
    kurt = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    skew = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    meanpz = factory.Faker('random_number', digits=randint(1, 38))
    medipz = factory.Faker('random_number', digits=randint(1, 38))
    pctsat = factory.Faker('pydecimal', left_digits=2, right_digits=1)
    pctsil = factory.Faker('pydecimal', left_digits=2, right_digits=1)
    permty = factory.Faker('random_number', digits=randint(1, 38))
    porsty = factory.Faker('pydecimal', left_digits=2, right_digits=1)
    dwf = factory.Faker('pydecimal', left_digits=3, right_digits=4)
    cod = factory.Faker('pydecimal', left_digits=2, right_digits=3)

    station = factory.SubFactory('factories.StationFactory', sedphy_list=None)
    sedchem1 = factory.RelatedFactory(Sedchem1Factory, factory_related_name='sedphy')
    sedchem2 = factory.RelatedFactory(Sedchem2Factory, factory_related_name='sedphy')
    sedpol1 = factory.RelatedFactory(Sedpol1Factory, factory_related_name='sedphy')
    sedpol2 = factory.RelatedFactory(Sedpol2Factory, factory_related_name='sedphy')


class WatcurrentsFactory(SADCOModelFactory):
    class Meta:
        model = Watcurrents

    current_dir = factory.Faker('random_number', digits=randint(1, 38))
    current_speed = factory.Faker('pydecimal', left_digits=2, right_digits=2)

    watphy = factory.SubFactory('factories.WatphyFactory', watcurrents=None)


class WatchlFactory(SADCOModelFactory):
    class Meta:
        model = Watchl

    chla = factory.Faker('pydecimal', left_digits=3, right_digits=3)
    chlb = factory.Faker('pydecimal', left_digits=3, right_digits=3)
    chlc = factory.Faker('pydecimal', left_digits=3, right_digits=3)

    watphy = factory.SubFactory('factories.WatphyFactory', watchl=None)


class Watpol1Factory(SADCOModelFactory):
    class Meta:
        model = Watpol1

    arsenic = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    cadmium = factory.Faker('pydecimal', left_digits=3, right_digits=3)
    chromium = factory.Faker('pydecimal', left_digits=5, right_digits=3)
    cobalt = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    copper = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    iron = factory.Faker('pydecimal', left_digits=6, right_digits=3)
    lead = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    manganese = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    mercury = factory.Faker('pydecimal', left_digits=3, right_digits=4)
    nickel = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    selenium = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    zinc = factory.Faker('pydecimal', left_digits=4, right_digits=3)

    watphy = factory.SubFactory('factories.WatphyFactory', watpol1=None)


class Watpol2Factory(SADCOModelFactory):
    class Meta:
        model = Watpol2

    aluminium = factory.LazyFunction(lambda: randint(0, 99999))
    antimony = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    bismuth = factory.Faker('pydecimal', left_digits=2, right_digits=1)
    molybdenum = factory.Faker('pydecimal', left_digits=2, right_digits=1)
    silver = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    titanium = factory.LazyFunction(lambda: randint(0, 9999))
    vanadium = factory.Faker('pydecimal', left_digits=2, right_digits=2)

    watphy = factory.SubFactory('factories.WatphyFactory', watpol2=None)


class Watchem1Factory(SADCOModelFactory):
    class Meta:
        model = Watchem1

    dic = factory.Faker('pydecimal', left_digits=6, right_digits=3)
    doc = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    fluoride = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    iodene = factory.Faker('pydecimal', left_digits=3, right_digits=3)
    iodate = factory.Faker('pydecimal', left_digits=3, right_digits=3)
    kjn = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    nh3 = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    nitrogen = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    oxa = factory.Faker('pydecimal', left_digits=3, right_digits=3)
    ph = factory.Faker('pydecimal', left_digits=2, right_digits=2)

    watphy = factory.SubFactory('factories.WatphyFactory', watchem1=None)


class Watchem2Factory(SADCOModelFactory):
    class Meta:
        model = Watchem2

    calcium = factory.Faker('pydecimal', left_digits=6, right_digits=3)
    cesium = factory.Faker('pydecimal', left_digits=3, right_digits=3)
    hydrocarbons = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    magnesium = factory.Faker('pydecimal', left_digits=5, right_digits=2)
    pah = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    potassium = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    rubidium = factory.Faker('pydecimal', left_digits=3, right_digits=3)
    sodium = factory.Faker('pydecimal', left_digits=5, right_digits=2)
    strontium = factory.Faker('pydecimal', left_digits=5, right_digits=3)
    so4 = factory.Faker('pydecimal', left_digits=2, right_digits=4)
    sussol = factory.Faker('pydecimal', left_digits=3, right_digits=3)

    watphy = factory.SubFactory('factories.WatphyFactory', watchem2=None)


class WatnutFactory(SADCOModelFactory):
    class Meta:
        model = Watnut

    no2 = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    no3 = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    p = factory.Faker('pydecimal', left_digits=3, right_digits=3)
    po4 = factory.Faker('pydecimal', left_digits=3, right_digits=2)
    ptot = factory.Faker('pydecimal', left_digits=3, right_digits=3)
    sio3 = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    sio4 = factory.Faker('pydecimal', left_digits=4, right_digits=2)

    watphy = factory.SubFactory('factories.WatphyFactory', watnut=None)


class WatphyFactory(SADCOModelFactory):
    class Meta:
        model = Watphy

    code = factory.Sequence(lambda n: fake.random_number(digits=7) + n)
    method_code = factory.Faker('random_number', digits=randint(1, 38))
    standard_code = factory.Faker('random_number', digits=randint(1, 38))
    subdes = factory.Faker('lexify', text='?????')
    spldattim = factory.Faker('date')
    spldep = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    filtered = factory.Faker('random_element', elements=('Y', 'N'))
    disoxygen = factory.Faker('pydecimal', left_digits=2, right_digits=2)
    salinity = factory.Faker('pydecimal', left_digits=2, right_digits=2)
    temperature = factory.Faker('pydecimal', left_digits=2, right_digits=2)
    sound_flag = factory.Faker('random_element', elements=('Y', 'N'))
    soundv = factory.Faker('pydecimal', left_digits=4, right_digits=1)
    turbidity = factory.Faker('pydecimal', left_digits=4, right_digits=3)
    pressure = factory.Faker('pydecimal', left_digits=5, right_digits=2)
    fluorescence = factory.Faker('pydecimal', left_digits=4, right_digits=4)

    station = factory.SubFactory('factories.StationFactory', watphy_list=None)
    sampling_device = factory.SubFactory(SamplingDeviceFactory)
    watnut = factory.RelatedFactory(WatnutFactory, factory_related_name='watphy')
    watchem1 = factory.RelatedFactory(Watchem1Factory, factory_related_name='watphy')
    watchem2 = factory.RelatedFactory(Watchem2Factory, factory_related_name='watphy')
    watpol1 = factory.RelatedFactory(Watpol1Factory, factory_related_name='watphy')
    watpol2 = factory.RelatedFactory(Watpol2Factory, factory_related_name='watphy')
    watchl = factory.RelatedFactory(WatchlFactory, factory_related_name='watphy')
    watcurrents = factory.RelatedFactory(WatcurrentsFactory, factory_related_name='watphy')


class StationFactory(SADCOModelFactory):
    class Meta:
        model = Station

    station_id = factory.Sequence(lambda n: f'{fake.random_number(digits=randint(1, 11))}')
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')
    date_start = factory.Faker('date')
    date_end = factory.Faker('date')
    daynull = factory.Faker('random_element', elements=('Y', 'N'))
    stnnam = factory.LazyFunction(lambda: fake.city()[:10])
    stndep = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    offshd = factory.Faker('pydecimal', left_digits=3, right_digits=3)
    passkey = factory.Faker('random_number', digits=randint(0, 8))
    dupflag = factory.Faker('random_element', elements=('Y', 'N'))
    max_spldep = factory.Faker('pydecimal', left_digits=4, right_digits=2)
    lat = factory.Faker('latitude')
    lon = factory.Faker('longitude')
    yearmon = fake.month() + "-" + str(fake.year())
    status_code = factory.SelfAttribute('status_mode.code')
    stn_ref = factory.Faker('lexify', text='?????', letters='ABCDE-12345')
    notes = factory.Faker('text', max_nb_chars=2000)

    status_mode = factory.SubFactory(StatusModeFactory)
    watphy_list = factory.RelatedFactory(WatphyFactory, factory_related_name='station')
    sedphy_list = factory.RelatedFactory(SedphyFactory, factory_related_name='station')
    survey = factory.SubFactory('factories.SurveyFactory', stations=None)


class SurveyFactory(SADCOModelFactory):
    class Meta:
        model = Survey

    survey_id = factory.SelfAttribute('inventory.survey_id')
    institute = factory.LazyFunction(lambda: fake.company()[:7])
    prjnam = factory.LazyFunction(lambda: fake.company()[:10])
    expnam = factory.LazyFunction(lambda: fake.company()[:10])
    planam = factory.LazyFunction(lambda: fake.company()[:10])
    notes_1 = factory.Faker('text', max_nb_chars=198)
    notes_2 = factory.Faker('text', max_nb_chars=38)
    notes_3 = factory.Faker('text', max_nb_chars=38)
    notes_4 = factory.Faker('text', max_nb_chars=38)

    planam_relation = None
    institute_relation = None
    inventory = factory.SubFactory('factories.InventoryFactory', survey=None)
    stations = factory.RelatedFactory(StationFactory, factory_related_name='survey')


class InvStatsFactory(SADCOModelFactory):
    class Meta:
        model = InvStats

    survey_id = factory.SelfAttribute('inventory.survey_id')
    station_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watphy_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watnut_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watpol1_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watpol2_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watchem1_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watchem2_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watchl_cnt = factory.Faker('random_number', digits=randint(1, 38))
    sedphy_cnt = factory.Faker('random_number', digits=randint(1, 38))
    sedpes_cnt = factory.Faker('random_number', digits=randint(1, 38))
    sedpol1_cnt = factory.Faker('random_number', digits=randint(1, 38))
    sedpol2_cnt = factory.Faker('random_number', digits=randint(1, 38))
    sedchem1_cnt = factory.Faker('random_number', digits=randint(1, 38))
    sedchem2_cnt = factory.Faker('random_number', digits=randint(1, 38))
    sedtax_cnt = factory.Faker('random_number', digits=randint(1, 38))
    plaphy_cnt = factory.Faker('random_number', digits=randint(1, 38))
    plapes_cnt = factory.Faker('random_number', digits=randint(1, 38))
    plapol1_cnt = factory.Faker('random_number', digits=randint(1, 38))
    plapol2_cnt = factory.Faker('random_number', digits=randint(1, 38))
    platax_cnt = factory.Faker('random_number', digits=randint(1, 38))
    plachl_cnt = factory.Faker('random_number', digits=randint(1, 38))
    tisphy_cnt = factory.Faker('random_number', digits=randint(1, 38))
    tispes_cnt = factory.Faker('random_number', digits=randint(1, 38))
    tispol1_cnt = factory.Faker('random_number', digits=randint(1, 38))
    tispol2_cnt = factory.Faker('random_number', digits=randint(1, 38))
    tisanimal_cnt = factory.Faker('random_number', digits=randint(1, 38))
    weather_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watcurrents_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watosd_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watctd_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watxbt_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watmbt_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watpfl_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watphy_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watosd_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watctd_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watxbt_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watmbt_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watpfl_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watnut_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watpol_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watchem_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watchl_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    sedphy_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    sedpes_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    sedpol_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    sedchem_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    sedtax_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    plaphy_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    plapes_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    plapol_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    platax_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    plachl_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    tisphy_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    tispes_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    tispol_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    tisanimal_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))
    watcurrents_stn_cnt = factory.Faker('random_number', digits=randint(1, 38))

    inventory = factory.SubFactory('factories.InventoryFactory', inv_stats=None)


class InventoryFactory(SADCOModelFactory):
    class Meta:
        model = Inventory

    data_centre = factory.LazyFunction(lambda: choice(('SADCO', 'DFFE')))
    survey_id = factory.Faker('lexify', text='?????????', letters='ABCDEFGHIJKLMNOP')
    project_name = factory.Sequence(lambda n: f'{fake.company()}.{n}')
    cruise_name = factory.Sequence(lambda n: f'{fake.name()}.{n}')
    national_pgm = factory.LazyFunction(lambda: choice(('Y', 'N')))
    exchange_restrict = factory.LazyFunction(lambda: choice(('Y', 'N')))
    coop_pgm = factory.LazyFunction(lambda: choice(('Y', 'N')))
    coordinated_int = factory.LazyFunction(lambda: choice(('Y', 'N')))
    port_start = factory.LazyFunction(lambda: fake.city()[:20])
    port_end = factory.LazyFunction(lambda: fake.city()[:20])
    country_code = factory.Faker('random_number', digits=randint(1, 38))
    coord_code = factory.Faker('random_number', digits=randint(1, 38))
    date_start = factory.Faker('date_between')
    date_end = factory.Faker('date_time_between_dates', datetime_start=date_start)
    lat_north = factory.Sequence(lambda n: f'{abs(fake.latitude()) + n}')
    lat_south = factory.Sequence(lambda n: f'{abs(fake.latitude()) + n}')
    long_west = factory.Sequence(lambda n: f'{-abs(fake.longitude()) + n}')
    long_east = factory.Sequence(lambda n: f'{-abs(fake.longitude()) + n}')
    areaname = factory.LazyFunction(lambda: fake.word()[:50])
    domain = factory.Faker('lexify', text='??????????', letters='ABCDEFGHIJKLMNOP')
    track_chart = factory.LazyFunction(lambda: choice(('Y', 'N')))
    target_country_code = factory.LazyFunction(lambda: randint(0, 50))
    stnid_prefix = factory.Faker('lexify', text='???', letters='ABCDE')
    gmt_diff = factory.LazyFunction(lambda: randint(-12, 12))
    gmt_freeze = factory.LazyFunction(lambda: choice(('Y', 'N')))
    projection_code = factory.Faker('random_number', digits=randint(1, 38))
    spheroid_code = factory.Faker('random_number', digits=randint(1, 38))
    datum_code = factory.Faker('random_number', digits=randint(1, 38))
    data_recorded = factory.LazyFunction(lambda: choice(('Y', 'N')))
    data_available = factory.LazyFunction(lambda: choice(('Y', 'N')))

    survey = factory.RelatedFactory(SurveyFactory, factory_related_name='inventory')
    planam = factory.SubFactory(PlanamFactory)
    cur_moorings = factory.RelatedFactory(CurrentMooringFactory, factory_related_name='inventory')
    wet_stations = factory.RelatedFactory(WetStationFactory, factory_related_name='inventory')
    wav_stations = factory.RelatedFactory(WavStationFactory, factory_related_name='inventory')
    institute = factory.SubFactory(InstitutesFactory)
    survey_type = factory.SubFactory(SurveyTypeFactory)
    scientist_1 = factory.SubFactory(ScientistsFactory)
    scientist_2 = factory.SubFactory(ScientistsFactory)
    inv_stats = factory.RelatedFactory(InvStatsFactory, factory_related_name='inventory')
