from .base_level import BaseLevel


class Level1(BaseLevel):
    """
    Level 1: Beginner - "First Contact"
    
    This is the easiest level with:
    - 4 enemies in a simple horizontal line
    - Normal speed (1.0x multiplier)
    - Normal shooting frequency (1.0x multiplier)
    
    Perfect for players to learn the game mechanics.
    """
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height, level_number=1)
    
    def get_level_name(self):
        """Return the name of Level 1"""
        return "First Contact"
    
    def get_enemy_count(self):
        """Level 1 has 4 enemies"""
        return 4
    
    def get_enemy_speed_multiplier(self):
        """Level 1 enemies move at normal speed"""
        return 1.0
    
    def get_enemy_shoot_chance_multiplier(self):
        """Level 1 enemies shoot at normal frequency"""
        return 1.0
    
    def get_enemy_positions(self):
        """
        Create a simple horizontal line of 4 enemies.
        Evenly spaced across the screen.
        
        Returns:
            List of (x, y) positions for enemies
        """
        positions = []
        enemy_count = self.get_enemy_count()
        spacing = 120  # More spacing for easier gameplay
        start_x = (self.screen_width - (enemy_count - 1) * spacing) // 2
        y_position = 100
        
        for i in range(enemy_count):
            x = start_x + i * spacing
            positions.append((x, y_position))
        
        return positions
