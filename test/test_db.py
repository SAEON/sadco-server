from sqlalchemy import select

from sadco.db import Session
from sadco.db.models import Survey, Inventory, Watphy, Station, Sedphy, Watnut, Watchem1, Watchem2, Watpol1, Watpol2, \
    Watchl, Watcurrents, SamplingDevice, Sedpol1, Sedpol2, Sedchem1, Sedchem2
from test.factories import ScientistsFactory, InventoryFactory, InstitutesFactory, SurveyFactory, StationFactory


def test_create_read_all():

    inventory = InventoryFactory()

    fetched_inventory = Session.query(Inventory).filter(Inventory.survey_id == inventory.survey_id).first()

    assert (fetched_inventory.survey_id, fetched_inventory.data_centre, fetched_inventory.project_name,
            fetched_inventory.cruise_name, fetched_inventory.national_pgm, fetched_inventory.exchange_restrict,
            fetched_inventory.coop_pgm, fetched_inventory.coordinated_int, fetched_inventory.planam_code,
            fetched_inventory.port_start, fetched_inventory.port_end, fetched_inventory.country_code,
            fetched_inventory.instit_code, fetched_inventory.coord_code, fetched_inventory.sci_code_1,
            fetched_inventory.sci_code_2, fetched_inventory.date_start, fetched_inventory.date_end,
            fetched_inventory.lat_north, fetched_inventory.lat_south, fetched_inventory.long_west,
            fetched_inventory.long_east, fetched_inventory.areaname, fetched_inventory.domain,
            fetched_inventory.track_chart, fetched_inventory.target_country_code, fetched_inventory.stnid_prefix,
            fetched_inventory.gmt_diff, fetched_inventory.gmt_freeze, fetched_inventory.projection_code,
            fetched_inventory.spheroid_code, fetched_inventory.datum_code, fetched_inventory.data_recorded,
            fetched_inventory.survey_type_code, fetched_inventory.data_available) == \
           (inventory.survey_id, inventory.data_centre, inventory.project_name, inventory.cruise_name,
            inventory.national_pgm, inventory.exchange_restrict, inventory.coop_pgm, inventory.coordinated_int,
            inventory.planam_code, inventory.port_start, inventory.port_end, inventory.country_code,
            inventory.instit_code, inventory.coord_code, inventory.sci_code_1, inventory.sci_code_2,
            inventory.date_start, inventory.date_end, inventory.lat_north, inventory.lat_south,
            inventory.long_west, inventory.long_east, inventory.areaname, inventory.domain, inventory.track_chart,
            inventory.target_country_code, inventory.stnid_prefix, inventory.gmt_diff, inventory.gmt_freeze,
            inventory.projection_code, inventory.spheroid_code, inventory.datum_code, inventory.data_recorded,
            inventory.survey_type_code, inventory.data_available)

    created_survey = inventory.survey

    fetched_survey = Session.query(Survey).filter(Survey.survey_id == created_survey.survey_id).first()

    assert (fetched_survey.survey_id, fetched_survey.institute, fetched_survey.instit_code, fetched_survey.prjnam,
            fetched_survey.expnam, fetched_survey.planam, fetched_survey.planam_code, fetched_survey.notes_1,
            fetched_survey.notes_2, fetched_survey.notes_3, fetched_survey.notes_4) == \
           (created_survey.survey_id, created_survey.institute, created_survey.instit_code, created_survey.prjnam,
            created_survey.expnam, created_survey.planam, created_survey.planam_code, created_survey.notes_1,
            created_survey.notes_2, created_survey.notes_3, created_survey.notes_4)

    created_station = created_survey.stations[0]

    fetched_station = Session.query(Station).filter(Station.station_id == created_station.station_id).first()

    assert (fetched_station.station_id, fetched_station.survey_id, fetched_station.latitude, fetched_station.longitude,
            fetched_station.date_start, fetched_station.date_end, fetched_station.daynull, fetched_station.stnnam,
            fetched_station.stndep, fetched_station.offshd, fetched_station.passkey, fetched_station.dupflag,
            fetched_station.max_spldep, fetched_station.lat, fetched_station.lon, fetched_station.yearmon,
            fetched_station.status_code, fetched_station.stn_ref, fetched_station.notes) == \
           (created_station.station_id, created_station.survey_id, created_station.latitude, created_station.longitude,
            created_station.date_start, created_station.date_end, created_station.daynull, created_station.stnnam,
            created_station.stndep, created_station.offshd, created_station.passkey, created_station.dupflag,
            created_station.max_spldep, created_station.lat, created_station.lon, created_station.yearmon,
            created_station.status_code, created_station.stn_ref, created_station.notes)

    created_watphy = created_station.watphy_list[0]

    fetched_watphy = Session.query(Watphy).filter(Watphy.code == created_watphy.code).first()

    assert (fetched_watphy.code, fetched_watphy.station_id, fetched_watphy.device_code, fetched_watphy.method_code,
            fetched_watphy.standard_code, fetched_watphy.subdes, fetched_watphy.spldattim, fetched_watphy.spldep,
            fetched_watphy.filtered, fetched_watphy.disoxygen, fetched_watphy.salinity, fetched_watphy.temperature,
            fetched_watphy.sound_flag, fetched_watphy.soundv, fetched_watphy.turbidity, fetched_watphy.pressure,
            fetched_watphy.fluorescence) == \
           (created_watphy.code, created_watphy.station_id, created_watphy.device_code, created_watphy.method_code,
            created_watphy.standard_code, created_watphy.subdes, created_watphy.spldattim, created_watphy.spldep,
            created_watphy.filtered, created_watphy.disoxygen, created_watphy.salinity, created_watphy.temperature,
            created_watphy.sound_flag, created_watphy.soundv, created_watphy.turbidity, created_watphy.pressure,
            created_watphy.fluorescence)

    created_watnut = created_watphy.watnut

    fetched_watnut = Session.query(Watnut).filter(Watnut.watphy_code == created_watnut.watphy_code).first()

    assert (fetched_watnut.watphy_code, fetched_watnut.no2, fetched_watnut.no3, fetched_watnut.p, fetched_watnut.po4,
            fetched_watnut.ptot, fetched_watnut.sio3, fetched_watnut.sio4) == \
           (created_watnut.watphy_code, created_watnut.no2, created_watnut.no3, created_watnut.p, created_watnut.po4,
            created_watnut.ptot, created_watnut.sio3, created_watnut.sio4)

    created_watchem1 = created_watphy.watchem1

    fetched_watchem1 = Session.query(Watchem1).filter(Watchem1.watphy_code == created_watchem1.watphy_code).first()

    assert (fetched_watchem1.watphy_code, fetched_watchem1.dic, fetched_watchem1.doc, fetched_watchem1.fluoride,
            fetched_watchem1.iodene, fetched_watchem1.iodate, fetched_watchem1.kjn, fetched_watchem1.nh3,
            fetched_watchem1.nitrogen, fetched_watchem1.oxa, fetched_watchem1.ph) == \
           (created_watchem1.watphy_code, created_watchem1.dic, created_watchem1.doc, created_watchem1.fluoride,
            created_watchem1.iodene, created_watchem1.iodate, created_watchem1.kjn, created_watchem1.nh3,
            created_watchem1.nitrogen, created_watchem1.oxa, created_watchem1.ph)

    created_watchem2 = created_watphy.watchem2

    fetched_watchem2 = Session.query(Watchem2).filter(Watchem2.watphy_code == created_watchem2.watphy_code).first()

    assert (fetched_watchem2.watphy_code, fetched_watchem2.calcium, fetched_watchem2.cesium,
            fetched_watchem2.hydrocarbons, fetched_watchem2.magnesium, fetched_watchem2.pah, fetched_watchem2.potassium,
            fetched_watchem2.rubidium, fetched_watchem2.sodium, fetched_watchem2.strontium, fetched_watchem2.so4,
            fetched_watchem2.sussol) == \
           (created_watchem2.watphy_code, created_watchem2.calcium, created_watchem2.cesium,
            created_watchem2.hydrocarbons, created_watchem2.magnesium, created_watchem2.pah,
            created_watchem2.potassium, created_watchem2.rubidium, created_watchem2.sodium,
            created_watchem2.strontium, created_watchem2.so4, created_watchem2.sussol)

    created_watpol1 = created_watphy.watpol1

    fetched_watpol1 = Session.query(Watpol1).filter(Watpol1.watphy_code == created_watpol1.watphy_code).first()

    assert (fetched_watpol1.watphy_code, fetched_watpol1.arsenic, fetched_watpol1.cadmium, fetched_watpol1.chromium,
            fetched_watpol1.cobalt, fetched_watpol1.copper, fetched_watpol1.iron, fetched_watpol1.lead,
            fetched_watpol1.manganese, fetched_watpol1.mercury, fetched_watpol1.nickel, fetched_watpol1.selenium,
            fetched_watpol1.zinc) == \
           (created_watpol1.watphy_code, created_watpol1.arsenic, created_watpol1.cadmium, created_watpol1.chromium,
            created_watpol1.cobalt, created_watpol1.copper, created_watpol1.iron, created_watpol1.lead,
            created_watpol1.manganese, created_watpol1.mercury, created_watpol1.nickel, created_watpol1.selenium,
            created_watpol1.zinc)

    created_watpol2 = created_watphy.watpol2

    fetched_watpol2 = Session.query(Watpol2).filter(Watpol2.watphy_code == created_watpol2.watphy_code).first()

    assert (fetched_watpol2.watphy_code, fetched_watpol2.aluminium, fetched_watpol2.antimony, fetched_watpol2.bismuth,
            fetched_watpol2.molybdenum, fetched_watpol2.silver, fetched_watpol2.titanium, fetched_watpol2.vanadium
            ) == \
           (created_watpol2.watphy_code, created_watpol2.aluminium, created_watpol2.antimony,
            created_watpol2.bismuth,
            created_watpol2.molybdenum, created_watpol2.silver, created_watpol2.titanium, created_watpol2.vanadium)

    created_watchl = created_watphy.watchl

    fetched_watchl = Session.query(Watchl).filter(Watchl.watphy_code == created_watchl.watphy_code).first()

    assert (fetched_watchl.watphy_code, fetched_watchl.chla, fetched_watchl.chlb, fetched_watchl.chlc) == \
           (created_watchl.watphy_code, created_watchl.chla, created_watchl.chlb, created_watchl.chlc)

    created_watcurrents = created_watphy.watcurrents

    fetched_watcurrents = Session.query(Watcurrents).filter(
        Watcurrents.watphy_code == created_watcurrents.watphy_code).first()

    assert (fetched_watcurrents.watphy_code, fetched_watcurrents.current_dir, fetched_watcurrents.current_speed) == \
           (created_watcurrents.watphy_code, created_watcurrents.current_dir, created_watcurrents.current_speed)

    created_sampling_device = created_watphy.sampling_device

    fetched_sampling_device = Session.query(SamplingDevice).filter(
        SamplingDevice.code == created_watphy.device_code).first()

    assert (fetched_sampling_device.code, fetched_sampling_device.name) == \
           (created_sampling_device.code, created_sampling_device.name)

    created_sedphy = created_station.sedphy_list[0]

    fetched_sedphy = Session.query(Sedphy).filter(Sedphy.code == created_sedphy.code).first()

    assert (fetched_sedphy.code, fetched_sedphy.station_id, fetched_sedphy.device_code, fetched_sedphy.method_code,
            fetched_sedphy.standard_code, fetched_sedphy.subdes, fetched_sedphy.spldattim, fetched_sedphy.spldep,
            fetched_sedphy.spldis, fetched_sedphy.splvol, fetched_sedphy.sievsz, fetched_sedphy.kurt,
            fetched_sedphy.skew, fetched_sedphy.meanpz, fetched_sedphy.medipz, fetched_sedphy.pctsat,
            fetched_sedphy.pctsil, fetched_sedphy.permty, fetched_sedphy.porsty, fetched_sedphy.dwf, fetched_sedphy.cod
            ) == \
           (created_sedphy.code, created_sedphy.station_id, created_sedphy.device_code, created_sedphy.method_code,
            created_sedphy.standard_code, created_sedphy.subdes, created_sedphy.spldattim, created_sedphy.spldep,
            created_sedphy.spldis, created_sedphy.splvol, created_sedphy.sievsz, created_sedphy.kurt,
            created_sedphy.skew, created_sedphy.meanpz, created_sedphy.medipz, created_sedphy.pctsat,
            created_sedphy.pctsil, created_sedphy.permty, created_sedphy.porsty, created_sedphy.dwf, created_sedphy.cod)

    created_sedpol1 = created_sedphy.sedpol1

    fetched_sedpol1 = Session.query(Sedpol1).filter(Sedpol1.sedphy_code == created_sedpol1.sedphy_code).first()

    assert (fetched_sedpol1.sedphy_code, fetched_sedpol1.arsenic, fetched_sedpol1.cadmium, fetched_sedpol1.chromium,
            fetched_sedpol1.cobalt, fetched_sedpol1.copper, fetched_sedpol1.iron, fetched_sedpol1.lead,
            fetched_sedpol1.manganese, fetched_sedpol1.mercury, fetched_sedpol1.nickel, fetched_sedpol1.selenium,
            fetched_sedpol1.zinc) == \
           (created_sedpol1.sedphy_code, created_sedpol1.arsenic, created_sedpol1.cadmium, created_sedpol1.chromium,
            created_sedpol1.cobalt, created_sedpol1.copper, created_sedpol1.iron, created_sedpol1.lead,
            created_sedpol1.manganese, created_sedpol1.mercury, created_sedpol1.nickel, created_sedpol1.selenium,
            created_sedpol1.zinc)

    created_sedpol2 = created_sedphy.sedpol2

    fetched_sedpol2 = Session.query(Sedpol2).filter(Sedpol2.sedphy_code == created_sedpol2.sedphy_code).first()

    assert (fetched_sedpol2.sedphy_code, fetched_sedpol2.aluminium, fetched_sedpol2.antimony, fetched_sedpol2.bismuth,
            fetched_sedpol2.molybdenum, fetched_sedpol2.silver, fetched_sedpol2.titanium, fetched_sedpol2.vanadium) == \
           (created_sedpol2.sedphy_code, created_sedpol2.aluminium, created_sedpol2.antimony, created_sedpol2.bismuth,
            created_sedpol2.molybdenum, created_sedpol2.silver, created_sedpol2.titanium, created_sedpol2.vanadium)

    created_sedchem1 = created_sedphy.sedchem1

    fetched_sedchem1 = Session.query(Sedchem1).filter(Sedchem1.sedphy_code == created_sedchem1.sedphy_code).first()

    assert (fetched_sedchem1.sedphy_code, fetched_sedchem1.fluoride, fetched_sedchem1.kjn, fetched_sedchem1.oxa,
            fetched_sedchem1.toc, fetched_sedchem1.ptot) == \
           (created_sedchem1.sedphy_code, created_sedchem1.fluoride, created_sedchem1.kjn, created_sedchem1.oxa,
            created_sedchem1.toc, created_sedchem1.ptot)

    created_sedchem2 = created_sedphy.sedchem2

    fetched_sedchem2 = Session.query(Sedchem2).filter(Sedchem2.sedphy_code == created_sedchem2.sedphy_code).first()

    assert (fetched_sedchem2.sedphy_code, fetched_sedchem2.calcium, fetched_sedchem2.magnesium,
            fetched_sedchem2.potassium, fetched_sedchem2.sodium, fetched_sedchem2.strontium, fetched_sedchem2.so3) == \
           (created_sedchem2.sedphy_code, created_sedchem2.calcium, created_sedchem2.magnesium,
            created_sedchem2.potassium, created_sedchem2.sodium, created_sedchem2.strontium, created_sedchem2.so3)
