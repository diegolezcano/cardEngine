#!/usr/bin/env python3
"""
Temporary script to create the "No Traps" counter trap card
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from card_creator import CardCreator
from database_manager import DatabaseManager

def main():
    """Create the No Traps counter trap card"""
    
    print("=" * 70)
    print("Creating 'No Traps' Counter Trap Card")
    print("=" * 70)
    
    # Initialize card creator
    creator = CardCreator()
    
    # Get next available card ID
    print("\nGetting next available card ID...")
    next_id = creator.db_manager.get_next_available_id(start_id=10000001)
    print(f"Next available ID: {next_id}")
    
    # Card details
    card_name = "No Traps"
    card_desc = "If a trap card is activated, negate the activation."
    image_path = r"C:\Users\vicky\Downloads\GameCards\No Traps!.jpeg"
    
    # Create the counter trap card
    print(f"\nCreating counter trap card: {card_name}")
    success = creator.create_trap(
        card_id=next_id,
        name=card_name,
        desc=card_desc,
        trap_type='counter',
        image_url=image_path
    )
    
    if success:
        print("\n" + "=" * 70)
        print(f"SUCCESS: '{card_name}' created with ID {next_id}")
        print("=" * 70)
        print(f"\nCard Details:")
        print(f"  ID: {next_id}")
        print(f"  Name: {card_name}")
        print(f"  Type: Counter Trap")
        print(f"  Effect: {card_desc}")
        print(f"\nFiles Created:")
        print(f"  Database: expansions/cards.cdb (entry added)")
        print(f"  Script: script/c{next_id}.lua")
        print(f"  Image: pics/{next_id}.jpg")
        return 0
    else:
        print("\nFAILED: Card creation failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

