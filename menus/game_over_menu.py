from .base_menu import BaseMenu
import pygame


class GameOverMenu(BaseMenu):
    """Game over menu displayed when the player is destroyed"""
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.options = ["Restart Game", "Quit to Main Menu"]
        self.selected_option = 0
        self.show_delay = 2000
        self.timer = 0
    
    def update(self, dt):
        """Update the menu timer"""
        self.timer += dt
    
    def reset_timer(self):
        """Reset the timer when game over occurs"""
        self.timer = 0
    
    def draw(self, surface):
        """Draw the game over menu"""
        self.draw_background(surface)
        
        game_over_text = self.font_large.render("GAME OVER", True, self.RED)
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, 200))
        surface.blit(game_over_text, game_over_rect)
        
        if self.timer >= self.show_delay:
            self.draw_options(surface)
            
            instructions = "Use UP/DOWN or W/S to navigate, ENTER/SPACE to select"
            instruction_text = self.font_small.render(instructions, True, self.GRAY)
            instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
            surface.blit(instruction_text, instruction_rect)
        else:

            waiting_text = self.font_medium.render("Press any key to continue...", True, self.WHITE)
            waiting_rect = waiting_text.get_rect(center=(self.screen_width // 2, 350))
            surface.blit(waiting_text, waiting_rect)
    
    def handle_input(self, event):
        """Handle game over menu input"""
        if self.timer < self.show_delay:
            if event.type == pygame.KEYDOWN:
                self.timer = self.show_delay
            return None
        
        return super().handle_input(event)
    
    def execute_option(self):
        """Execute the selected menu option"""
        if self.selected_option == 0:  
            return "RESTART_GAME"
        elif self.selected_option == 1:
            return "MAIN_MENU"
        return None