"""
Check for duplicate card names and analyze database entries
"""
from database_manager import DatabaseManager
import sqlite3

def check_duplicates():
    db = DatabaseManager('../expansions/cards.cdb')
    conn = db.connect()
    cursor = conn.cursor()
    
    # Check for duplicate names
    cursor.execute("""
        SELECT name, COUNT(*) as count, GROUP_CONCAT(id) as ids
        FROM texts 
        WHERE id >= 10000001 AND id < 20000000
        GROUP BY name
        HAVING COUNT(*) > 1
        ORDER BY count DESC
    """)
    duplicates = cursor.fetchall()
    
    if duplicates:
        print("⚠️  DUPLICATE CARD NAMES FOUND:")
        print("=" * 70)
        for name, count, ids in duplicates:
            print(f"  '{name}' appears {count} times")
            print(f"    IDs: {ids}")
            print()
    else:
        print("✅ No duplicate card names found in custom database")
    
    # Check for cards with same name as official cards
    print("\n" + "=" * 70)
    print("CHECKING FOR COMMON CARD NAMES:")
    print("=" * 70)
    
    common_names = ['Blue-Eyes White Dragon', 'Dark Magician', 'Exodia']
    for name in common_names:
        cursor.execute("""
            SELECT id, name FROM texts 
            WHERE name LIKE ? AND id >= 10000001 AND id < 20000000
        """, (f'%{name}%',))
        results = cursor.fetchall()
        if results:
            print(f"\n'{name}' found in custom database:")
            for card_id, card_name in results:
                print(f"  ID: {card_id}, Name: {card_name}")
    
    # Total card count
    cursor.execute("SELECT COUNT(*) FROM datas WHERE id >= 10000001 AND id < 20000000")
    total = cursor.fetchone()[0]
    print(f"\n" + "=" * 70)
    print(f"Total custom cards in database: {total}")
    print("=" * 70)
    
    conn.close()

if __name__ == "__main__":
    check_duplicates()

