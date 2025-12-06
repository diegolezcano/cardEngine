"""
Database Manager for Yu-Gi-Oh! Card Database
Handles all database operations for card creation, updating, and querying
"""

import sqlite3
import os
from typing import Optional, Dict, Any, List
from constants import *


class DatabaseManager:
    """Manages SQLite database operations for Yu-Gi-Oh! cards"""
    
    def __init__(self, db_path: str):
        """
        Initialize database manager
        
        Args:
            db_path: Path to the .cdb database file
        """
        self.db_path = db_path
        
    def connect(self):
        """Create a database connection"""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found: {self.db_path}")
        return sqlite3.connect(self.db_path)
    
    def card_exists(self, card_id: int) -> bool:
        """
        Check if a card with the given ID exists in the database
        
        Args:
            card_id: Card ID to check
            
        Returns:
            True if card exists, False otherwise
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM datas WHERE id = ?", (card_id,))
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except Exception as e:
            print(f"Error checking card existence: {e}")
            return False
    
    def get_card(self, card_id: int) -> Optional[Dict[str, Any]]:
        """
        Get card data from database
        
        Args:
            card_id: Card ID to retrieve
            
        Returns:
            Dictionary with card data or None if not found
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Get data from both datas and texts tables
            cursor.execute("""
                SELECT datas.id, datas.ot, datas.alias, datas.setcode, datas.type, 
                       datas.atk, datas.def, datas.level, datas.race, datas.attribute, 
                       datas.category, texts.name, texts.desc
                FROM datas
                LEFT JOIN texts ON datas.id = texts.id
                WHERE datas.id = ?
            """, (card_id,))
            
            row = cursor.fetchone()
            conn.close()
            
            if not row:
                return None
            
            return {
                'id': row[0],
                'ot': row[1],
                'alias': row[2],
                'setcode': row[3],
                'type': row[4],
                'atk': row[5],
                'def': row[6],
                'level': row[7],
                'race': row[8],
                'attribute': row[9],
                'category': row[10],
                'name': row[11],
                'desc': row[12]
            }
        except Exception as e:
            print(f"Error retrieving card: {e}")
            return None
    
    def add_card(self, card_data: Dict[str, Any]) -> bool:
        """
        Add a new card to the database
        
        Args:
            card_data: Dictionary containing card information
                Required keys: id, name, desc, type, ot
                Optional keys: alias, setcode, atk, def, level, race, attribute, category
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Validate required fields
            required_fields = ['id', 'name', 'desc', 'type', 'ot']
            for field in required_fields:
                if field not in card_data:
                    print(f"Error: Missing required field '{field}'")
                    return False
            
            card_id = card_data['id']
            
            conn = self.connect()
            cursor = conn.cursor()
            
            # Check if card already exists
            if self.card_exists(card_id):
                print(f"Warning: Card with ID {card_id} already exists.")
                conn.close()
                return False
            
            # Insert into datas table
            cursor.execute("""
                INSERT INTO datas (id, ot, alias, setcode, type, atk, def, level, race, attribute, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                card_id,
                card_data.get('ot', SCOPE_OCG_TCG),
                card_data.get('alias', 0),
                card_data.get('setcode', 0),
                card_data['type'],
                card_data.get('atk', 0),
                card_data.get('def', 0),
                card_data.get('level', 0),
                card_data.get('race', 0),
                card_data.get('attribute', 0),
                card_data.get('category', 0)
            ))
            
            # Insert into texts table
            cursor.execute("""
                INSERT INTO texts (id, name, desc, str1, str2, str3, str4, str5, str6, 
                                  str7, str8, str9, str10, str11, str12, str13, str14, str15, str16)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                card_id,
                card_data['name'],
                card_data['desc'],
                card_data.get('str1', ''),
                card_data.get('str2', ''),
                card_data.get('str3', ''),
                card_data.get('str4', ''),
                card_data.get('str5', ''),
                card_data.get('str6', ''),
                card_data.get('str7', ''),
                card_data.get('str8', ''),
                card_data.get('str9', ''),
                card_data.get('str10', ''),
                card_data.get('str11', ''),
                card_data.get('str12', ''),
                card_data.get('str13', ''),
                card_data.get('str14', ''),
                card_data.get('str15', ''),
                card_data.get('str16', '')
            ))
            
            conn.commit()
            conn.close()
            
            print(f"✓ Successfully added card: {card_data['name']} (ID: {card_id})")
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Database error: {e}")
            return False
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    def update_card(self, card_data: Dict[str, Any]) -> bool:
        """
        Update an existing card in the database
        
        Args:
            card_data: Dictionary containing card information (must include 'id')
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if 'id' not in card_data:
                print("Error: Card ID is required for update")
                return False
            
            card_id = card_data['id']
            
            conn = self.connect()
            cursor = conn.cursor()
            
            # Check if card exists
            if not self.card_exists(card_id):
                print(f"Error: Card with ID {card_id} does not exist")
                conn.close()
                return False
            
            # Build update query for datas table
            datas_fields = ['ot', 'alias', 'setcode', 'type', 'atk', 'def', 'level', 'race', 'attribute', 'category']
            datas_updates = []
            datas_values = []
            
            for field in datas_fields:
                if field in card_data:
                    datas_updates.append(f"{field} = ?")
                    datas_values.append(card_data[field])
            
            if datas_updates:
                datas_values.append(card_id)
                query = f"UPDATE datas SET {', '.join(datas_updates)} WHERE id = ?"
                cursor.execute(query, datas_values)
            
            # Build update query for texts table
            texts_fields = ['name', 'desc', 'str1', 'str2', 'str3', 'str4', 'str5', 'str6',
                           'str7', 'str8', 'str9', 'str10', 'str11', 'str12', 'str13', 'str14', 'str15', 'str16']
            texts_updates = []
            texts_values = []
            
            for field in texts_fields:
                if field in card_data:
                    texts_updates.append(f"{field} = ?")
                    texts_values.append(card_data[field])
            
            if texts_updates:
                texts_values.append(card_id)
                query = f"UPDATE texts SET {', '.join(texts_updates)} WHERE id = ?"
                cursor.execute(query, texts_values)
            
            conn.commit()
            conn.close()
            
            print(f"✓ Successfully updated card ID: {card_id}")
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Database error: {e}")
            return False
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    def delete_card(self, card_id: int) -> bool:
        """
        Delete a card from the database
        
        Args:
            card_id: ID of card to delete
        
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Check if card exists
            if not self.card_exists(card_id):
                print(f"Error: Card with ID {card_id} does not exist")
                conn.close()
                return False
            
            # Delete from both tables
            cursor.execute("DELETE FROM datas WHERE id = ?", (card_id,))
            cursor.execute("DELETE FROM texts WHERE id = ?", (card_id,))
            
            conn.commit()
            conn.close()
            
            print(f"✓ Successfully deleted card ID: {card_id}")
            return True
            
        except sqlite3.Error as e:
            print(f"✗ Database error: {e}")
            return False
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    def list_custom_cards(self, min_id: int = 10000000, max_id: int = 99999999) -> List[Dict[str, Any]]:
        """
        List all custom cards within a specified ID range
        
        Args:
            min_id: Minimum card ID (default: 10000000)
            max_id: Maximum card ID (default: 99999999)
        
        Returns:
            List of dictionaries containing card data
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT datas.id, texts.name, datas.type, datas.atk, datas.def
                FROM datas
                LEFT JOIN texts ON datas.id = texts.id
                WHERE datas.id >= ? AND datas.id <= ?
                ORDER BY datas.id
            """, (min_id, max_id))
            
            cards = []
            for row in cursor.fetchall():
                cards.append({
                    'id': row[0],
                    'name': row[1],
                    'type': row[2],
                    'atk': row[3],
                    'def': row[4]
                })
            
            conn.close()
            return cards
            
        except Exception as e:
            print(f"Error listing cards: {e}")
            return []
    
    def get_next_available_id(self, start_id: int = 10000100) -> int:
        """
        Get the next available card ID starting from the specified ID
        
        Args:
            start_id: Starting ID to search from (default: 10000100)
        
        Returns:
            Next available card ID
        """
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            # Find the highest ID >= start_id
            cursor.execute("""
                SELECT MAX(id) FROM datas WHERE id >= ?
            """, (start_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result[0] is None:
                return start_id
            else:
                return result[0] + 1
                
        except Exception as e:
            print(f"Error finding next available ID: {e}")
            return start_id


def create_blank_database(db_path: str) -> bool:
    """
    Create a blank card database with the required tables
    
    Args:
        db_path: Path where the database should be created
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create datas table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS datas (
                id INTEGER PRIMARY KEY,
                ot INTEGER,
                alias INTEGER,
                setcode INTEGER,
                type INTEGER,
                atk INTEGER,
                def INTEGER,
                level INTEGER,
                race INTEGER,
                attribute INTEGER,
                category INTEGER
            )
        """)
        
        # Create texts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS texts (
                id INTEGER PRIMARY KEY,
                name TEXT,
                desc TEXT,
                str1 TEXT,
                str2 TEXT,
                str3 TEXT,
                str4 TEXT,
                str5 TEXT,
                str6 TEXT,
                str7 TEXT,
                str8 TEXT,
                str9 TEXT,
                str10 TEXT,
                str11 TEXT,
                str12 TEXT,
                str13 TEXT,
                str14 TEXT,
                str15 TEXT,
                str16 TEXT
            )
        """)
        
        conn.commit()
        conn.close()
        
        print(f"✓ Successfully created blank database: {db_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        return False

