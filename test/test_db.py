from sadco.db.models import Survey, Inventory, Watphy, Station, Sedphy, Watnut, Watchem1, Watchem2, Watpol1, Watpol2, \
    Watchl, Watcurrents, SamplingDevice, Sedpol1, Sedpol2, Sedchem1, Sedchem2, InvStats, CurMooring, CurDepth, CurData
from test.factories import InventoryFactory
from test import TestSession


def test_create_read_all():
    created_inventory = InventoryFactory()

    fetched_inventory = TestSession.query(Inventory).filter(Inventory.survey_id == created_inventory.survey_id).first()

    assert_model_equality(created_inventory, fetched_inventory)

    created_inventory_stats = created_inventory.inv_stats

    fetched_inventory_stats = TestSession.query(InvStats).filter(InvStats.survey_id == created_inventory.survey_id).first()

    assert_model_equality(created_inventory_stats, fetched_inventory_stats)

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

    created_cur_mooring = created_inventory.cur_moorings[0]

    fetched_cur_mooring = TestSession.query(CurMooring).filter(CurMooring.code == created_cur_mooring.code).first()

    assert_model_equality(created_cur_mooring, fetched_cur_mooring)

    created_cur_depth = created_cur_mooring.cur_depths[0]

    fetched_cur_depth = TestSession.query(CurDepth).filter(CurDepth.code == created_cur_depth.code).first()

    assert_model_equality(created_cur_depth, fetched_cur_depth)

    created_cur_data = created_cur_depth.cur_data_list[0]

    fetched_cur_data = TestSession.query(CurData).filter(CurData.code == created_cur_data.code).first()

    assert_model_equality(created_cur_data, fetched_cur_data)


def assert_model_equality(model1, model2):
    """Compares all attributes of two SQLAlchemy models for equality."""

    for attr in model1.__table__.columns:
        assert getattr(model1, attr.name) == getattr(model2, attr.name)
