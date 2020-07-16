
import pandas as pd
import pymongo
import sqlite3
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Load file from the path
load_dotenv()

conn = sqlite3.connect('rpg_db.sqlite3')
curs = conn.cursor()

get_rpg = 'SELECT * FROM charactercreator_character;'
characters = curs.execute(get_rpg).fetchall()


DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="OOPS")

client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster0.skazp.mongodb.net/test?retryWrites=true&w=majority")
db = client.test


for char in characters:
    rpg_char = {
        'character_id': char[0],
        'name': char[1],
        'level': char[2],
        'exp': char[3],
        'hp': char[4],
        'strength': char[5],
        'intelligence': char[6],
        'dexterity': char[7],
        'wisdom': char[8]
    }
    db.test.insert_one(rpg_char)

print(db.test.find_one({'name': 'Ali'}))