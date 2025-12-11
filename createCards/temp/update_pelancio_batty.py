import sys
sys.path.insert(0, '..')
from database_manager import DatabaseManager
from constants import RACE_SUNO

db = DatabaseManager('../../expansions/cards.cdb')

# Update Pelancio and Batty to Suno race
cards = {
    10000004: 'Batty',
    10000011: 'Koala Pelancio'
}

print("Updating Pelancio and Batty to Suno race...\n")
for card_id, card_name in cards.items():
    try:
        db.update_card({'id': card_id, 'race': RACE_SUNO})
        print(f"✓ Updated {card_name} (ID: {card_id}) to Suno race")
    except Exception as e:
        print(f"✗ Failed to update {card_name} (ID: {card_id}): {e}")

print("\nUpdate complete!")
