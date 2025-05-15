from airflow import DAG
from airflow.providers.microsoft.azure.hooks.data_lake import AzureDataLakeHook
from airflow.operators.python import PythonOperator
from datetime import datetime

def test_azure_connection():
    try:
        hook = AzureDataLakeHook(azure_data_lake_conn_id="azure-data-lake-default")
        files = hook.list("")
        print(f"Conexão bem-sucedida! Arquivos encontrados: {files}")
    except Exception as e:
        print(f"Erro na conexão: {e}")

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 3, 13),
}

with DAG(
    dag_id="test_azure_datalake",
         schedule_interval='@daily',
         default_args=default_args,
         catchup=False) as dag:

    test_connection = PythonOperator(
        task_id="test_azure_connection",
        python_callable=test_azure_connection
    )

    test_connection
