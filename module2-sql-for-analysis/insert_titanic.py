import pandas as pd
import psycopg2
import sqlite3
import os
from os.path import join, dirname
from dotenv import load_dotenv
from pathlib import Path
p = Path().absolute()


# Load file from the path
load_dotenv()

DB_HOST = os.getenv("DB_HOST", default="OOPS")
DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="OOPS")

pg_conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                           password=DB_PASSWORD, host=DB_HOST)

df = pd.read_csv('titanic.csv')
df['Name'] = df['Name'].str.replace("'", " ")

conn = sqlite3.connect('titanic.sqlite3')
curs = conn.cursor()
df.to_sql('titanic', conn)

sl_conn = sqlite3.connect('titanic.sqlite3')
sl_curs = sl_conn.cursor()

get_titanic = 'SELECT * FROM titanic;'
passengers = sl_curs.execute(get_titanic).fetchall()

create_table_statement = """
CREATE TABLE titanic1 (
    id SERIAL PRIMARY KEY,
    survived INTEGER,
    pclass INTEGER,
    name VARCHAR(150),
    sex VARCHAR(10),
    age FLOAT(1),
    sibling_spouse_aboard INTEGER,
    parents_children_aboard INTEGER,
    fare FLOAT(4)
);
"""
pg_curs = pg_conn.cursor()
pg_curs.execute(create_table_statement)


for passenger in passengers:
    insert_passenger = """
    INSERT INTO titanic1
    (survived, pclass, name, sex, age, 
    sibling_spouse_aboard, parents_children_aboard, fare)
    VALUES""" + str(passenger[1:]) + ";"
    pg_curs.execute(insert_passenger)

pg_conn.commit()
