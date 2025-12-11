import sys
sys.path.insert(0, '..')
from database_manager import DatabaseManager
from constants import get_race_name

db = DatabaseManager('../../expansions/cards.cdb')

# Verify cards
card_ids = {
    10000010: 'Josefina - The Vampire',
    10000015: 'Queen of the Night'
}

print("Verifying Suno race updates...\n")
for card_id, card_name in card_ids.items():
    card = db.get_card(card_id)
    if card:
        race_name = get_race_name(card['race'])
        print(f"{card_name} (ID: {card_id})")
        print(f"  Race: {race_name} (0x{card['race']:X})")
        print(f"  Status: {'✓ Suno' if race_name == 'Suno' else '✗ NOT Suno'}")
        print()
    else:
        print(f"{card_name} (ID: {card_id}) - NOT FOUND\n")
