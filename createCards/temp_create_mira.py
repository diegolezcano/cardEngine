from database_manager import DatabaseManager
from constants import *

db = DatabaseManager('../expansions/cards.cdb')

card_data = {
    'id': 10000019,
    'name': 'Mira',
    'desc': 'A normal monster.',
    'type': TYPE_MONSTER | TYPE_NORMAL,
    'atk': 110,
    'def': 90,
    'level': 4,
    'race': RACE_FIEND,
    'attribute': ATTRIBUTE_LIGHT,
    'ot': SCOPE_OCG_TCG,
    'alias': 0,
    'setcode': 0,
    'category': 0
}

result = db.add_card(card_data)
print('Card created:', result)

