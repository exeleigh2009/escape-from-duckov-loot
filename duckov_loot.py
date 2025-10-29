"""
Duckov Rarity Indicator Mod
Author: YourName
Version: 1.2.0
"""

from enum import Enum
from typing import Dict, Tuple, List
import json
import time

class RarityLevel(Enum):
    TRASH = "trash"
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    ARTIFACT = "artifact"

class RarityMod:
    def __init__(self):
        self.mod_name = "Rarity Indicator"
        self.version = "1.2.0"
        self.author = "YourName"
        self.enabled = True
        
        # Rarity colors (RGB)
        self.rarity_colors = {
            RarityLevel.TRASH: (128, 128, 128),       # Gray
            RarityLevel.COMMON: (255, 255, 255),      # White
            RarityLevel.UNCOMMON: (0, 100, 255),      # Blue
            RarityLevel.RARE: (170, 0, 255),          # Purple
            RarityLevel.EPIC: (255, 128, 0),          # Orange
            RarityLevel.LEGENDARY: (255, 0, 0),       # Red
            RarityLevel.ARTIFACT: (255, 255, 0)       # Yellow
        }
        
        # Rarity names for display
        self.rarity_names = {
            RarityLevel.TRASH: "Trash",
            RarityLevel.COMMON: "Common",
            RarityLevel.UNCOMMON: "Uncommon",
            RarityLevel.RARE: "Rare",
            RarityLevel.EPIC: "Epic",
            RarityLevel.LEGENDARY: "Legendary",
            RarityLevel.ARTIFACT: "Artifact"
        }
        
        # Spawn chances (percentage)
        self.spawn_chances = {
            RarityLevel.TRASH: 40.0,
            RarityLevel.COMMON: 35.0,
            RarityLevel.UNCOMMON: 15.0,
            RarityLevel.RARE: 6.0,
            RarityLevel.EPIC: 3.0,
            RarityLevel.LEGENDARY: 0.9,
            RarityLevel.ARTIFACT: 0.1
        }
        
        self.item_rarity = self.load_item_rarity()
        self.rarity_cache = {}
        
    def load_item_rarity(self) -> Dict[str, RarityLevel]:
        """Load item rarity from config file"""
        try:
            with open('config/rarity_config.json', 'r') as f:
                config = json.load(f)
                return {item: RarityLevel(rarity) for item, rarity in config.items()}
        except FileNotFoundError:
            # Default rarity assignments
            return {
                # Trash items
                "Bread Crust": RarityLevel.TRASH,
                "Broken Feather": RarityLevel.TRASH,
                "Muddy Water": RarityLevel.TRASH,
                
                # Common items
                "Bread Crumbs": RarityLevel.COMMON,
                "Duck Feather": RarityLevel.COMMON,
                "Pond Water": RarityLevel.COMMON,
                "Small Stone": RarityLevel.COMMON,
                
                # Uncommon items
                "Rubber Duck": RarityLevel.UNCOMMON,
                "Duck Tape": RarityLevel.UNCOMMON,
                "Duck Goggles": RarityLevel.UNCOMMON,
                "Quack Radio": RarityLevel.UNCOMMON,
                
                # Rare items
                "Golden Egg": RarityLevel.RARE,
                "Platinum Feather": RarityLevel.RARE,
                "Treasure Map": RarityLevel.RARE,
                "Ancient Coin": RarityLevel.RARE,
                
                # Epic items
                "Duck King's Crown": RarityLevel.EPIC,
                "Magic Bread": RarityLevel.EPIC,
                "Ancient Artifact": RarityLevel.EPIC,
                "Crystal Pond Shard": RarityLevel.EPIC,
                
                # Legendary items
                "Phoenix Egg": RarityLevel.LEGENDARY,
                "Staff of Quack": RarityLevel.LEGENDARY,
                "Scroll of Eternal Life": RarityLevel.LEGENDARY,
                "Duck God's Blessing": RarityLevel.LEGENDARY,
                
                # Artifact items
                "Heart of the Lake": RarityLevel.ARTIFACT,
                "Key to Duck Paradise": RarityLevel.ARTIFACT,
                "Relic of First Duck": RarityLevel.ARTIFACT,
                "Eternal Bread": RarityLevel.ARTIFACT
            }
    
    def get_item_rarity(self, item_name: str) -> RarityLevel:
        """Get rarity level for an item"""
        if item_name in self.rarity_cache:
            return self.rarity_cache[item_name]
        
        rarity = self.item_rarity.get(item_name, RarityLevel.COMMON)
        self.rarity_cache[item_name] = rarity
        return rarity
    
    def get_rarity_color(self, rarity: RarityLevel) -> Tuple[int, int, int]:
        """Get RGB color for rarity level"""
        return self.rarity_colors.get(rarity, (255, 255, 255))
    
    def get_rarity_display_name(self, rarity: RarityLevel) -> str:
        """Get display name for rarity level"""
        return self.rarity_names.get(rarity, "Unknown")
    
    def format_item_display(self, item_name: str) -> str:
        """Format item name with rarity indicator"""
        rarity = self.get_item_rarity(item_name)
        display_name = self.get_rarity_display_name(rarity)
        
        # Emoji indicators
        emoji_map = {
            RarityLevel.TRASH: "⚪",
            RarityLevel.COMMON: "⚪",
            RarityLevel.UNCOMMON: "🔵",
            RarityLevel.RARE: "🟣",
            RarityLevel.EPIC: "🟠",
            RarityLevel.LEGENDARY: "🔴",
            RarityLevel.ARTIFACT: "🟡"
        }
        
        emoji = emoji_map.get(rarity, "⚪")
        return f"{emoji} [{display_name}] {item_name}"
    
    def get_rarity_tooltip(self, item_name: str) -> Dict:
        """Get complete rarity information for tooltip"""
        rarity = self.get_item_rarity(item_name)
        color = self.get_rarity_color(rarity)
        
        return {
            "item_name": item_name,
            "rarity_level": rarity.value,
            "rarity_name": self.get_rarity_display_name(rarity),
            "color": color,
            "spawn_chance": self.spawn_chances.get(rarity, 0),
            "value_multiplier": self.get_value_multiplier(rarity)
        }
    
    def get_value_multiplier(self, rarity: RarityLevel) -> float:
        """Get value multiplier based on rarity"""
        multipliers = {
            RarityLevel.TRASH: 0.5,
            RarityLevel.COMMON: 1.0,
            RarityLevel.UNCOMMON: 2.5,
            RarityLevel.RARE: 6.0,
            RarityLevel.EPIC: 15.0,
            RarityLevel.LEGENDARY: 40.0,
            RarityLevel.ARTIFACT: 100.0
        }
        return multipliers.get(rarity, 1.0)
    
    def generate_loot_notification(self, item_name: str) -> str:
        """Generate colored loot notification"""
        rarity = self.get_item_rarity(item_name)
        display_name = self.get_rarity_display_name(rarity)
        
        notifications = {
            RarityLevel.UNCOMMON: f"🦆 Uncommon item found: {item_name}",
            RarityLevel.RARE: f"🎉 Rare item found: {item_name}",
            RarityLevel.EPIC: f"🔥 Epic item found: {item_name}",
            RarityLevel.LEGENDARY: f"💎 LEGENDARY ITEM FOUND: {item_name}",
            RarityLevel.ARTIFACT: f"🌟 ARTIFACT DISCOVERED: {item_name}"
        }
        
        return notifications.get(rarity, f"Item found: {item_name}")
    
    def calculate_item_value(self, base_value: float, item_name: str) -> float:
        """Calculate final item value with rarity multiplier"""
        rarity = self.get_item_rarity(item_name)
        multiplier = self.get_value_multiplier(rarity)
        return base_value * multiplier

