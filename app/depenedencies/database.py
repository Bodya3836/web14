from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Dependency
def get_db():
    """
    The get_db function opens a new database connection if there is none yet for the current application context.
    It will also create the database tables if they don’t exist yet.
    
    :return: A database session
    :doc-author: Trelent
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()