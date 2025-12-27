from .base_level import BaseLevel


class Level2(BaseLevel):
    """
    Level 2: Intermediate - "Escalation"
    
    Increased difficulty with:
    - 8 enemies in two rows (4 per row)
    - Faster movement (1.3x speed multiplier)
    - More frequent shooting (1.5x shoot chance multiplier)
    
    Players face more enemies and increased aggression.
    """
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height, level_number=2)
    
    def get_level_name(self):
        """Return the name of Level 2"""
        return "Escalation"
    
    def get_enemy_count(self):
        """Level 2 has 8 enemies"""
        return 8
    
    def get_enemy_speed_multiplier(self):
        """Level 2 enemies move 30% faster"""
        return 1.3
    
    def get_enemy_shoot_chance_multiplier(self):
        """Level 2 enemies shoot 50% more frequently"""
        return 1.5
    
    def get_enemy_positions(self):
        """
        Create two rows of enemies (4 per row).
        Simple horizontal rows.
        
        Returns:
            List of (x, y) positions for enemies
        """
        positions = []
        enemies_per_row = 4
        spacing = 120
        row_spacing = 60
        
        # Calculate starting position for centered rows
        start_x = (self.screen_width - (enemies_per_row - 1) * spacing) // 2
        
        # First row (top)
        for i in range(enemies_per_row):
            x = start_x + i * spacing
            y = 80
            positions.append((x, y))
        
        # Second row (below)
        for i in range(enemies_per_row):
            x = start_x + i * spacing
            y = 80 + row_spacing
            positions.append((x, y))
        
        return positions
