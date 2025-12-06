# Yu-Gi-Oh! Card Creator System

A comprehensive toolkit for creating custom Yu-Gi-Oh! cards with automated database management, Lua script generation, and image downloading.

## Features

- ✅ **Complete Card Creation**: Database entries, Lua scripts, and images all in one command
- ✅ **Automatic Image Downloading**: Download and resize card images from URLs
- ✅ **Template-Based Scripts**: Generate Lua scripts with common effect patterns
- ✅ **Support for All Card Types**: Monsters, Spells, and Traps with full customization
- ✅ **Database Management**: Add, update, delete, and query cards
- ✅ **ID Validation**: Prevent duplicate cards and find next available IDs

## Quick Start

### Prerequisites

1. Python 3.7 or higher
2. Required Python packages (see Installation)

### Installation

```bash
# Navigate to the createCards directory
cd createCards

# Install required packages
pip install -r requirements.txt
```

### Basic Usage

#### Create a Spell Card

```bash
python card_creator.py --id 10000100 --name "Healing Light" --type spell \
  --desc "Restore 500 Life Points" --effect recover_lp --effect-amount 500 \
  --image-url "https://example.com/healing-light.jpg"
```

#### Create a Monster Card

```bash
python card_creator.py --id 10000101 --name "Fire Dragon" --type monster \
  --desc "A dragon wreathed in flames" --atk 2000 --def 1500 --level 4 \
  --attribute FIRE --race Dragon \
  --image-url "https://example.com/fire-dragon.jpg"
```

#### Create an Effect Monster

```bash
python card_creator.py --id 10000102 --name "Mystic Warrior" --type monster \
  --desc "When summoned: Draw 1 card" --atk 1800 --def 1200 --level 4 \
  --attribute LIGHT --race Warrior --effect-monster
```

## Card ID Conventions

- **10000000-19999999**: Custom spell/trap cards
- **20000000-29999999**: Custom monster cards
- **30000000-39999999**: Special custom cards

For this project, start with IDs **10000100** and above to avoid conflicts with existing cards.

## Available Effect Patterns

Use `--effect` with one of these patterns and `--effect-amount` to specify the value:

| Pattern | Description | Example |
|---------|-------------|---------|
| `recover_lp` | Recover Life Points | `--effect recover_lp --effect-amount 500` |
| `damage` | Inflict damage to opponent | `--effect damage --effect-amount 500` |
| `draw` | Draw cards | `--effect draw --effect-amount 2` |
| `atk_boost` | Boost ATK of all your monsters | `--effect atk_boost --effect-amount 500` |
| `def_boost` | Boost DEF of all your monsters | `--effect def_boost --effect-amount 500` |

List all available effects:
```bash
python card_creator.py --list-effects
```

## Attributes and Races

### Attributes (for Monsters)

- EARTH, WATER, FIRE, WIND, LIGHT, DARK, DIVINE

List all attributes:
```bash
python card_creator.py --list-attributes
```

### Races (for Monsters)

- Warrior, Spellcaster, Fairy, Fiend, Zombie, Machine, Aqua, Pyro, Rock, Winged Beast
- Plant, Insect, Thunder, Dragon, Beast, Beast-Warrior, Dinosaur, Fish
- Sea Serpent, Reptile, Psychic, Divine-Beast, Creator God, Wyrm, Cyberse, Illusion

List all races:
```bash
python card_creator.py --list-races
```

## Card Types

### Spell Cards

- **Normal** (default): `--spell-type normal`
- **Quick-Play**: `--spell-type quickplay`
- **Continuous**: `--spell-type continuous`
- **Equip**: `--spell-type equip`
- **Field**: `--spell-type field`

### Trap Cards

- **Normal** (default): `--trap-type normal`
- **Continuous**: `--trap-type continuous`
- **Counter**: `--trap-type counter`

### Monster Cards

- **Normal Monster** (default): No additional flags
- **Effect Monster**: Add `--effect-monster` flag

## Command Line Options

### Required Arguments

- `--id` - Card ID (8-digit number, e.g., 10000100)
- `--name` - Card name
- `--desc` - Card description/effect text
- `--type` - Card type: `monster`, `spell`, or `trap`

### Monster-Specific Arguments

- `--atk` - Attack points
- `--def` - Defense points
- `--level` - Level/Rank (1-12)
- `--attribute` - Attribute (EARTH, WATER, FIRE, etc.)
- `--race` - Race/Type (Dragon, Warrior, etc.)
- `--effect-monster` - Make it an effect monster (default is normal)

### Spell/Trap Arguments

- `--spell-type` - Spell type (normal, quickplay, continuous, equip, field)
- `--trap-type` - Trap type (normal, continuous, counter)

### Effect Arguments

- `--effect` - Effect pattern name
- `--effect-amount` - Amount/value for the effect

### Image Arguments

- `--image-url` - URL to download card image from

### Optional Arguments

- `--db` - Database path (default: `../expansions/cards.cdb`)
- `--script-dir` - Script directory (default: `../script`)
- `--pics-dir` - Images directory (default: `../pics`)
- `--no-script` - Skip Lua script generation
- `--overwrite` - Overwrite existing files

## File Structure

