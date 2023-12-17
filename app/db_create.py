from db_setting import session_scope, engine
from db_model import IPO_Calendar, Base

print('start session')
with session_scope() as session:
    # Create the tables
    Base.metadata.create_all(engine)
    print("Tables created successfully!")