from .base_menu import BaseMenu
import pygame


class LevelCompleteMenu(BaseMenu):
    """Menu displayed when a level is completed successfully"""
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.current_level = 1
        self.total_levels = 5
        self.level_name = ""
        self.options = ["Restart Level", "Main Menu"]
        self.selected_option = 0
        
        self.wait_time = 5000
        self.timer = 0
        self.can_proceed = False
        
    def set_level_info(self, level_number, level_name):
        """
        Set the current level information and update menu options.
        
        Args:
            level_number: The level that was just completed (1, 2, 3, etc.)
            level_name: The name of the completed level
        """
        self.current_level = level_number
        self.level_name = level_name
        
        self.timer = 0
        self.can_proceed = False
        
        if level_number < self.total_levels:
            self.options = ["Next Level", "Restart Level", "Select Level", "Main Menu"]
        else:
            self.options = ["Restart Level", "Select Level", "Main Menu"]
        
        self.selected_option = 0
    
    def update(self, dt):
        """
        Update the timer to enable options after 5 seconds.
        
        Args:
            dt: Delta time in milliseconds
        """
        if not self.can_proceed:
            self.timer += dt
            if self.timer >= self.wait_time:
                self.can_proceed = True
    
    def handle_input(self, event):
        """Handle menu input navigation - only allow input after timer expires"""
        if not self.can_proceed:
            return None
        
        return super().handle_input(event)
    
    def draw(self, surface):
        """Draw the level complete menu"""
        self.draw_background(surface)
        
        title_text = self.font_large.render("LEVEL COMPLETE!", True, self.GREEN)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 120))
        surface.blit(title_text, title_rect)
        
        level_info = f"Level {self.current_level}: {self.level_name}"
        level_text = self.font_medium.render(level_info, True, self.WHITE)
        level_rect = level_text.get_rect(center=(self.screen_width // 2, 200))
        surface.blit(level_text, level_rect)
        
        if self.current_level < self.total_levels:
            message = "Great job! Ready for the next challenge?"
        else:
            message = "CONGRATULATIONS! You've completed all levels!"
            victory_text = self.font_medium.render(message, True, self.YELLOW)
            victory_rect = victory_text.get_rect(center=(self.screen_width // 2, 250))
            surface.blit(victory_text, victory_rect)
            message = "You are a true Galaxy Shooter champion!"
        
        message_text = self.font_small.render(message, True, self.WHITE)
        message_rect = message_text.get_rect(center=(self.screen_width // 2, 280 if self.current_level < self.total_levels else 300))
        surface.blit(message_text, message_rect)
        
        if not self.can_proceed:
            remaining_time = max(0, (self.wait_time - self.timer) // 1000 + 1)
            timer_message = f"Please wait {remaining_time} seconds before continuing..."
            timer_text = self.font_small.render(timer_message, True, self.YELLOW)
            timer_rect = timer_text.get_rect(center=(self.screen_width // 2, 350))
            surface.blit(timer_text, timer_rect)
        else:
            self.draw_options(surface)
        
        if self.can_proceed:
            instructions = "Use UP/DOWN or W/S to navigate, ENTER/SPACE to select"
        else:
            instructions = "Enjoy your victory! Options will be available shortly..."
        instruction_text = self.font_small.render(instructions, True, self.GRAY)
        instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        surface.blit(instruction_text, instruction_rect)
    
    def execute_option(self):
        """Execute the selected menu option"""
        if not self.can_proceed:
            return None
        
        selected_text = self.options[self.selected_option]
        
        if selected_text == "Next Level":
            return "NEXT_LEVEL"
        elif selected_text == "Restart Level":
            return "RESTART_LEVEL"
        elif selected_text == "Select Level":
            return "SELECT_LEVEL"
        elif selected_text == "Main Menu":
            return "MAIN_MENU"
        
        return None
    
    def has_next_level(self):
        """Check if there is a next level available"""
        return self.current_level < self.total_levels
