from database_manager import DatabaseManager
from constants import *

db = DatabaseManager('../expansions/cards.cdb')

# Create Bat with a Phone - Normal Spell
card_data = {
    'id': 10000023,
    'ot': 3,
    'alias': 0,
    'setcode': 0,
    'type': TYPE_SPELL,
    'atk': 0,
    'def': 0,
    'level': 0,
    'race': 0,
    'attribute': 0,
    'category': 0,
    'name': 'Bat with a Phone',
    'desc': 'Special Summon 1 DARK monster from your hand or Deck.'
}

db.add_card(card_data)
print('Bat with a Phone card created successfully')

