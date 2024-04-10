from sqlalchemy.orm import scoped_session, sessionmaker

import sadco.db

# SQLAlchemy session to use for making assertions about database state
TestSession = scoped_session(sessionmaker(
    bind=sadco.db.engine,
    autocommit=False,
    autoflush=False,
    future=True
))
