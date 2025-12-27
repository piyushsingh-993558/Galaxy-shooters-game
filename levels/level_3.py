from .base_level import BaseLevel
from entities.boss3 import Boss3


class Level3(BaseLevel):
    """
    Level 3: Advanced - "Invasion Force"
    
    Advanced difficulty with:
    - 10 enemies in two rows (5 per row)
    - Moderately faster movement (1.4x speed multiplier)
    - More frequent shooting (1.8x shoot chance multiplier)
    
    A solid challenge before facing the bosses!
    """
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height, level_number=3)
    
    def get_level_name(self):
        """Return the name of Level 3"""
        return "Invasion Force"
    
    def get_enemy_count(self):
        """Level 3 has 10 enemies"""
        return 10
    
    def get_enemy_speed_multiplier(self):
        """Level 3 enemies move 40% faster"""
        return 1.4
    
    def get_enemy_shoot_chance_multiplier(self):
        """Level 3 enemies shoot 80% more frequently"""
        return 1.8
    
    def level_has_boss(self):
        """Level 3 has a boss after defeating all enemies"""
        return True
    
    def create_boss(self):
        """Create the Guardian Destroyer boss"""
        return Boss3(self.screen_width, self.screen_height)
    
    def get_enemy_positions(self):
        """
        Create two rows of enemies (5 per row).
        Simple horizontal rows.
        
        Returns:
            List of (x, y) positions for enemies
        """
        positions = []
        enemies_per_row = 5
        spacing = 100
        row_spacing = 60
        
        # Calculate starting position
        start_x = (self.screen_width - (enemies_per_row - 1) * spacing) // 2
        
        # Create two rows of enemies
        for row in range(2):
            y = 70 + row * row_spacing
            for col in range(enemies_per_row):
                x = start_x + col * spacing
                positions.append((x, y))
        
        return positions
