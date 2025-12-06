from database_manager import DatabaseManager
from constants import *

db = DatabaseManager('../expansions/cards.cdb')

card_data = {
    'id': 10000015,
    'name': 'Queen of the Night',
    'desc': '"Josefina - The Vampire" + "Batty"\nAll DARK monsters on the field gain 50 ATK.',
    'type': TYPE_MONSTER | TYPE_FUSION | TYPE_EFFECT,
    'atk': 200,
    'def': 100,
    'level': 5,
    'race': RACE_FIEND,
    'attribute': ATTRIBUTE_DARK,
    'ot': SCOPE_OCG_TCG,
    'alias': 0,
    'setcode': 0,
    'category': 0
}

result = db.add_card(card_data)
print('Card created:', result)