```
createCards/
├── card_creator.py         # Main script
├── database_manager.py     # Database operations
├── script_generator.py     # Lua script generation
├── image_downloader.py     # Image downloading
├── constants.py            # Game constants
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── templates/             # Lua script templates
    ├── monster_normal.lua
    ├── monster_effect.lua
    ├── spell_basic.lua
    ├── spell_quickplay.lua
    ├── spell_continuous.lua
    ├── trap_normal.lua
    └── trap_continuous.lua
```

## Database Schema

The card database (`cards.cdb`) contains two main tables:

### datas Table
- `id` - Card ID (primary key)
- `ot` - Scope/legality (OCG/TCG/Custom)
- `alias` - Alias ID
- `setcode` - Set codes
- `type` - Card type flags
- `atk` - Attack points
- `def` - Defense/Link markers
- `level` - Level/Rank/Scales
- `race` - Monster type/race
- `attribute` - Attribute
- `category` - Effect categories

### texts Table
- `id` - Card ID (primary key)
- `name` - Card name
- `desc` - Card description
- `str1-str16` - Additional effect strings

## Advanced Usage

### Using the Python API

```python
from card_creator import CardCreator
from constants import *

# Initialize
creator = CardCreator()

# Create a spell card
creator.create_spell(
    card_id=10000100,
    name="Mystical Heal",
    desc="Restore 1000 Life Points",
    image_url="https://example.com/card.jpg",
    effect_pattern="recover_lp",
    effect_params={'amount': 1000}
)

# Create a monster
creator.create_monster(
    card_id=10000101,
    name="Thunder Dragon",
    desc="A legendary dragon of thunder",
    atk=2500,
    def_val=2000,
    level=7,
    attribute=ATTRIBUTE_LIGHT,
    race=RACE_DRAGON,
    is_normal=True,
    image_url="https://example.com/dragon.jpg"
)
```

### Database Management

```python
from database_manager import DatabaseManager

db = DatabaseManager("../expansions/cards.cdb")

# Get next available ID
next_id = db.get_next_available_id(10000100)
print(f"Next available ID: {next_id}")

# List custom cards
cards = db.list_custom_cards(min_id=10000000, max_id=10999999)
for card in cards:
    print(f"{card['id']}: {card['name']}")

# Check if card exists
if db.card_exists(10000100):
    print("Card exists!")
```

### Image Management

```python
from image_downloader import ImageDownloader

downloader = ImageDownloader("../pics")

# Download and resize image
downloader.download_image(
    url="https://example.com/card.jpg",
    card_id=10000100,
    resize=True
)

# Verify image exists
exists, info = downloader.verify_image(10000100)
print(info)
```

## Troubleshooting

### Database Not Found

**Error**: `Database file not found: ../expansions/cards.cdb`

**Solution**: Make sure you're running the script from the `createCards` directory, or specify the database path:
```bash
python card_creator.py --db "C:\path\to\cards.cdb" ...
```

### Image Download Failed

**Error**: Failed to download image

**Solutions**:
- Check that the URL is valid and accessible
- Verify your internet connection
- Try a different image URL
- Manually place the image in `pics/{card_id}.jpg`

### Script Generation Failed

**Error**: Template not found

**Solution**: Ensure the `templates/` directory exists with all template files

### Pillow Not Installed

**Warning**: Image resizing disabled

**Solution**: Install Pillow:
```bash
pip install Pillow
```

### Card Already Exists

**Error**: Card with ID already exists

**Solution**: 
- Use a different card ID
- Use `--overwrite` to replace the existing card
- Find next available ID with database manager

## Examples

### Example 1: Simple Heal Spell

```bash
python card_creator.py \
  --id 10000100 \
  --name "Minor Heal" \
  --type spell \
  --desc "Restore 500 Life Points" \
  --effect recover_lp \
  --effect-amount 500 \
  --image-url "https://example.com/heal.jpg"
```

### Example 2: Powerful Dragon

```bash
python card_creator.py \
  --id 10000101 \
  --name "Azure-Eyes Ultimate Dragon" \
  --type monster \
  --desc "A legendary dragon with eyes of azure flame" \
  --atk 3000 \
  --def 2500 \
  --level 8 \
  --attribute LIGHT \
  --race Dragon \
  --image-url "https://example.com/dragon.jpg"
```

### Example 3: Draw Spell

```bash
python card_creator.py \
  --id 10000102 \
  --name "Mystic Draw" \
  --type spell \
  --desc "Draw 2 cards" \
  --effect draw \
  --effect-amount 2 \
  --image-url "https://example.com/draw.jpg"
```

### Example 4: Continuous Trap

```bash
python card_creator.py \
  --id 10000103 \
  --name "Eternal Protection" \
  --type trap \
  --trap-type continuous \
  --desc "Your monsters cannot be destroyed by battle" \
  --image-url "https://example.com/protection.jpg"
```

## Tips

1. **Start with simple cards**: Begin with basic spell cards using effect patterns
2. **Use consistent ID ranges**: Keep your cards organized by ID ranges
3. **Test in-game**: Always test your cards in the game after creation
4. **Backup your database**: Keep backups of `cards.cdb` before making changes
5. **Use high-quality images**: Recommended size is 177x254 pixels
6. **Check for conflicts**: Ensure your IDs don't conflict with official cards

## Support

For issues or questions:
1. Check this README first
2. Review the Troubleshooting section
3. Examine the example scripts in the edopro source
4. Check the EDOPro documentation

## License

This tool is designed for use with EDOPro and follows the same licensing as the Yu-Gi-Oh! game engine.

