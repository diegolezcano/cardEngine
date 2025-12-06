from database_manager import DatabaseManager
from constants import *

db = DatabaseManager('../expansions/cards.cdb')

# Create Huntrix - XYZ Effect Monster
# Rank 4, requires 3 Level 4 LIGHT monsters (Rumi, Zoey, Mira)
card_data = {
    'id': 10000022,
    'ot': 3,
    'alias': 0,
    'setcode': 0,
    'type': TYPE_MONSTER | TYPE_XYZ | TYPE_EFFECT,
    'atk': 0,
    'def': 0,
    'level': 4,  # Rank 4
    'race': RACE_WARRIOR,  # Using Warrior as default
    'attribute': ATTRIBUTE_LIGHT,
    'category': 0,
    'name': 'Huntrix',
    'desc': '3 Level 4 LIGHT monsters\n"Rumi" + "Zoey" + "Mira"\nAll LIGHT monsters on the field gain 50 ATK.'
}

db.add_card(card_data)
print('Huntrix card created successfully')
