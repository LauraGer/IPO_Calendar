"""
Copyright 2023 Laura Gerlach

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# This file keeps methods to create sql query statements
from sqlalchemy import select, func

aggregation_functions = {
    'min': func.min,
    'max': func.max,
    'avg': func.avg,
    'count': func.count
}

def get_scalar_aggregation_from_table(table, aggregation_name, *columns):
    # this function creates a aggregated sql query
    # input: table name, aggregation name and a list of columns
    # output: aggregated sql query
    aggregation_func = aggregation_functions.get(aggregation_name)
    if aggregation_func is None:
        raise ValueError(f"Aggregation function '{aggregation_name}' is not supported.")
    select_columns = [aggregation_func(column) for column in columns]
    aggregation_query = select(select_columns, from_obj=table, correlate=False)

    return aggregation_query

def get_list_of_column_values_from_table(table, column):
    select_columns =  table.c[column]
    list_query = select(select_columns)

    return list_query