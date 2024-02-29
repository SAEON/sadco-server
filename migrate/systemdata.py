import logging
import os
import pathlib

from dotenv import load_dotenv
from alembic import command
from alembic.config import Config
from sqlalchemy import delete, select, text, event, DDL
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.schema import CreateSchema

from sadco.db import Base, Session, engine

logger = logging.getLogger(__name__)


def initialize():
    logger.info('Initializing static system data...')

    load_dotenv(pathlib.Path(os.getcwd()) / '.env')  # for a local run; in a container there's no .env

    init_database_schema()

    logger.info('Done.')


def init_database_schema():
    """Create or update the ODP database schema."""
    cwd = os.getcwd()
    os.chdir(pathlib.Path(__file__).parent)

    event.listen(Base.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS sadco"))

    try:
        # alembic_cfg = Config('alembic.ini')
        try:
            with engine.connect() as conn:
                conn.execute(text('select version_num from alembic_version'))
            schema_exists = True
        except ProgrammingError:  # from psycopg2.errors.UndefinedTable
            schema_exists = False

        if not schema_exists:
            Base.metadata.create_all(engine)
            # command.stamp(alembic_cfg, 'head')
            logger.info('Created the ODP database schema.')
    finally:
        os.chdir(cwd)
