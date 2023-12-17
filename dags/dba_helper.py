from sqlalchemy import create_engine, MetaData
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic import command
from dba.db_model import Base

from config import HOST, DATABASE, USER, PASSWORD, DATABASE_URL


# PostgreSQL connection parameters
db_params = {
    'host': "postgres",
    'database': DATABASE,
    'user': USER,
    'password': PASSWORD,
}

print('##CREATE CONNECTION##')
engine = create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}")


def migrate_data():
    # Create a migration context and operations
    with engine.connect() as conn:
        context = MigrationContext.configure(conn)
        op = Operations(context)
        
        # Check if a migration is needed for Base
        if context.get_current_revision() != Base.metadata.tables.get(Base.__tablename__):
            # If a migration is needed, perform the migration
            command.upgrade(context, revision='head')
            print("Migration applied.")
        
        # Create tables if they do not exist
        Base.metadata.create_all(engine)
        print("Tables created.")


