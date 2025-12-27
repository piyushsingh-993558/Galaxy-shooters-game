from .base_menu import BaseMenu
import pygame


class LevelSelectMenu(BaseMenu):
    """Menu for selecting which level to play"""
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height)
        self.level_names = [
            "Level 1: First Contact",
            "Level 2: Escalation", 
            "Level 3: Invasion Force",
            "Level 4: Massive Assault",
            "Level 5: Final Confrontation",
            "Back to Main Menu"
        ]
        self.options = self.level_names
        self.selected_option = 0
        
        # Level descriptions for display
        self.level_descriptions = [
            "Beginner - 5 enemies, normal speed",
            "Intermediate - 10 enemies, faster movement",
            "Advanced - 15 enemies, rapid fire",
            "Expert - 20 enemies, diamond formation",
            "Master - 25 enemies, ultimate challenge",
            "Return to the main menu"
        ]
    
    def draw(self, surface):
        """Draw the level selection menu"""
        self.draw_background(surface)
        
        self.draw_title(surface, "SELECT LEVEL")
        
        start_y = 250
        option_spacing = 70
        
        for i, (level_name, description) in enumerate(zip(self.level_names, self.level_descriptions)):

            name_color = self.YELLOW if i == self.selected_option else self.WHITE
            desc_color = self.GRAY if i == self.selected_option else (100, 100, 100)
            
            name_text = self.font_medium.render(level_name, True, name_color)
            name_rect = name_text.get_rect(center=(self.screen_width // 2, start_y + i * option_spacing))
            surface.blit(name_text, name_rect)
            

            if i < len(self.level_descriptions) - 1:
                desc_text = self.font_small.render(description, True, desc_color)
                desc_rect = desc_text.get_rect(center=(self.screen_width // 2, start_y + i * option_spacing + 25))
                surface.blit(desc_text, desc_rect)
            

            if i == self.selected_option:
                indicator = self.font_medium.render("> ", True, self.YELLOW)
                indicator_rect = indicator.get_rect()
                indicator_rect.right = name_rect.left - 10
                indicator_rect.centery = name_rect.centery
                surface.blit(indicator, indicator_rect)
        
        instructions = "Use UP/DOWN or W/S to navigate, ENTER/SPACE to select"
        instruction_text = self.font_small.render(instructions, True, self.GRAY)
        instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        surface.blit(instruction_text, instruction_rect)
    
    def execute_option(self):
        """Execute the selected menu option"""
        if self.selected_option < 5:
            return f"LEVEL_{self.selected_option + 1}"
        else:
            return "MAIN_MENU"
        
        return None