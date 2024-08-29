from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from core.database.config import DBConfig

engine = create_engine(DBConfig.database_url)
DBSession = sessionmaker(bind=engine)


def create_db_session() -> DBSession:
    db_session = DBSession()
    try:
        yield db_session
    finally:
        db_session.close()
