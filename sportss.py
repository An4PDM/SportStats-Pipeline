from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
from config import API_KEY, CONN_ID, CONTAINER, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import pandas as pd
import requests


def extract_data(**kwargs):
    try:
        api_key = API_KEY
        date = datetime.now().strftime("%Y-%m-%d")
        url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={date}"

        #Requisição para a API
        response = requests.get(url)

        #Verificando se a conexão foi bem sucedida
        if response.status_code == 200:
            data = response.json() #Conversão para Json
            events = data.get('events',[])
            df = pd.DataFrame(events)
            df_serial = df.to_json() # Para evitar o erro de serialização

        else:
            print(f'Erro na requisição: {response.status_code}')

        kwargs['ti'].xcom_push(key='df', value=df_serial)

    except Exception as e:
        raise ValueError(f'Error on extracting data: {e}')
    
def transforming_data(**kwargs):
    ti = kwargs['ti']
    df_serial = ti.xcom_pull(key='df',task_ids='Extract')
    df = pd.read_json(df_serial)

    # Seleção de colunas específicas
    df_modified = df[['idEvent', 'strEvent', 'strSport', 'idLeague', 'strLeague', 'dateEvent', 'strTime', 'idVenue', 'strVenue']]

    # Alteração do nome das colunas
    df_modified = df_modified.rename(columns={'strEvent': 'event', 'strSport': 'sport', 'strLeague': 'league', 'strTime': 'time', 'strVenue': 'venue'})

    # Ordenação pelo id do evento
    df_modified = df_modified.sort_values(by = 'idEvent')
    
    # Seleção dos primeiros 20 registros
    df_modified = df_modified.head(20)

    # Transformação em df serializável e push dos dados
    df_serial = df_modified.to_json()
    kwargs['ti'].xcom_push(key='df', value=df_serial)

# Para salvar localmente
def loading_data_pkl(**kwargs):
    ti = kwargs['ti']
    df_serial = ti.xcom_pull(key='df', task_ids='Transform')
    df = pd.read_json(df_serial)

    # Busca do caminho absoluto em relação ao local onde o Airflow roda
    output_dir = '/home/ana/airflow/dags/SportStats/data'
    os.makedirs(output_dir, exist_ok=True) # Monta a pasta se ela não existir

    date = datetime.now().strftime("%Y-%m-%d")
    df.to_pickle(os.path.join(output_dir, f"sportstats_{date}.pkl"))

# Para salvar em um datalake no Azure
def loading_data_adls (**kwargs):
    print(1)


with DAG (
    dag_id = 'theSportsDB',
    schedule_interval='@daily',
    start_date=datetime(2025,5,13),
    catchup=True
) as dag:
    
    start = EmptyOperator(task_id='Start')
    extract = PythonOperator(task_id='Extract', python_callable=extract_data)
    transform = PythonOperator(task_id='Transform', python_callable=transforming_data)
    load_pkl = PythonOperator(task_id='Load_pkl', python_callable=loading_data_pkl)
    #load_adls = PythonOperator(task_id='Load_adls', python_callable=loading_data_adls)
    end = EmptyOperator(task_id='End')

start >> extract >> transform >> load_pkl >> end

