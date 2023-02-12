from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from core.config import settings
#DATABASE_URL = config.DATABASE_URL
DATABASE_URL = "mysql+mysqldb://root:root123@localhost/sqhit"


db_engine = create_engine(DATABASE_URL,pool_recycle=60 * 5, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=db_engine)

Base = declarative_base()


def get_db():
    """
    Function to generate db session
    :return: Session
    """
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
