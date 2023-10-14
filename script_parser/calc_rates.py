"""
### DAG documntation
This is a simple ETL data pipeline example which extract rates data from API
 and load it into postgresql.
"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable


import decimal
from time import localtime, strftime
from datetime import datetime
import requests
import psycopg2

default_args = {
    "owner": "airflow",
    'start_date': days_ago(1)
}
conn = psycopg2.connect(database='test',
                            user='postgres',
                            password='password',
                            host='host.docker.internal',
                            port='5430')


variables = Variable.set(key="currency_load_variables",
                         value={"table_name": "rates",
                                "rate_base": "BTC", 
                                "rate_target": "USD",              
                                "url_base":"https://api.exchangerate.host/"},
                         serialize_json=True)
dag_variables = Variable.get("currency_load_variables", deserialize_json=True)

def import_codes(**kwargs):
# Parameters
    hist_date = "latest"
    url = dag_variables.get('url_base') + hist_date
    ingest_datetime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    
    try:
        response = requests.get(url,
            params={'base': dag_variables.get('rate_base')})
    except Exception as err:
        print(f'Error occured: {err}')
        return
    data = response.json()
    rate_date = data['date']
    value_ = str(decimal.Decimal(data['rates']['USD']))[:20]
    
    ti = kwargs['task_instance']
    ti.xcom_push(key='results', value={"rate_date":rate_date, "value_":value_, "ingest_datetime":ingest_datetime })

"""
Save rates in postgresql
"""
def insert_data(**kwargs):
    task_instance = kwargs['ti']
    results = task_instance.xcom_pull(key='results', task_ids='import_rates')
    
    print("rate_date: ", results["rate_date"])
    print("value_: ", results["value_"])
    
    ingest_datetime = strftime("%Y-%m-%d %H:%M:%S", localtime())
    
    
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {dag_variables.get('table_name')} (ingest_datetime, rate_date, rate_base, rate_target, value_ ) valueS('{ingest_datetime}','{results['rate_date']}', '{dag_variables.get('rate_base')}', '{dag_variables.get('rate_target')}', '{results['value_']}');")
    conn.commit()

    cursor.close()
    conn.close()

with DAG(dag_id = "calc-rates", schedule_interval = "*/10 * * * *",
    default_args = default_args, tags=["1T", "test"], catchup = False) as dag:
        
    dag.doc_md = __doc__

    hello_bash_task = BashOperator(task_id = 'bash_task',
                    bash_command = "echo 'Good morning my diggers!'")
    
    import_rates = PythonOperator(task_id = "import_rates",
                                                python_callable = import_codes)
    
    insert_rates = PythonOperator(task_id="insert_data",
                                                python_callable = insert_data) 
    

    
    hello_bash_task >> import_rates >> insert_rates