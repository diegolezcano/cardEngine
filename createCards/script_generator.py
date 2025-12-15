"""
Lua Script Generator for Yu-Gi-Oh! Cards
Generates card scripts from templates based on card type and effects
"""

import os
from typing import Dict, Any, Optional
from constants import *


class ScriptGenerator:
    """Generates Lua scripts for Yu-Gi-Oh! cards"""
    
    # Common effect patterns
    EFFECT_PATTERNS = {
        'recover_lp': {
            'operation': 'Duel.Recover(tp,{amount},REASON_EFFECT)',
            'properties': 'e1:SetProperty(EFFECT_FLAG_PLAYER_TARGET)',
            'description': 'Recover {amount} Life Points'
        },
        'damage': {
            'operation': 'Duel.Damage(1-tp,{amount},REASON_EFFECT)',
            'properties': 'e1:SetProperty(EFFECT_FLAG_PLAYER_TARGET)',
            'description': 'Inflict {amount} damage to opponent'
        },
        'draw': {
            'operation': 'Duel.Draw(tp,{amount},REASON_EFFECT)',
            'properties': '',
            'description': 'Draw {amount} card(s)'
        },
        'atk_boost': {
            'code': 'e1:SetCode(EFFECT_UPDATE_ATTACK)',
            'properties': 'e1:SetTargetRange(LOCATION_MZONE,0)\n\te1:SetValue({amount})',
            'description': 'All your monsters gain {amount} ATK'
        },
        'def_boost': {
            'code': 'e1:SetCode(EFFECT_UPDATE_DEFENSE)',
            'properties': 'e1:SetTargetRange(LOCATION_MZONE,0)\n\te1:SetValue({amount})',
            'description': 'All your monsters gain {amount} DEF'
        }
    }
    
    def __init__(self, templates_dir: str = None, output_dir: str = None):
        """
        Initialize script generator
        
        Args:
            templates_dir: Directory containing template files
            output_dir: Directory where scripts should be saved
        """
        if templates_dir is None:
            templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        if output_dir is None:
            output_dir = "../script"
        
        self.templates_dir = templates_dir
        self.output_dir = output_dir
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created directory: {self.output_dir}")
    
    def _load_template(self, template_name: str) -> Optional[str]:
        """
        Load a template file
        
        Args:
            template_name: Name of template file (without .lua extension)
        
        Returns:
            Template content as string or None if not found
        """
        template_path = os.path.join(self.templates_dir, f"{template_name}.lua")
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: Template not found: {template_path}")
            return None
        except Exception as e:
            print(f"Error loading template: {e}")
            return None
    
    def _get_template_name(self, card_type: int) -> str:
        """
        Determine which template to use based on card type
        
        Args:
            card_type: Card type flags
        
        Returns:
            Template name
        """
        if is_monster(card_type):
            if card_type & TYPE_NORMAL:
                return 'monster_normal'
            else:
                return 'monster_effect'
        elif is_spell(card_type):
            if card_type & TYPE_CONTINUOUS:
                return 'spell_continuous'
            elif card_type & TYPE_QUICKPLAY:
                return 'spell_quickplay'
            else:
                return 'spell_basic'
        elif is_trap(card_type):
            if card_type & TYPE_COUNTER:
                return 'trap_counter'
            elif card_type & TYPE_CONTINUOUS:
                return 'trap_continuous'
            else:
                return 'trap_normal'
        
        return 'spell_basic'  # Default
    
    def generate_script(self, card_data: Dict[str, Any], effect_pattern: Optional[str] = None,
                       effect_params: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Generate a Lua script for a card
        
        Args:
            card_data: Dictionary containing card information (must include 'id', 'name', 'type')
            effect_pattern: Name of effect pattern to use (e.g., 'recover_lp', 'draw')
            effect_params: Parameters for the effect pattern (e.g., {'amount': 500})
        
        Returns:
            Generated script content or None if failed
        """
        # Validate required fields
        if 'id' not in card_data or 'name' not in card_data or 'type' not in card_data:
            print("Error: card_data must include 'id', 'name', and 'type'")
            return None
        
        card_id = card_data['id']
        card_name = card_data['name']
        card_type = card_data['type']
        effect_desc = card_data.get('desc', '')
        
        # Get appropriate template
        template_name = self._get_template_name(card_type)
        template = self._load_template(template_name)
        
        if not template:
            return None
        
        # Replace basic placeholders
        script = template.replace('{CARD_ID}', str(card_id))
        script = script.replace('{CARD_NAME}', card_name)
        script = script.replace('{EFFECT_DESC}', effect_desc)
        
        # Apply effect pattern if specified
        if effect_pattern and effect_pattern in self.EFFECT_PATTERNS:
            pattern = self.EFFECT_PATTERNS[effect_pattern]
            params = effect_params or {}
            
            # Replace operation
            if 'operation' in pattern:
                operation = pattern['operation']
                for key, value in params.items():
                    operation = operation.replace(f'{{{key}}}', str(value))
                script = script.replace('{EFFECT_OPERATION}', operation)
            
            # Replace properties
            if 'properties' in pattern:
                properties = pattern['properties']
                for key, value in params.items():
                    properties = properties.replace(f'{{{key}}}', str(value))
                script = script.replace('{ADDITIONAL_PROPERTIES}', properties)
            
            # Replace effect code
            if 'code' in pattern:
                code = pattern['code']
                for key, value in params.items():
                    code = code.replace(f'{{{key}}}', str(value))
                script = script.replace('{EFFECT_CODE}', code)
        else:
            # Remove placeholder tags if no pattern specified
            script = script.replace('{EFFECT_OPERATION}', '-- TODO: Add effect operation here')
            script = script.replace('{ADDITIONAL_PROPERTIES}', '')
            script = script.replace('{EFFECT_CODE}', '-- TODO: Add effect code here')
            script = script.replace('{EFFECT_TYPE}', 'Custom Effect')
        
        return script
    
    def save_script(self, card_id: int, script_content: str, overwrite: bool = False) -> bool:
        """
        Save a Lua script to file
        
        Args:
            card_id: Card ID (used for filename)
            script_content: Script content to save
            overwrite: Whether to overwrite existing file
        
        Returns:
            True if successful, False otherwise
        """
        filename = f"c{card_id}.lua"
        filepath = os.path.join(self.output_dir, filename)
        
        # Check if file exists
        if os.path.exists(filepath) and not overwrite:
            print(f"Warning: Script file already exists: {filepath}")
            print(f"Use overwrite=True to replace it")
            return False
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(script_content)
            print(f"✓ Script saved: {filepath}")
            return True
        except Exception as e:
            print(f"✗ Error saving script: {e}")
            return False
    
    def generate_and_save(self, card_data: Dict[str, Any], effect_pattern: Optional[str] = None,
                         effect_params: Optional[Dict[str, Any]] = None, 
                         overwrite: bool = False) -> bool:
        """
        Generate and save a Lua script in one step
        
        Args:
            card_data: Card information
            effect_pattern: Effect pattern name
            effect_params: Effect parameters
            overwrite: Whether to overwrite existing files
        
        Returns:
            True if successful, False otherwise
        """
        script = self.generate_script(card_data, effect_pattern, effect_params)
        
        if not script:
            return False
        
        return self.save_script(card_data['id'], script, overwrite)
    
    def delete_script(self, card_id: int) -> bool:
        """
        Delete a script file
        
        Args:
            card_id: Card ID whose script should be deleted
        
        Returns:
            True if deleted, False if not found or error
        """
        filename = f"c{card_id}.lua"
        filepath = os.path.join(self.output_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Script file not found: {filepath}")
            return False
        
        try:
            os.remove(filepath)
            print(f"✓ Deleted script: {filepath}")
            return True
        except Exception as e:
            print(f"✗ Error deleting script: {e}")
            return False
    
    def list_available_patterns(self) -> Dict[str, str]:
        """
        Get list of available effect patterns with descriptions
        
        Returns:
            Dictionary of pattern names and descriptions
        """
        patterns = {}
        for name, pattern in self.EFFECT_PATTERNS.items():
            patterns[name] = pattern.get('description', name)
        return patterns


def create_card_script(card_id: int, card_name: str, card_type: int, 
                      effect_desc: str = '', effect_pattern: Optional[str] = None,
                      effect_params: Optional[Dict[str, Any]] = None,
                      script_dir: str = "../script") -> bool:
    """
    Convenience function to create a card script
    
    Args:
        card_id: Card ID
        card_name: Card name
        card_type: Card type flags
        effect_desc: Effect description
        effect_pattern: Effect pattern name
        effect_params: Effect parameters
        script_dir: Directory to save script
    
    Returns:
        True if successful, False otherwise
    """
    generator = ScriptGenerator(output_dir=script_dir)
    
    card_data = {
        'id': card_id,
        'name': card_name,
        'type': card_type,
        'desc': effect_desc
    }
    
    return generator.generate_and_save(card_data, effect_pattern, effect_params)


if __name__ == "__main__":
    # Test the script generator
    print("Script Generator Test")
    print("=" * 60)
    
    generator = ScriptGenerator()
    
    # List available patterns
    print("\nAvailable Effect Patterns:")
    for name, desc in generator.list_available_patterns().items():
        print(f"  - {name}: {desc}")
    
    # Test: Generate a simple spell card that recovers LP
    test_card = {
        'id': 99999999,
        'name': 'Test Heal Card',
        'type': TYPE_SPELL,
        'desc': 'Restore 500 Life Points'
    }
    
    print(f"\nGenerating test script for card {test_card['id']}...")
    script = generator.generate_script(test_card, 'recover_lp', {'amount': 500})
    
    if script:
        print(f"\n✓ Script generated successfully!")
        print(f"\nPreview (first 10 lines):")
        lines = script.split('\n')[:10]
        for line in lines:
            print(f"  {line}")
    else:
        print(f"\n✗ Failed to generate script")

