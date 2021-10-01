from datetime import timedelta
from textwrap import dedent
import sys
import os

from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from ops.ETL.ETLTasks import MergingDataSTG, DataCleaning, MoveHistoricalData, CurrentProducts

# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

dag = DAG(
    'etl',
    default_args=default_args,
    description='Data Cleaning Product Vendors',
    #schedule_interval=timedelta(days=1),
    start_date=days_ago(0),
    tags=['dataCleaning', 'dataTransformation']
)

start_operator = DummyOperator(task_id='Begin_execution',dag=dag)

task1 = MergingDataSTG(task_id='merge_vendors_data',dag=dag)
task2 = DataCleaning(task_id='data_cleaning',dag=dag)
task3 = MoveHistoricalData(task_id='move_historical_data',dag=dag)
task4 = CurrentProducts(task_id='current_products',dag=dag)
task5 = DummyOperator(task_id='run_recommendations',dag=dag)
task6 = DummyOperator(task_id='clean_collections',dag=dag)

end_operator = DummyOperator(task_id='Stop_execution',dag=dag)

# Tasks Dependency

start_operator >> task1 >> task2 >> task3 >> task4 >> task5 >> task6 >> end_operator

