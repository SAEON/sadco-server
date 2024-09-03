from sqlalchemy import create_engine
import logging
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from sadco.config import sadco_config

logging.basicConfig(level=logging.DEBUG)

logging.debug("Debug message: About to connect ...")

engine = create_engine(
    sadco_config.SADCO.DB.URL,
    echo=sadco_config.SADCO.DB.ECHO,
    isolation_level=sadco_config.SADCO.DB.ISOLATION_LEVEL,
    future=True,
)

Session = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        future=True,
    )
)

logging.debug("Debug message: connected ...")

class _Base:
    __table_args__ = {"schema": "sadco"}

    def save(self):
        Session.add(self)
        Session.flush()

    def delete(self):
        Session.delete(self)
        Session.flush()

    def __repr__(self):
        try:
            params = ', '.join(f'{attr}={getattr(self, attr)!r}' for attr in getattr(self, '_repr_'))
            return f'{self.__class__.__name__}({params})'
        except AttributeError:
            return object.__repr__(self)


Base = declarative_base(cls=_Base)
