from database_manager import DatabaseManager
from constants import *

db = DatabaseManager('../expansions/cards.cdb')

card_data = {
    'id': 10000016,
    'name': 'ATK to DEF',
    'desc': 'All monsters on the field swap their ATK and DEF until the end of this turn.',
    'type': TYPE_SPELL,
    'atk': 0,
    'def': 0,
    'level': 0,
    'race': 0,
    'attribute': 0,
    'ot': SCOPE_OCG_TCG,
    'alias': 0,
    'setcode': 0,
    'category': 0
}

result = db.add_card(card_data)
print('Card created:', result)

