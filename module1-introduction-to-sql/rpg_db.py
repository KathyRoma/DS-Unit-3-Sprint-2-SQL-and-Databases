import sqlite3

conn = sqlite3.connect('rpg_db.sqlite3')
curs = conn.cursor()

count_characters = 'SELECT COUNT(*) FROM charactercreator_character;' 
print(curs.execute(count_characters).fetchall() [0][0])

query = 'SELECT character_id, COUNT(distinct item_id) FROM charactercreator_character_inventory GROUP BY character_id LIMIT 20'
result = curs.execute(query).fetchall()
print('\n Each character has the following number of items:')
for each in result:
    print(f'Character {each[0]} has {each[1]} item(s).')
