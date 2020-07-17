import sqlite3

conn = sqlite3.connect('rpg_db.sqlite3')
curs = conn.cursor()

count_characters = 'SELECT COUNT(*) FROM charactercreator_character;' 
print(curs.execute(count_characters).fetchall() [0][0])

query = '''SELECT character_id, COUNT(distinct item_id) 
           FROM charactercreator_character_inventory 
           GROUP BY character_id 
           LIMIT 20'''

result = curs.execute(query).fetchall()

print('\n Each character has the following number of items:')
for each in result:
    print(f'Character {each[0]} has {each[1]} item(s).')

# Alternative character count
char = curs.execute('SELECT * FROM charactercreator_character').fetchall()
print('# of characters',len(char))


# Subclasses counts
mage = curs.execute('SELECT * FROM charactercreator_mage').fetchall()
thief = curs.execute('SELECT * FROM charactercreator_thief').fetchall()
cleric = curs.execute('SELECT * FROM charactercreator_cleric').fetchall()
fighter = curs.execute('SELECT * FROM charactercreator_fighter').fetchall()
print('# of Mages: ',len(mage))
print('# of Thieves: ',len(thief))
print('# of Clerics: ',len(cleric))
print('# of Fighters: ',len(fighter))


# items in armory_item
item = curs.execute('SELECT * FROM armory_item').fetchall()
print('# of items: ', len(item))


# weapons in armory_weapon
weapon = curs.execute('SELECT * FROM armory_weapon').fetchall()
print('# of weapons: ',len(weapon))


# items for a character (alternative)
char_inv = curs.execute('''SELECT character_id, count(item_id) 
                           FROM charactercreator_character_inventory 
                           GROUP BY character_id''').fetchall()


# weapon ownership by a character
char_w = curs.execute('''SELECT character_id, count(item_id) as weapons 
                         FROM charactercreator_character_inventory as cci, armory_weapon as w 
                         WHERE cci.item_id = w.item_ptr_id 
                         GROUP BY character_id''').fetchall()

print('\n Each character has the following number of weapons:')
for each in char_w[:20]:
    print(f'Character {each[0]} has {each[1]} weapon(s).')


# average items and weapons
ave_item = curs.execute('''SELECT avg(items)
                        FROM (SELECT count(item_id) as items
                        FROM charactercreator_character_inventory as c 
                        GROUP BY character_id )''').fetchall()[0][0]


ave_weapon = curs.execute('''SELECT avg(weapons)
                        FROM (SELECT count(item_id) as weapons
                        FROM charactercreator_character_inventory as c, armory_weapon as w
                        WHERE c.item_id = w.item_ptr_id 
                        GROUP BY character_id )''').fetchall()[0][0]


print('Average items per character: ', round(ave_item, 2))
print('Average weapons per character: ', round(ave_weapon, 2))