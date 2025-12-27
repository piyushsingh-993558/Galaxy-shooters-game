from .base_level import BaseLevel
from entities.boss5 import Boss5


class Level5(BaseLevel):
    """
    Level 5: Master - "Final Confrontation"
    
    Ultimate difficulty with:
    - 18 enemies in three rows (6 per row)
    - Fast movement (2.2x speed multiplier)
    - Maximum shooting frequency (3.0x shoot chance multiplier)
    
    The ultimate test for galaxy shooter masters!
    """
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height, level_number=5)
    
    def get_level_name(self):
        """Return the name of Level 5"""
        return "Final Confrontation"
    
    def get_enemy_count(self):
        """Level 5 has 18 enemies"""
        return 18
    
    def get_enemy_speed_multiplier(self):
        """Level 5 enemies move 2.2x faster"""
        return 2.2
    
    def get_enemy_shoot_chance_multiplier(self):
        """Level 5 enemies shoot 3x more frequently"""
        return 3.0
    
    def level_has_boss(self):
        """Level 5 has the final boss after defeating all enemies"""
        return True
    
    def create_boss(self):
        """Create the Omega Commander final boss"""
        return Boss5(self.screen_width, self.screen_height)
    
    def get_enemy_positions(self):
        """
        Create three rows of enemies (6 per row).
        Simple horizontal rows.
        
        Returns:
            List of (x, y) positions for enemies
        """
        positions = []
        enemies_per_row = 6
        spacing = 90
        row_spacing = 55
        
        # Calculate starting position
        start_x = (self.screen_width - (enemies_per_row - 1) * spacing) // 2
        
        # Create three rows of enemies
        for row in range(3):
            y = 50 + row * row_spacing
            for col in range(enemies_per_row):
                x = start_x + col * spacing
                positions.append((x, y))
        
        return positions