"""
Card Cleanup Utility
Analyzes and deletes cards from the database that don't have corresponding images
"""

from database_manager import DatabaseManager
import os
from typing import List, Tuple


def analyze_cards_without_images(db_path: str = '../expansions/cards.cdb', 
                                  pics_dir: str = '../pics',
                                  min_id: int = 10000001,
                                  max_id: int = 19999999) -> Tuple[List[Tuple[int, str]], List[Tuple[int, str]]]:
    """
    Analyze which cards in the database don't have images
    
    Args:
        db_path: Path to the database file
        pics_dir: Path to the pictures directory
        min_id: Minimum card ID to check
        max_id: Maximum card ID to check
    
    Returns:
        Tuple of (cards_without_images, cards_with_images)
        Each is a list of tuples (card_id, card_name)
    """
    db = DatabaseManager(db_path)
    
    # Get all custom cards from database
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT datas.id, texts.name 
        FROM datas 
        LEFT JOIN texts ON datas.id = texts.id 
        WHERE datas.id >= ? AND datas.id <= ? 
        ORDER BY datas.id
    """, (min_id, max_id))
    all_cards = cursor.fetchall()
    conn.close()
    
    missing_images = []
    cards_with_images = []
    
    for card_id, card_name in all_cards:
        if card_name is None:
            card_name = f"Unknown (ID: {card_id})"
        
        jpg_path = os.path.join(pics_dir, f'{card_id}.jpg')
        png_path = os.path.join(pics_dir, f'{card_id}.png')
        
        if os.path.exists(jpg_path) or os.path.exists(png_path):
            cards_with_images.append((card_id, card_name))
        else:
            missing_images.append((card_id, card_name))
    
    return missing_images, cards_with_images


def print_analysis_report(missing_images: List[Tuple[int, str]], 
                         cards_with_images: List[Tuple[int, str]]):
    """Print a formatted report of the analysis"""
    total = len(missing_images) + len(cards_with_images)
    
    print("=" * 70)
    print("CARD IMAGE ANALYSIS REPORT")
    print("=" * 70)
    print(f"Total custom cards in database: {total}")
    print(f"Cards WITH images: {len(cards_with_images)}")
    print(f"Cards WITHOUT images: {len(missing_images)}")
    print("=" * 70)
    
    if missing_images:
        print("\n📋 CARDS WITHOUT IMAGES (candidates for deletion):")
        print("-" * 70)
        for card_id, card_name in missing_images:
            print(f"  ID: {card_id:8d} | Name: {card_name}")
        
        print("\n" + "=" * 70)
        print(f"⚠️  SUMMARY: {len(missing_images)} cards would be deleted")
        print("=" * 70)
    else:
        print("\n✅ All cards have images! No cards to delete.")


def delete_cards_without_images(db_path: str = '../expansions/cards.cdb',
                                pics_dir: str = '../pics',
                                min_id: int = 10000001,
                                max_id: int = 19999999,
                                dry_run: bool = False) -> int:
    """
    Delete cards from database that don't have images
    
    Args:
        db_path: Path to the database file
        pics_dir: Path to the pictures directory
        min_id: Minimum card ID to check
        max_id: Maximum card ID to check
        dry_run: If True, only report what would be deleted without actually deleting
    
    Returns:
        Number of cards deleted (or would be deleted if dry_run=True)
    """
    missing_images, cards_with_images = analyze_cards_without_images(
        db_path, pics_dir, min_id, max_id
    )
    
    if not missing_images:
        print("✅ No cards to delete - all cards have images!")
        return 0
    
    # Print report
    print_analysis_report(missing_images, cards_with_images)
    
    if dry_run:
        print("\n🔍 DRY RUN MODE - No cards will be deleted")
        print(f"   Would delete {len(missing_images)} cards")
        return len(missing_images)
    
    # Confirm deletion
    print(f"\n⚠️  WARNING: About to delete {len(missing_images)} cards from the database!")
    response = input("Are you sure you want to proceed? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("❌ Deletion cancelled.")
        return 0
    
    # Delete cards
    db = DatabaseManager(db_path)
    deleted_count = 0
    failed_count = 0
    
    print("\n🗑️  Deleting cards...")
    for card_id, card_name in missing_images:
        if db.delete_card(card_id):
            deleted_count += 1
            print(f"  ✓ Deleted: {card_name} (ID: {card_id})")
        else:
            failed_count += 1
            print(f"  ✗ Failed to delete: {card_name} (ID: {card_id})")
    
    print("\n" + "=" * 70)
    print(f"✅ Deletion complete!")
    print(f"   Successfully deleted: {deleted_count} cards")
    if failed_count > 0:
        print(f"   Failed to delete: {failed_count} cards")
    print("=" * 70)
    
    return deleted_count


def main():
    """Main function for command-line usage"""
    import sys
    
    # Check for command-line arguments
    dry_run = '--dry-run' in sys.argv or '-d' in sys.argv
    analyze_only = '--analyze' in sys.argv or '-a' in sys.argv
    
    if analyze_only:
        # Just analyze and report
        missing_images, cards_with_images = analyze_cards_without_images()
        print_analysis_report(missing_images, cards_with_images)
    else:
        # Delete cards (with dry-run option)
        delete_cards_without_images(dry_run=dry_run)


if __name__ == "__main__":
    main()

