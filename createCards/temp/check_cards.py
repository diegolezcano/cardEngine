import sys
sys.path.insert(0, '..')
from database_manager import DatabaseManager

db = DatabaseManager('../../expansions/cards.cdb')

# Get card details for the two IDs
card_ids = [10000010, 10000015]

print("Cards to update to Suno race:\n")
for card_id in card_ids:
    card = db.get_card(card_id)
    if card:
        print(f"ID: {card_id}")
        print(f"Name: {card['name']}")
        print(f"Current Race: 0x{card['race']:X}")
        print()
    else:
        print(f"Card ID {card_id} not found\n")
