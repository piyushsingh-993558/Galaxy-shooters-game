from .base_level import BaseLevel
from entities.boss4 import Boss4


class Level4(BaseLevel):
    """
    Level 4: Expert - "Massive Assault"
    
    High difficulty with:
    - 14 enemies in two rows (7 per row)
    - Fast movement (1.6x speed multiplier)
    - Frequent shooting (2.0x shoot chance multiplier)
    
    A challenging test before the boss battle!
    """
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height, level_number=4)
    
    def get_level_name(self):
        """Return the name of Level 4"""
        return "Massive Assault"
    
    def get_enemy_count(self):
        """Level 4 has 14 enemies"""
        return 14
    
    def get_enemy_speed_multiplier(self):
        """Level 4 enemies move 60% faster"""
        return 1.6
    
    def get_enemy_shoot_chance_multiplier(self):
        """Level 4 enemies shoot 2x more frequently"""
        return 2.0
    
    def level_has_boss(self):
        """Level 4 has a boss after defeating all enemies"""
        return True
    
    def create_boss(self):
        """Create the War Machine boss"""
        return Boss4(self.screen_width, self.screen_height)
    
    def get_enemy_positions(self):
        """
        Create two rows of enemies (7 per row).
        Simple horizontal rows.
        
        Returns:
            List of (x, y) positions for enemies
        """
        positions = []
        enemies_per_row = 7
        spacing = 80
        row_spacing = 60
        
        # Calculate starting position
        start_x = (self.screen_width - (enemies_per_row - 1) * spacing) // 2
        
        # Create two rows of enemies
        for row in range(2):
            y = 60 + row * row_spacing
            for col in range(enemies_per_row):
                x = start_x + col * spacing
                positions.append((x, y))
        
        return positions