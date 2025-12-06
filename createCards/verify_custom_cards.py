"""
Verify which cards in the game are from your custom database
"""
from database_manager import DatabaseManager
import sqlite3

def verify_custom_cards():
    """Check what cards are in the custom database"""
    db = DatabaseManager('../expansions/cards.cdb')
    conn = db.connect()
    cursor = conn.cursor()
    
    # Get all custom cards
    cursor.execute("""
        SELECT datas.id, texts.name, datas.type, datas.atk, datas.def, datas.level
        FROM datas 
        LEFT JOIN texts ON datas.id = texts.id 
        WHERE datas.id >= 10000001 AND datas.id < 20000000 
        ORDER BY datas.id
    """)
    custom_cards = cursor.fetchall()
    
    print("=" * 80)
    print("YOUR CUSTOM CARDS (from expansions/cards.cdb)")
    print("=" * 80)
    print(f"Total: {len(custom_cards)} cards\n")
    
    for card_id, name, card_type, atk, defense, level in custom_cards:
        if name is None:
            name = "Unknown"
        
        # Determine card type
        if card_type & 0x1:  # Monster
            if card_type & 0x10:  # Normal
                type_str = "Normal Monster"
            elif card_type & 0x20:  # Effect
                type_str = "Effect Monster"
            elif card_type & 0x40:  # Fusion
                type_str = "Fusion Monster"
            else:
                type_str = "Monster"
            stats = f"ATK: {atk}, DEF: {defense}, Level: {level}"
        elif card_type & 0x2:  # Spell
            if card_type & 0x40000:  # Equip
                type_str = "Equip Spell"
            elif card_type & 0x20000:  # Continuous
                type_str = "Continuous Spell"
            elif card_type & 0x10000:  # Quick-Play
                type_str = "Quick-Play Spell"
            else:
                type_str = "Normal Spell"
            stats = ""
        elif card_type & 0x4:  # Trap
            type_str = "Trap Card"
            stats = ""
        else:
            type_str = "Unknown"
            stats = ""
        
        print(f"  ID: {card_id:8d} | {name:30s} | {type_str:20s} {stats}")
    
    print("\n" + "=" * 80)
    print("NOTE: EDOPro loads cards from multiple databases:")
    print("  - expansions/cards.cdb (your custom cards)")
    print("  - repositories/delta-bagooska/cards.delta.cdb (official cards)")
    print("  - repositories/delta-bagooska/cards-unofficial.delta.cdb (unofficial)")
    print("  - And several other databases...")
    print("\nThe 1392 results you see includes ALL cards from ALL databases.")
    print("Your custom cards have IDs 10000001-19999999.")
    print("=" * 80)
    
    conn.close()

if __name__ == "__main__":
    verify_custom_cards()

