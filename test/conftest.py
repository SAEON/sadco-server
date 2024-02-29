import pytest

from sqlalchemy_utils import create_database, drop_database
from sqlalchemy import text, inspect

import migrate.systemdata
from sadco.db import Base, Session, engine
from sadco.config import sadco_config


@pytest.fixture(scope='session', autouse=True)
def database():
    """An auto-use, run-once fixture that provides a clean
    database with an up-to-date ODP schema."""
    create_database(url := sadco_config.SADCO.DB.URL)
    try:
        migrate.systemdata.init_database_schema()
        yield
    finally:
        drop_database(url)


@pytest.fixture(autouse=True)
def session():
    """An auto-use, per-test fixture that disposes of the current
    session after every test."""
    try:
        yield
    finally:
        Session.remove()


@pytest.fixture(autouse=True)
def delete_all_data():
    """An auto-use, per-test fixture that deletes all table data
    after every test."""
    try:
        yield
    finally:
        with engine.begin() as conn:
            inspector = inspect(engine)
            for table in Base.metadata.tables:
                if not inspector.has_table(table, schema="sadco"):
                    continue
                conn.execute(text(f'ALTER TABLE "{table}" DISABLE TRIGGER ALL'))
                conn.execute(text(f'DELETE FROM "{table}"'))
                conn.execute(text(f'ALTER TABLE "{table}" ENABLE TRIGGER ALL'))
