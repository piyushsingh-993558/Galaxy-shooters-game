from abc import ABC, abstractmethod
import pygame


class BaseMenu(ABC):
    """Abstract Base Class for all game menus"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GRAY = (128, 128, 128)
        self.YELLOW = (255, 255, 0)
        

        self.selected_option = 0
        self.options = []
        
    def draw_title(self, surface, title):
        """Draw the menu title"""
        title_text = self.font_large.render(title, True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 150))
        surface.blit(title_text, title_rect)
        
    def draw_options(self, surface):
        """Draw menu options with selection highlight"""
        start_y = 300
        option_spacing = 80
        
        for i, option in enumerate(self.options):
            color = self.YELLOW if i == self.selected_option else self.WHITE
            option_text = self.font_medium.render(option, True, color)
            option_rect = option_text.get_rect(center=(self.screen_width // 2, start_y + i * option_spacing))
            surface.blit(option_text, option_rect)
            
            # Draw selection indicator
            if i == self.selected_option:
                indicator = self.font_medium.render("> ", True, self.YELLOW)
                indicator_rect = indicator.get_rect()
                indicator_rect.right = option_rect.left - 10
                indicator_rect.centery = option_rect.centery
                surface.blit(indicator, indicator_rect)
    
    def draw_background(self, surface):
        """Draw semi-transparent background overlay"""
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(180)
        overlay.fill(self.BLACK)
        surface.blit(overlay, (0, 0))
    
    def handle_input(self, event):
        """Handle menu input navigation"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.execute_option()
        return None
    
    @abstractmethod
    def execute_option(self):
        """Execute the selected menu option"""
        pass
    
    @abstractmethod
    def draw(self, surface):
        """Draw the complete menun"""
        pass