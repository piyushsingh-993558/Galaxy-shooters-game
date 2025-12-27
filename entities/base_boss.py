from abc import ABC, abstractmethod
import pygame
import random
import os
from .enemy import Enemy
from .enemyBullets import EnemyBullet

class BaseBoss(Enemy, ABC):
    """
    Abstract Base Class for all boss enemies that inherits from Enemy.
    
    This class provides a template for creating bosses with different configurations
    using inheritance and polymorphism. Each boss can customize:
    - Health points (level 3: 5 HP, level 4: 8 HP, level 5: 12 HP)
    - Boss images from assets/images directory
    - Stationary behavior (doesn't move down like regular enemies)
    - Shooting patterns
    
    Design Principles:
    - Inheritance: Inherits from Enemy class for common functionality
    - Reusability: Common boss logic is implemented once in base class
    - Modularity: Each boss is self-contained with its own configuration
    - Encapsulation: Boss state and logic are encapsulated in the class
    """
    
    def __init__(self, x, y, screen_width, screen_height, level):
        """
        Initialize the base boss.
        
        Args:
            x: Initial x position
            y: Initial y position
            screen_width: Width of the game screen
            screen_height: Height of the game screen
            level: Boss level (3, 4, or 5)
        """
        self.level = level
        self.screen_height = screen_height
        
        super().__init__(x, y, screen_width)
        
        self._load_boss_image()
        
        self.rect.centerx = x
        self.rect.y = y
        
        self.max_hp = self._get_max_hp_by_level()
        self.current_hp = self.max_hp
        self.is_alive = True
        
        self.speed = 0 
        self.move_direction = 1
        self.move_counter = 0
        self.horizontal_speed = 2
        
    def _load_boss_image(self):
        """
        Load the appropriate boss image based on level.
        """
        image_path = f"assets/images/boss{self.level}.png"
        
        if os.path.exists(image_path):
            try:
                # Load and scale the boss image
                original_image = pygame.image.load(image_path)
                # Scale the boss image to be larger than regular enemies
                self.image = pygame.transform.scale(original_image, (120, 90))
            except pygame.error as e:
                print(f"Could not load boss image {image_path}: {e}")
                self._create_fallback_image()
        else:
            print(f"Boss image {image_path} not found, using fallback")
            self._create_fallback_image()
            
    def _create_fallback_image(self):
        """
        Create a fallback colored rectangle if image loading fails.
        """
        self.image = pygame.Surface((120, 90))
        colors = {3: (255, 0, 0), 4: (255, 165, 0), 5: (128, 0, 128)}
        self.image.fill(colors.get(self.level, (255, 255, 255)))
        
    def _get_max_hp_by_level(self):
        """
        Return the maximum HP based on boss level.
        
        Returns:
            int: Maximum HP (level 3: 5, level 4: 8, level 5: 12)
        """
        hp_mapping = {3: 5, 4: 8, 5: 12}
        return hp_mapping.get(self.level, 5)
        
    def update(self, dt=None):
        """
        Update boss behavior. Override enemy update to prevent downward movement.
        
        Args:
            dt: Delta time in milliseconds (optional, for compatibility with sprite group updates)
        """
        self.rect.x += self.move_direction * self.horizontal_speed
        self.move_counter += 1
        
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
        
        if self.rect.left < 0:
            self.rect.left = 0
            self.move_direction = 1
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
            self.move_direction = -1
            
    def shoot(self):
        """
        Override enemy shoot method with boss-specific shooting pattern.
        Bosses shoot more frequently than regular enemies.
        
        Returns:
            EnemyBullet if shooting, None otherwise
        """
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot_delay = random.randint(500, 1500)
            return EnemyBullet(self.rect.centerx, self.rect.bottom)
        return None
    
    def take_damage(self, damage=1):
        """
        Reduce boss health by damage amount.
        
        Args:
            damage: Amount of damage to take (default: 1)
            
        Returns:
            True if boss is still alive, False if defeated
        """
        self.current_hp -= damage
        
        if self.current_hp <= 0:
            self.current_hp = 0
            self.is_alive = False
            return False
            
        return True
    
    def get_hp_percentage(self):
        """
        Get current HP as a percentage.
        
        Returns:
            Float between 0.0 and 1.0 representing HP percentage
        """
        return self.current_hp / self.max_hp if self.max_hp > 0 else 0.0
    
    def is_defeated(self):
        """
        Check if boss is defeated.
        
        Returns:
            True if boss is defeated, False otherwise
        """
        return not self.is_alive
        
    def draw_hp_bar(self, surface, x, y, width=200, height=20):
        """
        Draw the boss HP bar.
        
        Args:
            surface: Surface to draw on
            x: X position of the HP bar
            y: Y position of the HP bar
            width: Width of the HP bar
            height: Height of the HP bar
        """
        background_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, (100, 20, 20), background_rect)
        
        hp_percentage = self.get_hp_percentage()
        hp_width = int(width * hp_percentage)
        
        if hp_width > 0:
            hp_rect = pygame.Rect(x, y, hp_width, height)
            if hp_percentage > 0.6:
                color = (50, 200, 50)
            elif hp_percentage > 0.3:
                color = (200, 200, 50)
            else:
                color = (200, 50, 50)
            pygame.draw.rect(surface, color, hp_rect)
        
        pygame.draw.rect(surface, (255, 255, 255), background_rect, 2)
        
        font = pygame.font.Font(None, 24)
        hp_text = font.render(f"{self.current_hp}/{self.max_hp}", True, (255, 255, 255))
        text_rect = hp_text.get_rect(center=(x + width // 2, y + height // 2))
        surface.blit(hp_text, text_rect)
        
    def update_shooting(self, dt):
        """
        Update boss shooting behavior. This method is called by the main game loop.
        
        Args:
            dt: Delta time in milliseconds
            
        Returns:
            EnemyBullet if boss shoots, None otherwise
        """
        return self.shoot()
        
    @abstractmethod
    def get_boss_name(self):
        """
        Return the name of this boss.
        Must be implemented by subclasses.
        """
        pass