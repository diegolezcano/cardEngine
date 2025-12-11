import sys
sys.path.insert(0, '..')
from database_manager import DatabaseManager

db = DatabaseManager('../../expansions/cards.cdb')

# Search for Pelancio and Batty
print("Searching for Pelancio and Batty...\n")

conn = db.connect()
cursor = conn.cursor()

cursor.execute("""
    SELECT datas.id, texts.name, datas.race
    FROM datas
    LEFT JOIN texts ON datas.id = texts.id
    WHERE texts.name LIKE '%Pelancio%' OR texts.name LIKE '%Batty%'
    ORDER BY texts.name
""")

results = cursor.fetchall()
conn.close()

if results:
    print(f"Found {len(results)} card(s):\n")
    for row in results:
        card_id, name, race = row
        print(f"ID: {card_id}")
        print(f"Name: {name}")
        print(f"Current Race: 0x{race:X}")
        print()
else:
    print("No cards found.")
