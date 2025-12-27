from .base_menu import BaseMenu


class PauseMenu(BaseMenu):
    """Pause menu displayed when the game is paused during gameplay"""
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.options = ["Resume Game", "Restart Game", "Quit to Main Menu"]
        self.selected_option = 0
    
    def draw(self, surface):
        """Draw the pause menu"""
        self.draw_background(surface)
        self.draw_title(surface, "GAME PAUSED")
        self.draw_options(surface)
        
        # Draw instructions
        instructions_1 = "Use UP/DOWN or W/S to navigate, ENTER/SPACE to select"
        instructions_2 = "Press ESC or P to resume game"
        
        instruction_text_1 = self.font_small.render(instructions_1, True, self.GRAY)
        instruction_rect_1 = instruction_text_1.get_rect(center=(self.screen_width // 2, self.screen_height - 80))
        surface.blit(instruction_text_1, instruction_rect_1)
        
        instruction_text_2 = self.font_small.render(instructions_2, True, self.GRAY)
        instruction_rect_2 = instruction_text_2.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        surface.blit(instruction_text_2, instruction_rect_2)
    
    def execute_option(self):
        """Execute the selected menu option"""
        if self.selected_option == 0:  # Resume Game
            return "RESUME_GAME"
        elif self.selected_option == 1:  # Restart Game
            return "RESTART_GAME"
        elif self.selected_option == 2:  # Quit to Main Menu
            return "MAIN_MENU"
        return None