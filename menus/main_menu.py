from .base_menu import BaseMenu


class MainMenu(BaseMenu):
    """Main menu displayed when the game starts"""
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.options = ["Start Game", "Select Level", "Quit Game"]
        self.selected_option = 0
    
    def draw(self, surface):
        """Draw the main menu"""
        self.draw_background(surface)
        self.draw_title(surface, "GALAXY SHOOTER")
        self.draw_options(surface)
        
        # Draw instructions
        instructions = "Use UP/DOWN or W/S to navigate, ENTER/SPACE to select"
        instruction_text = self.font_small.render(instructions, True, self.GRAY)
        instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        surface.blit(instruction_text, instruction_rect)
    
    def execute_option(self):
        """Execute the selected menu option"""
        if self.selected_option == 0:  # Start Game
            return "START_GAME"
        elif self.selected_option == 1:  # Select Level
            return "SELECT_LEVEL"
        elif self.selected_option == 2:  # Quit Game
            return "QUIT_GAME"
        return None