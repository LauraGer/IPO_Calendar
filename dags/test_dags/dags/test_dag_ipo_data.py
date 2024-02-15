import unittest
from datetime import datetime, timedelta
from airflow.models import DagBag
from airflow.configuration import conf
import os

from dotenv import load_dotenv
load_dotenv()

class TestLoadIPODataDag(unittest.TestCase):

    def setUp(self):

        # conf.load_test_config('unittest.cfg')

        os.environ['AIRFLOW__CORE__UNIT_TEST_MODE'] = 'True'
        os.environ['sql_alchemy_conn'] = "postgresql+psycopg2://%(POSTGRES_USER)s:%(POSTGRES_PASSWORD)s@%(HOST)s/%(APP_DB)s"

        print("SQL Alchemy Connection:", conf.get('core', 'sql_alchemy_conn'))

        self.dagbag = DagBag(dag_folder='./dags', include_examples=False)


    def test_dag_load_ipo_data_definition(self):
        dag_id = 'load_ipo_data_to_postgres'
        dag = self.dagbag.get_dag(dag_id)
        # self.assertIsNotNone(dag)
        self.assertEqual(dag.schedule_interval, timedelta(days=7))
        self.assertEqual(dag.start_date, datetime(2023, 1, 1))
        self.assertFalse(dag.catchup)

    def test_tasks_in_dag(self):
        dag_id = 'load_ipo_data_to_postgres'
        dag = self.dagbag.get_dag(dag_id)

        # Check if tasks exist in the DAG
        self.assertIn('create_table_task', dag.task_dict)
        self.assertIn('write_dataframe_to_postgres_task', dag.task_dict)
        self.assertIn('remove_duplicates_task', dag.task_dict)

        # Additional checks can be added to verify task properties if necessary

if __name__ == '__main__':
    unittest.main()