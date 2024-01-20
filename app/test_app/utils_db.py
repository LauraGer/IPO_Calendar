import os
from app.dba.models import Base
from sqlalchemy import Table, delete, MetaData, create_engine
from sqlalchemy.orm import sessionmaker

TEST_DB_URL = os.getenv("TEST_DB_URL")

def cleanup_test_table(engine, table):
    # metadata = MetaData(bind=engine)
    # table = Table(table_name, metadata, autoload=True)
    with engine.connect() as conn:
        delete_query = delete(table)
        conn.execute(delete_query)

engine = create_engine(TEST_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def init_test_database():
    yield SessionLocal()