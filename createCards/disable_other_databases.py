"""
Disable other database repositories in EDOPro
This will make EDOPro only load cards from expansions/cards.cdb (your custom cards)
"""

import json
import os
import shutil
from datetime import datetime

def backup_config():
    """Create a backup of the current config"""
    config_path = '../config/configs.json'
    backup_path = f'../config/configs.json.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    
    if os.path.exists(config_path):
        shutil.copy2(config_path, backup_path)
        print(f"✓ Backup created: {backup_path}")
        return backup_path
    return None

def disable_other_databases():
    """Disable all repositories except custom cards"""
    config_path = '../config/configs.json'
    
    # Backup first
    backup_path = backup_config()
    
    # Read current config
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Disable all repositories
    disabled_count = 0
    for repo in config.get('repos', []):
        if repo.get('should_read', True):
            repo['should_read'] = False
            disabled_count += 1
            print(f"  Disabled: {repo.get('repo_name', 'Unknown')}")
    
    # Write updated config
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent='\t', ensure_ascii=False)
    
    print(f"\n✓ Disabled {disabled_count} repositories")
    print(f"✓ EDOPro will now only load cards from expansions/cards.cdb")
    print(f"\n⚠️  IMPORTANT: Restart EDOPro for changes to take effect!")
    print(f"   Backup saved at: {backup_path}")
    
    return True

def enable_other_databases():
    """Re-enable all repositories"""
    config_path = '../config/configs.json'
    
    # Read current config
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Enable all repositories
    enabled_count = 0
    for repo in config.get('repos', []):
        if not repo.get('should_read', False):
            repo['should_read'] = True
            enabled_count += 1
            print(f"  Enabled: {repo.get('repo_name', 'Unknown')}")
    
    # Write updated config
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent='\t', ensure_ascii=False)
    
    print(f"\n✓ Re-enabled {enabled_count} repositories")
    print(f"⚠️  IMPORTANT: Restart EDOPro for changes to take effect!")
    
    return True

def show_status():
    """Show current repository status"""
    config_path = '../config/configs.json'
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("=" * 70)
    print("CURRENT REPOSITORY STATUS")
    print("=" * 70)
    
    for repo in config.get('repos', []):
        status = "ENABLED" if repo.get('should_read', True) else "DISABLED"
        name = repo.get('repo_name', 'Unknown')
        path = repo.get('repo_path', 'Unknown')
        print(f"  {name:30s} | {status:10s} | {path}")
    
    print("=" * 70)
    print("\nNote: Your custom cards are in expansions/cards.cdb (always loaded)")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'disable':
            print("Disabling other databases...")
            disable_other_databases()
        elif sys.argv[1] == 'enable':
            print("Re-enabling other databases...")
            enable_other_databases()
        elif sys.argv[1] == 'status':
            show_status()
        else:
            print("Usage: py disable_other_databases.py [disable|enable|status]")
    else:
        print("=" * 70)
        print("EDOPro Database Control")
        print("=" * 70)
        print("\nThis script controls which card databases EDOPro loads.")
        print("\nOptions:")
        print("  disable  - Disable all repositories (only custom cards)")
        print("  enable   - Re-enable all repositories (default)")
        print("  status   - Show current status")
        print("\nUsage:")
        print("  py disable_other_databases.py disable")
        print("  py disable_other_databases.py enable")
        print("  py disable_other_databases.py status")
        print("\n⚠️  WARNING: Always restart EDOPro after making changes!")

