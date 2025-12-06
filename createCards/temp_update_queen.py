from database_manager import DatabaseManager
from constants import *

db = DatabaseManager('../expansions/cards.cdb')

new_desc = '2 Level 4 DARK monsters\n"Josefina - The Vampire" + "Batty"\nAll DARK monsters on the field gain 50 ATK.'

db.update_card({
    'id': 10000015,
    'type': TYPE_MONSTER | TYPE_XYZ | TYPE_EFFECT,
    'level': 4,
    'desc': new_desc
})

print('Database updated successfully')

