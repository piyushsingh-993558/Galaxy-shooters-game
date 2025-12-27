from .base_boss import BaseBoss


class Boss3(BaseBoss):
    """
    Boss 3: "Guardian Destroyer" - Level 3 boss encounter
    
    Features:
    - 5 HP (5 bullets to kill)
    - Horizontal movement only
    - Faster shooting than regular enemies
    - Boss3.jpeg image from assets/images
    
    This boss introduces players to boss mechanics with moderate challenge.
    """
    
    def __init__(self, screen_width, screen_height):
        x = screen_width // 2
        y = 50
        super().__init__(x, y, screen_width, screen_height, level=3)
    
    def get_boss_name(self):
        """Return the name of this boss"""
        return "Guardian Destroyer"