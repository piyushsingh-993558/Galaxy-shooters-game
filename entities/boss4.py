from .base_boss import BaseBoss


class Boss4(BaseBoss):
    """
    Boss 4: "War Machine" - Level 4 boss encounter
    
    Features:
    - 8 HP (8 bullets to kill)
    - Horizontal movement only
    - Faster shooting than Boss3
    - Boss4.jpeg image from assets/images
    
    This boss provides a moderate challenge with increased durability.
    """
    
    def __init__(self, screen_width, screen_height):
        # Start boss at top center of screen
        x = screen_width // 2
        y = 50
        # Initialize with level 4
        super().__init__(x, y, screen_width, screen_height, level=4)
    
    def get_boss_name(self):
        """Return the name of this boss"""
        return "War Machine"