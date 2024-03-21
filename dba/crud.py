from sqlalchemy import select, Table, MetaData, and_, or_, func, not_
from sqlalchemy.orm import Session
from dba.db_helper import get_engine_by_db_params, get_session
from dba.models_app import Base, AsOfList, AsOfStockHistory
from .schemas_app import UserCreate
import bcrypt
from sqlalchemy.exc import IntegrityError

class Create:
    @staticmethod
    def create_as_of_list_record(as_of_list: AsOfList, db_params):
        db = get_session(db_params)

        # Check if the record already exists
        existing_record = db.query(AsOfList).filter_by(listname=as_of_list.listname, symbol=as_of_list.symbol, as_of_date=as_of_list.as_of_date).first()

        if existing_record:
            # Update the existing record
            existing_record.some_attribute = as_of_list.some_attribute  # Update the attributes as needed
            db.commit()  # Commit the changes
            db.refresh(existing_record)  # Refresh the record
            return existing_record
        else:
            # Create a new record
            db.add(as_of_list)
            db.commit()
            db.refresh(as_of_list)
            return as_of_list

    @staticmethod
    def create_table_if_not_exist(db_params, Table):
        engine = get_engine_by_db_params(db_params)
        metadata = MetaData(bind=engine)

        if not metadata.tables.get(Table.__name__):
            Table.__table__.create(engine, checkfirst=True)
            return False
        return True

class Read:
    def get_as_of_distinct_listnames(db_params):
        session = get_session(db_params)
        try:
            # Fetch distinct listnames along with their corresponding AsOf dates
            results = session.query(
                AsOfList.listname.distinct()
                # ,
                # func.to_char(AsOfList.as_of_date, 'YYYY-MM-DD').label('as_of_date')
            ).all()

            # listnames_with_date = [{"listname": item[0], "as_of_date": item[1]} for item in results]
            results =  [item[0] for item in results]
            return results

        except Exception as e:
            print(f"[{__name__}] - an error occurred: {e}")

    def get_symbols_of_app(db_params):
        session = get_session(db_params)
        try:
            results = session.query(AsOfStockHistory.symbol.distinct()).filter(
                AsOfStockHistory.symbol != None,
                AsOfStockHistory.symbol != ""
            ).all()

            raw_strings = [item[0] for item in results]

            return(raw_strings)

        except Exception as e:
            print(f"[{__name__}] - an error occurred: {e}")

    def get_list_details(db_params, list_name):
        session = get_session(db_params)
        try:
            results = session.query(AsOfList.symbol,
                                    AsOfList.as_of_date,
                                    AsOfList.as_of_price
                                    ).filter(
                AsOfList.listname == list_name
            ).all()

            formatted_results = []
            for result in results:
                symbol = result[0]
                date = result[1].strftime('%Y-%m-%d')  # Format the date as 'yyyy-mm-dd'
                value = result[2]
                formatted_results.append(f'| {symbol} | {date} | {value} |<br>')
            return '\n'.join(formatted_results)

            # return(results)

        except Exception as e:
            print(f"[{__name__}] - an error occurred: {e}")

    def get_symbols_min_date_key(db_params):
        session = get_session(db_params)
        try:
            # Query to get distinct symbols and their minimum date key
            results = session.query(
                AsOfStockHistory.symbol,
                func.to_char(func.min(AsOfStockHistory.date), 'YYYY-MM-DD').label('min_date'),
                func.avg((AsOfStockHistory.open +
                            AsOfStockHistory.high +
                            AsOfStockHistory.low +
                            AsOfStockHistory.close) / 4).label('avg_price_o_h_l_c')
            ).filter(
                not_(or_(AsOfStockHistory.symbol == None, AsOfStockHistory.symbol == ""))

            ).group_by(
                AsOfStockHistory.symbol
            ).all()

            # Convert results to a list of dictionaries
            symbols_min_datekey = [{'symbol': item[0], 'min_datekey': item[1], 'avg_price_o_h_l_c': item[2]} for item in results]

            return symbols_min_datekey

        except Exception as e:
            print(f"[{__name__}] - an error occurred: {e}")

    def get_AsOf_price_by_date(db_params, date):
        session = get_session(db_params)
        try:
            # Query to get distinct symbols and their minimum date key
            results = session.query(
                func.avg((AsOfStockHistory.open +
                            AsOfStockHistory.high +
                            AsOfStockHistory.low +
                            AsOfStockHistory.close) / 4).label('avg_price_o_h_l_c')
            ).filter(
                not_(or_(AsOfStockHistory.symbol == None, AsOfStockHistory.symbol == "")),
                AsOfStockHistory.date.between(date, date + 1)

            ).group_by(
                AsOfStockHistory.symbol,
                func.to_char(func.min(AsOfStockHistory.date), 'YYYY-MM-DD')
            ).all()

            # Convert results to a list of dictionaries
            as_of_price = [item[0] for item in results]

            return as_of_price

        except Exception as e:
            print(f"[{__name__}] - an error occurred: {e}")

class Update:
    @staticmethod
    def update_list(as_of_list: AsOfList, db_params):
        db = get_session(db_params)
        db.update(as_of_list)
        db.commit()
        db.refresh(as_of_list)
        return as_of_list

class BulkInsert:
    @staticmethod
    def bulk_insert_or_replace(data, symbol, db_params):
        """
        Inserts Data of a specific symbol and updates existing
        """
        engine = get_engine_by_db_params(db_params)
        #check if table exists
        try:
            Base.metadata.create_all(bind=engine, checkfirst=True, tables=[AsOfStockHistory.__table__])
        except IntegrityError as e:
            print(f"An error occurred: {e}")

        session = get_session(db_params)
        try:
            dates = {item['date'] for item in data}

            # Check if any data already exists in the database based on symbol and date
            existing_dates = session.query( AsOfStockHistory.date).filter(
                AsOfStockHistory.symbol==symbol,
                AsOfStockHistory.date.in_(dates)
            ).all()
            existing_dates_str = [date[0].strftime('%Y-%m-%d') for date in existing_dates]
            bulk_insert_data = [item for item in data if item['date'] not in existing_dates_str]
            update_data = [item for item in data if item['date'] in existing_dates_str]

            cnt_bulk = len(bulk_insert_data)
            cnt_update = len(update_data)
            # Bulk insert for data that doesn't already exist
            if bulk_insert_data:
                objects_to_insert = [AsOfStockHistory(**item) for item in bulk_insert_data]
                if objects_to_insert:
                    session.bulk_save_objects(objects_to_insert)

            # Update for data that already exists
            for obj in update_data:
                existing_data = session.query(AsOfStockHistory).filter_by(symbol=obj['symbol'], date=obj['date']).first()
                if existing_data:
                    for key, value in obj.items():
                        # Update attributes of existing_data
                        setattr(existing_data, key, value)
                else:
                    # Handle case where the record does not exist
                    print(f"No existing record found for symbol={obj['symbol']} and date={obj['date']}")

            session.commit()
            return cnt_bulk, cnt_update
        except IntegrityError as e:
            session.rollback()
            print(f"Failed to perform bulk insertion: {e}")
        finally:
            session.close()