from .base_boss import BaseBoss


class Boss5(BaseBoss):
    """
    Boss 5: "Omega Commander" - Level 5 final boss
    
    Features:
    - 12 HP (12 bullets to kill)
    - Horizontal movement only
    - Fastest shooting rate
    - Boss5.jpeg image from assets/images
    
    The final challenge with maximum health and aggressive shooting.
    """
    
    def __init__(self, screen_width, screen_height):
        # Start boss at top center of screen
        x = screen_width // 2
        y = 50
        # Initialize with level 5
        super().__init__(x, y, screen_width, screen_height, level=5)
    
    def get_boss_name(self):
        """Return the name of this boss"""
        return "Omega Commander"