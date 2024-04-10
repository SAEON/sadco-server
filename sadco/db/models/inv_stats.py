from sqlalchemy import Column, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship

from sadco.db import Base


class InvStats(Base):
    __tablename__ = 'inv_stats'

    survey_id = Column(String(9), ForeignKey('sadco.inventory.survey_id'), primary_key=True)
    station_cnt = Column(Numeric(precision=38, scale=0), nullable=False)
    watphy_cnt = Column(Numeric(precision=38, scale=0))
    watnut_cnt = Column(Numeric(precision=38, scale=0))
    watpol1_cnt = Column(Numeric(precision=38, scale=0))
    watpol2_cnt = Column(Numeric(precision=38, scale=0))
    watchem1_cnt = Column(Numeric(precision=38, scale=0))
    watchem2_cnt = Column(Numeric(precision=38, scale=0))
    watchl_cnt = Column(Numeric(precision=38, scale=0))
    sedphy_cnt = Column(Numeric(precision=38, scale=0))
    sedpes_cnt = Column(Numeric(precision=38, scale=0))
    sedpol1_cnt = Column(Numeric(precision=38, scale=0))
    sedpol2_cnt = Column(Numeric(precision=38, scale=0))
    sedchem1_cnt = Column(Numeric(precision=38, scale=0))
    sedchem2_cnt = Column(Numeric(precision=38, scale=0))
    sedtax_cnt = Column(Numeric(precision=38, scale=0))
    plaphy_cnt = Column(Numeric(precision=38, scale=0))
    plapes_cnt = Column(Numeric(precision=38, scale=0))
    plapol1_cnt = Column(Numeric(precision=38, scale=0))
    plapol2_cnt = Column(Numeric(precision=38, scale=0))
    platax_cnt = Column(Numeric(precision=38, scale=0))
    plachl_cnt = Column(Numeric(precision=38, scale=0))
    tisphy_cnt = Column(Numeric(precision=38, scale=0))
    tispes_cnt = Column(Numeric(precision=38, scale=0))
    tispol1_cnt = Column(Numeric(precision=38, scale=0))
    tispol2_cnt = Column(Numeric(precision=38, scale=0))
    tisanimal_cnt = Column(Numeric(precision=38, scale=0))
    weather_cnt = Column(Numeric(precision=38, scale=0))
    watcurrents_cnt = Column(Numeric(precision=38, scale=0))
    watosd_cnt = Column(Numeric(precision=38, scale=0))
    watctd_cnt = Column(Numeric(precision=38, scale=0))
    watxbt_cnt = Column(Numeric(precision=38, scale=0))
    watmbt_cnt = Column(Numeric(precision=38, scale=0))
    watpfl_cnt = Column(Numeric(precision=38, scale=0))
    watphy_stn_cnt = Column(Numeric(precision=38, scale=0))
    watosd_stn_cnt = Column(Numeric(precision=38, scale=0))
    watctd_stn_cnt = Column(Numeric(precision=38, scale=0))
    watxbt_stn_cnt = Column(Numeric(precision=38, scale=0))
    watmbt_stn_cnt = Column(Numeric(precision=38, scale=0))
    watpfl_stn_cnt = Column(Numeric(precision=38, scale=0))
    watnut_stn_cnt = Column(Numeric(precision=38, scale=0))
    watpol_stn_cnt = Column(Numeric(precision=38, scale=0))
    watchem_stn_cnt = Column(Numeric(precision=38, scale=0))
    watchl_stn_cnt = Column(Numeric(precision=38, scale=0))
    sedphy_stn_cnt = Column(Numeric(precision=38, scale=0))
    sedpes_stn_cnt = Column(Numeric(precision=38, scale=0))
    sedpol_stn_cnt = Column(Numeric(precision=38, scale=0))
    sedchem_stn_cnt = Column(Numeric(precision=38, scale=0))
    sedtax_stn_cnt = Column(Numeric(precision=38, scale=0))
    plaphy_stn_cnt = Column(Numeric(precision=38, scale=0))
    plapes_stn_cnt = Column(Numeric(precision=38, scale=0))
    plapol_stn_cnt = Column(Numeric(precision=38, scale=0))
    platax_stn_cnt = Column(Numeric(precision=38, scale=0))
    plachl_stn_cnt = Column(Numeric(precision=38, scale=0))
    tisphy_stn_cnt = Column(Numeric(precision=38, scale=0))
    tispes_stn_cnt = Column(Numeric(precision=38, scale=0))
    tispol_stn_cnt = Column(Numeric(precision=38, scale=0))
    tisanimal_stn_cnt = Column(Numeric(precision=38, scale=0))
    watcurrents_stn_cnt = Column(Numeric(precision=38, scale=0))

    inventory = relationship('Inventory', uselist=False, back_populates='inv_stats')