# Example usage in game
class EnhancedInventory:
    def __init__(self):
        self.rarity_mod = RarityMod()
        self.items = []
    
    def add_item(self, item_name: str, base_value: float):
        """Add item with rarity consideration"""
        final_value = self.rarity_mod.calculate_item_value(base_value, item_name)
        display_name = self.rarity_mod.format_item_display(item_name)
        
        item_data = {
            'name': item_name,
            'display_name': display_name,
            'base_value': base_value,
            'final_value': final_value,
            'rarity_info': self.rarity_mod.get_rarity_tooltip(item_name)
        }
        
        self.items.append(item_data)
        
        # Show special notification for rare items
        rarity = self.rarity_mod.get_item_rarity(item_name)
        if rarity.value in ['uncommon', 'rare', 'epic', 'legendary', 'artifact']:
            print(self.rarity_mod.generate_loot_notification(item_name))
    
    def display_inventory(self):
        """Display inventory with rarity colors"""
        print("\n=== ENHANCED INVENTORY ===")
        for item in self.items:
            print(f"{item['display_name']} - Value: {item['final_value']:.1f}")
            print(f"   Rarity: {item['rarity_info']['rarity_name']}")

# Configuration file
rarity_config = {
    "Bread Crust": "trash",
    "Bread Crumbs": "common",
    "Rubber Duck": "uncommon",
    "Golden Egg": "rare",
    "Duck King's Crown": "epic",
    "Phoenix Egg": "legendary",
    "Heart of the Lake": "artifact"
}

# Save config (run once)
with open('config/rarity_config.json', 'w') as f:
    json.dump(rarity_config, f, indent=2)
