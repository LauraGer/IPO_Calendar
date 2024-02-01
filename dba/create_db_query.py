# Copyright 2023 Laura Gerlach

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This file keeps methods to create sql query statements
"""
from sqlalchemy import select, func, text

aggregation_functions = {
    'min': func.min,
    'max': func.max,
    'avg': func.avg,
    'count': func.count
}

def get_scalar_aggregation_from_table(table, aggregation_name, *columns):
    """
    Create a scalar aggregation SQL query.

    This function takes a table name, aggregation name, and a list of columns
    to generate an SQL query that performs the specified aggregation on the specified columns.

    Parameters:
    - table: SQLAlchemy Table object representing the database table.
    - aggregation_name: String representing the desired aggregation function (e.g., 'sum', 'avg').
    - *columns: Variable-length list of column names on which the aggregation will be performed.

    Returns:
    - SQLAlchemy Select object representing the aggregation query.
    """
    aggregation_func = aggregation_functions.get(aggregation_name)
    if aggregation_func is None:
        raise ValueError(f"Aggregation function '{aggregation_name}' is not supported.")
    select_columns = [aggregation_func(column) for column in columns]
    aggregation_query = select(select_columns, from_obj=table, correlate=False)

    return aggregation_query

def get_query_list_of_column_values_from_table(table, column):
    """
    This function generates a SQL query that selects all values from a specified column in a given table.

    Parameters:
    - table: SQLAlchemy Table object representing the database table.
    - column: String representing the column name for which values will be retrieved.

    Returns:
    - SQLAlchemy Select object representing the query to retrieve the specified column values.
    """
    select_columns =  table.c[column]
    list_query = select(select_columns)

    return list_query

def get_query_columns_from_table(metadata, table_name, columns, where_condition=None,  bind_parameters=None):
    """
    Retrieve specific columns from a table based on the provided conditions.

    Parameters:
    - metadata: SQLAlchemy Metadata object.
    - table_name: Name of the table to query.
    - columns: List of column names to retrieve.
    - where_condition: Optional WHERE condition for the query.
    - bind_parameters: Additional bind parameters for the WHERE condition.

    Returns:
    - SQLAlchemy Select object representing the query to retrieve the specified column values.
    """

    # Get the table from metadata and define alias
    table = metadata.tables[table_name]
    table_alias = table.alias()

    # Create a select statement with the specified columns and the aliased table
    query = select([table_alias.columns[col] for col in columns]).select_from(table_alias)

    # Add WHERE condition if provided
    if where_condition is not None:
        query = query.where(where_condition)

    # Add bind parameters if provided
    if bind_parameters is not None:
        query = query.params(bind_parameters)

    # Apply DISTINCT
    query = query.distinct()

    return query

