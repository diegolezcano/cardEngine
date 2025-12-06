# Card Cleanup Utility Guide

## Overview
The `cleanup_cards.py` script helps you identify and remove cards from the database that don't have corresponding image files in the `pics` folder.

## Usage

### 1. Analyze Only (Safe - No Deletions)
Check which cards don't have images without deleting anything:

```bash
cd createCards
py cleanup_cards.py --analyze
```

or

```bash
py cleanup_cards.py -a
```

### 2. Dry Run (Preview Deletions)
See what would be deleted without actually deleting:

```bash
py cleanup_cards.py --dry-run
```

or

```bash
py cleanup_cards.py -d
```

### 3. Delete Cards Without Images
Actually delete cards that don't have images (requires confirmation):

```bash
py cleanup_cards.py
```

**⚠️ Warning:** This will permanently delete cards from the database. Make sure you have a backup!

## Python API Usage

You can also import and use the functions in your own scripts:

```python
from cleanup_cards import analyze_cards_without_images, delete_cards_without_images

# Analyze cards
missing, with_images = analyze_cards_without_images()
print(f"Found {len(missing)} cards without images")

# Delete cards (dry run first!)
deleted = delete_cards_without_images(dry_run=True)  # Preview
deleted = delete_cards_without_images(dry_run=False)  # Actually delete
```

## Customization

You can customize the ID range to check:

```python
from cleanup_cards import delete_cards_without_images

# Check only cards in a specific range
delete_cards_without_images(
    min_id=10000001,
    max_id=10000050,
    dry_run=True
)
```

## What Gets Checked

The script checks for image files in these formats:
- `{CARD_ID}.jpg`
- `{CARD_ID}.png`

If neither file exists in the `pics` folder, the card is considered to be missing an image.

## Safety Features

1. **Analysis Mode**: Always analyze first before deleting
2. **Dry Run**: Preview deletions without making changes
3. **Confirmation**: Requires typing "yes" to confirm deletion
4. **Detailed Logging**: Shows exactly what's being deleted

## Example Output

```
======================================================================
CARD IMAGE ANALYSIS REPORT
======================================================================
Total custom cards in database: 25
Cards WITH images: 21
Cards WITHOUT images: 4
======================================================================

📋 CARDS WITHOUT IMAGES (candidates for deletion):
----------------------------------------------------------------------
  ID: 10000022 | Name: Test Card 1
  ID: 10000023 | Name: Test Card 2
  ID: 10000024 | Name: Test Card 3
  ID: 10000025 | Name: Test Card 4

======================================================================
⚠️  SUMMARY: 4 cards would be deleted
======================================================================
```

