

'''
=================================================
Milestone 3

Nama  : Stanislaus Kanopi Johan Trielianto  
Batch : FTDS-010- HCK

Program ini dibuat untuk mempelajari prosses data enginerring yang baik ,dan dengan mengunakan 
dataset harga kos kosan/ rumah di jerman  . 
=================================================
'''
# persiapan data
import psycopg2 as psy
from sqlalchemy import create_engine
import pandas as pd
#menggunakan sqlalchemy

engine = create_engine('postgresql://airflow:airflow@localhost:5434/airflow')
data = pd.read_csv('data/immo_data_dirty.csv')

data.to_sql('table_m3', engine, if_exists='replace', index=True)