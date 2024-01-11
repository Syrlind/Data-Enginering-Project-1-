
'''
=================================================
Milestone 3

Nama  : Stanislaus Kanopi Johan Trielianto  
Batch : FTDS-010- HCK

Program ini dibuat untuk mempelajari prosses data enginerring yang baik ,dan dengan mengunakan 
dataset harga kos kosan/ rumah di jerman  . 
=================================================
'''



from airflow.models import DAG

from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.task_group import TaskGroup

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from datetime import datetime, timedelta
import numpy as np


from sqlalchemy import create_engine, insert
import pandas as pd




def ambil_data():
    # fetch data
    """
    In this function we used it to fetch data from postgres to convert it into csv  , for later used to be cleaned up  
    .We can see it fetch from "table_m3" ,  with usesage of  create engine and and saved by P2M3_Stanislaus_raw_data.csv file
    in data file  .   
    """
    engine = create_engine("postgresql+psycopg2://airflow:airflow@postgres:5432/airflow")
    conn = engine.connect()

    df = pd.read_sql_query("select * from table_m3", conn)

    # save to .data/ path
    df.to_csv('/opt/airflow/data/P2M3_Stanislaus_raw_data.csv' , sep=',', index=False)

def processing():
    """
    Data processing membersihkan data yang ditarik dengan bantuan pandas dan pada prosses akhir dijadikan data_clean , 
    dan setelah itu akan di kirim ke dalam elasticsearch  .     
    """
    df = pd.read_csv("/opt/airflow/data/P2M3_Stanislaus_raw_data.csv")
    
    
    df.to_csv('/opt/airflow/data/P2M3_Stanislaus_clean_data.csv',sep=',', index=False)

def upload():
    '''
    Upload dengan elasticsearch dengan port 9200   , mengirim data_clean dan dijadikan json file dan dikirim ke elastic
    search , dan akan di presentasi dengan kibana . 
    '''
    es = Elasticsearch(hosts=["http://elasticsearch:9200"])#Memasukan di port yang disediakan
    df=pd.read_csv('/opt/airflow/data/P2M3_Stanislaus_clean_data.csv')
    for i,r in df.iterrows():
        doc=r.to_json()
        res=es.index(index="frompostgresql", doc_type="doc", body=doc)
        print(res)


default_args= {
    'owner': 'Stanislaus',
    'start_date': datetime(2023, 12, 26),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),# dijalankan setiap 5 menit sekali 
}

with DAG(
    "P2M3",
    description='P2M3',
    schedule_interval='30 6 * * *', # schedule for 6:30 AM WIB,
    default_args=default_args, 
    catchup=False) as dag:

    
    fetching_data = PythonOperator(
        task_id='fetching_data',
        python_callable=ambil_data
    )
  
    # task: 2
    edit_data = PythonOperator(
    task_id='edit_data',
    python_callable=processing
)

    upload_data = PythonOperator(
    task_id='upload_data',
    python_callable=upload
)
    """
    Proses yang terpenting akan dilakukan dengan urutan berikut , fetching_data , edit_data ,upload_data 
    """
    #Fix the dependency definition
    fetching_data>> upload_data
