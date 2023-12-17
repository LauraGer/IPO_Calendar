from config import DATABASE_URL
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Preparation
db_url = DATABASE_URL
print(db_url)
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)

# Enable logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@contextmanager
def session_scope():
    session = Session()
    print('session started')
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()