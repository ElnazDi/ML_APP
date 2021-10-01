from datetime import timedelta
from textwrap import dedent
import sys
import os

from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

from ops.Kaufland.KauflandTasks import ReadKauflandCategories, ReadKauflandBasicData, ReadKauflandDetailedData
from ops.Netto.NettoTasks import ReadNettoCategories, ReadNettoBasicData, ReadNettoDetailedData
from ops.Aldi.AldiTasks import ReadAldiCategories, ReadAldiBasicData, ReadAldiDetailedData
# These args will get passed on to each operator

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
    'dataExtraction',
    default_args=default_args,
    description='Product vendors workflow DAG',
    #schedule_interval=timedelta(days=1),
    start_date=days_ago(0),
    tags=['dataExtraction']
)

start_operator = DummyOperator(task_id='Begin_execution',dag=dag)

# Aldi
task1 = ReadAldiCategories(task_id='Read_Categories_Aldi',dag=dag)
task2 = ReadAldiBasicData(task_id='Read_Basic_Data_Aldi',dag=dag)
task3= ReadAldiDetailedData(task_id='Read_Detailed_Data_Aldi',dag=dag)

# Netto
task4 = ReadNettoCategories(task_id='Read_Categories_Netto',dag=dag)
task5 = ReadNettoBasicData(task_id='Read_Basic_Data_Netto',dag=dag)
task6 = ReadNettoDetailedData(task_id='Read_Detailed_Data_Netto',dag=dag)

# Kaufland
task7 = ReadKauflandCategories(task_id='Read_Categories_Kaufland',dag=dag)
task8 = ReadKauflandBasicData(task_id='Read_Basic_Data_Kaufland',dag=dag)
task9 = ReadKauflandDetailedData(task_id='Read_Detailed_Data_Kaufland',dag=dag)

end_operator = DummyOperator(task_id='Stop_execution',dag=dag)

# Tasks Dependency
start_operator >> [task1, task4, task7]
task1 >> task2
task4 >> task5
task7 >> task8
[task2, task5, task8] >> end_operator

#start_operator >> [task3, task6, task9] >> end_operator
