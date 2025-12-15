#!/usr/bin/env python3
"""
Yu-Gi-Oh! Card Creator - Main Script
Creates custom cards by managing database entries, Lua scripts, and images
"""

import argparse
import sys
import os
from typing import Optional, Dict, Any

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from constants import *
from database_manager import DatabaseManager
from script_generator import ScriptGenerator
from image_downloader import ImageDownloader


class CardCreator:
    """Main card creation interface"""
    
    def __init__(self, db_path: str = None, script_dir: str = None, pics_dir: str = None):
        """
        Initialize card creator
        
        Args:
            db_path: Path to card database
            script_dir: Directory for Lua scripts
            pics_dir: Directory for card images
        """
        if db_path is None:
            db_path = "../expansions/cards.cdb"
        if script_dir is None:
            script_dir = "../script"
        if pics_dir is None:
            pics_dir = "../pics"
        
        self.db_path = db_path
        self.db_manager = DatabaseManager(db_path)
        self.script_generator = ScriptGenerator(output_dir=script_dir)
        self.image_downloader = ImageDownloader(pics_directory=pics_dir)
    
    def create_card(self, card_data: Dict[str, Any], image_url: Optional[str] = None,
                   effect_pattern: Optional[str] = None, effect_params: Optional[Dict[str, Any]] = None,
                   generate_script: bool = True, overwrite: bool = False) -> bool:
        """
        Create a complete card with database entry, script, and image
        
        Args:
            card_data: Card information dictionary
            image_url: URL to download card image from
            effect_pattern: Effect pattern for script generation
            effect_params: Parameters for effect pattern
            generate_script: Whether to generate Lua script
            overwrite: Whether to overwrite existing files
        
        Returns:
            True if successful, False otherwise
        """
        card_id = card_data.get('id')
        card_name = card_data.get('name', 'Unknown')
        
        print("=" * 70)
        print(f"Creating Card: {card_name} (ID: {card_id})")
        print("=" * 70)
        
        # Step 1: Add to database
        print(f"\n[1/3] Adding to database...")
        if not self.db_manager.add_card(card_data):
            print(f"✗ Failed to add card to database")
            return False
        
        # Step 2: Generate script (if applicable)
        if generate_script:
            print(f"\n[2/3] Generating Lua script...")
            if not self.script_generator.generate_and_save(card_data, effect_pattern, 
                                                           effect_params, overwrite):
                print(f"⚠ Warning: Failed to generate script (card is still in database)")
        else:
            print(f"\n[2/3] Skipping script generation")
        
        # Step 3: Download or copy image (if URL/path provided)
        if image_url:
            print(f"\n[3/3] Processing card image...")
            # Check if it's a local file path or URL
            is_local_file = not image_url.lower().startswith(('http://', 'https://'))
            
            if is_local_file:
                # Local file - copy it
                result = self.image_downloader.copy_local_image(image_url, card_id, 
                                                                resize=True, overwrite=overwrite)
            else:
                # URL - download it
                result = self.image_downloader.download_with_retry(image_url, card_id, 
                                                                   resize=True, overwrite=overwrite)
            
            if not result:
                print(f"⚠ Warning: Failed to process image (card is still in database)")
        else:
            print(f"\n[3/3] No image URL provided, skipping image download")
            print(f"    You can manually place the image at: pics/{card_id}.jpg")
        
        print("\n" + "=" * 70)
        print(f"✓ Card creation complete: {card_name}")
        print("=" * 70)
        return True
    
    def create_monster(self, card_id: int, name: str, desc: str, atk: int, def_val: int,
                      level: int, attribute: int, race: int, 
                      is_normal: bool = True, image_url: Optional[str] = None,
                      effect_pattern: Optional[str] = None, effect_params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Create a monster card
        
        Args:
            card_id: Card ID
            name: Card name
            desc: Card description
            atk: Attack points
            def_val: Defense points
            level: Level/Rank
            attribute: Attribute value
            race: Race value
            is_normal: Whether it's a normal monster (vs effect monster)
            image_url: Image URL
            effect_pattern: Effect pattern for effect monsters
            effect_params: Effect parameters
        
        Returns:
            True if successful
        """
        card_type = TYPE_MONSTER_NORMAL if is_normal else TYPE_MONSTER_EFFECT
        
        card_data = {
            'id': card_id,
            'name': name,
            'desc': desc,
            'type': card_type,
            'ot': SCOPE_OCG_TCG,
            'atk': atk,
            'def': def_val,
            'level': level,
            'attribute': attribute,
            'race': race
        }
        
        return self.create_card(card_data, image_url, effect_pattern, effect_params)
    
    def create_spell(self, card_id: int, name: str, desc: str,
                    spell_type: str = 'normal', image_url: Optional[str] = None,
                    effect_pattern: Optional[str] = None, effect_params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Create a spell card
        
        Args:
            card_id: Card ID
            name: Card name
            desc: Card description/effect
            spell_type: Type of spell ('normal', 'quickplay', 'continuous', 'equip', 'field')
            image_url: Image URL
            effect_pattern: Effect pattern
            effect_params: Effect parameters
        
        Returns:
            True if successful
        """
        spell_types = {
            'normal': TYPE_SPELL,
            'quickplay': TYPE_SPELL_QUICKPLAY,
            'continuous': TYPE_SPELL_CONTINUOUS,
            'equip': TYPE_SPELL_EQUIP,
            'field': TYPE_SPELL_FIELD
        }
        
        card_type = spell_types.get(spell_type.lower(), TYPE_SPELL)
        
        card_data = {
            'id': card_id,
            'name': name,
            'desc': desc,
            'type': card_type,
            'ot': SCOPE_OCG_TCG
        }
        
        return self.create_card(card_data, image_url, effect_pattern, effect_params)
    
    def create_trap(self, card_id: int, name: str, desc: str,
                   trap_type: str = 'normal', image_url: Optional[str] = None,
                   effect_pattern: Optional[str] = None, effect_params: Optional[Dict[str, Any]] = None) -> bool:
        """
        Create a trap card
        
        Args:
            card_id: Card ID
            name: Card name
            desc: Card description/effect
            trap_type: Type of trap ('normal', 'continuous', 'counter')
            image_url: Image URL
            effect_pattern: Effect pattern
            effect_params: Effect parameters
        
        Returns:
            True if successful
        """
        trap_types = {
            'normal': TYPE_TRAP,
            'continuous': TYPE_TRAP_CONTINUOUS,
            'counter': TYPE_TRAP_COUNTER
        }
        
        card_type = trap_types.get(trap_type.lower(), TYPE_TRAP)
        
        card_data = {
            'id': card_id,
            'name': name,
            'desc': desc,
            'type': card_type,
            'ot': SCOPE_OCG_TCG
        }
        
        return self.create_card(card_data, image_url, effect_pattern, effect_params)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Yu-Gi-Oh! Card Creator - Create custom cards with database entries, scripts, and images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a spell card that heals 500 LP
  python card_creator.py --id 10000100 --name "Healing Light" --type spell \\
    --desc "Restore 500 Life Points" --effect recover_lp --effect-amount 500 \\
    --image-url "https://example.com/card.jpg"
  
  # Create a normal monster
  python card_creator.py --id 10000101 --name "Fire Dragon" --type monster \\
    --desc "A dragon wreathed in flames" --atk 2000 --def 1500 --level 4 \\
    --attribute FIRE --race Dragon --image-url "https://example.com/dragon.jpg"
  
  # Create an effect monster
  python card_creator.py --id 10000102 --name "Mystic Warrior" --type monster \\
    --desc "When summoned: Draw 1 card" --atk 1800 --def 1200 --level 4 \\
    --attribute LIGHT --race Warrior --effect-monster
        """
    )
    
    # Basic card information
    parser.add_argument('--id', type=int, required=True, help='Card ID (e.g., 10000100)')
    parser.add_argument('--name', type=str, required=True, help='Card name')
    parser.add_argument('--desc', '--description', type=str, required=True, help='Card description/effect')
    parser.add_argument('--type', type=str, required=True, choices=['monster', 'spell', 'trap'],
                       help='Card type')
    
    # Monster-specific
    parser.add_argument('--atk', type=int, help='Attack points (monsters only)')
    parser.add_argument('--def', type=int, help='Defense points (monsters only)')
    parser.add_argument('--level', type=int, help='Level/Rank (monsters only)')
    parser.add_argument('--attribute', type=str, help='Attribute (EARTH, WATER, FIRE, WIND, LIGHT, DARK, DIVINE)')
    parser.add_argument('--race', type=str, help='Race/Type (Dragon, Warrior, Spellcaster, etc.)')
    parser.add_argument('--effect-monster', action='store_true', help='Create effect monster (default is normal)')
    
    # Spell/Trap-specific
    parser.add_argument('--spell-type', type=str, choices=['normal', 'quickplay', 'continuous', 'equip', 'field'],
                       default='normal', help='Spell card type')
    parser.add_argument('--trap-type', type=str, choices=['normal', 'continuous', 'counter'],
                       default='normal', help='Trap card type')
    
    # Effect pattern
    parser.add_argument('--effect', type=str, help='Effect pattern (recover_lp, damage, draw, atk_boost, def_boost)')
    parser.add_argument('--effect-amount', type=int, help='Amount for effect (e.g., LP to recover, cards to draw)')
    
    # Image
    parser.add_argument('--image-url', type=str, help='URL to download card image from')
    
    # Options
    parser.add_argument('--db', type=str, help='Database path (default: ../expansions/cards.cdb)')
    parser.add_argument('--script-dir', type=str, help='Script directory (default: ../script)')
    parser.add_argument('--pics-dir', type=str, help='Images directory (default: ../pics)')
    parser.add_argument('--no-script', action='store_true', help='Skip Lua script generation')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files')
    
    # List options
    parser.add_argument('--list-effects', action='store_true', help='List available effect patterns')
    parser.add_argument('--list-attributes', action='store_true', help='List available attributes')
    parser.add_argument('--list-races', action='store_true', help='List available races')
    
    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Handle list commands
    if args.list_effects:
        print("Available Effect Patterns:")
        generator = ScriptGenerator()
        for name, desc in generator.list_available_patterns().items():
            print(f"  {name:15} - {desc}")
        return 0
    
    if args.list_attributes:
        print("Available Attributes:")
        for value, name in ATTRIBUTE_NAMES.items():
            print(f"  {name}")
        return 0
    
    if args.list_races:
        print("Available Races:")
        for value, name in RACE_NAMES.items():
            print(f"  {name}")
        return 0
    
    # Create card creator
    creator = CardCreator(
        db_path=args.db,
        script_dir=args.script_dir,
        pics_dir=args.pics_dir
    )
    
    # Prepare effect parameters
    effect_params = None
    if args.effect and args.effect_amount is not None:
        effect_params = {'amount': args.effect_amount}
    
    # Create card based on type
    success = False
    
    if args.type == 'monster':
        # Validate monster parameters
        def_val = getattr(args, 'def')
        if args.atk is None or def_val is None or args.level is None:
            print("Error: Monsters require --atk, --def, and --level")
            return 1
        if args.attribute is None or args.race is None:
            print("Error: Monsters require --attribute and --race")
            return 1
        
        # Parse attribute and race
        attribute = parse_attribute(args.attribute)
        race = parse_race(args.race)
        
        if attribute is None:
            print(f"Error: Invalid attribute '{args.attribute}'")
            print("Use --list-attributes to see valid attributes")
            return 1
        if race is None:
            print(f"Error: Invalid race '{args.race}'")
            print("Use --list-races to see valid races")
            return 1
        
        success = creator.create_monster(
            card_id=args.id,
            name=args.name,
            desc=args.desc,
            atk=args.atk,
            def_val=def_val,
            level=args.level,
            attribute=attribute,
            race=race,
            is_normal=not args.effect_monster,
            image_url=args.image_url,
            effect_pattern=args.effect,
            effect_params=effect_params
        )
    
    elif args.type == 'spell':
        success = creator.create_spell(
            card_id=args.id,
            name=args.name,
            desc=args.desc,
            spell_type=args.spell_type,
            image_url=args.image_url,
            effect_pattern=args.effect,
            effect_params=effect_params
        )
    
    elif args.type == 'trap':
        success = creator.create_trap(
            card_id=args.id,
            name=args.name,
            desc=args.desc,
            trap_type=args.trap_type,
            image_url=args.image_url,
            effect_pattern=args.effect,
            effect_params=effect_params
        )
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

