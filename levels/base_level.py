from abc import ABC, abstractmethod
import pygame
from entities.enemy import Enemy


class BaseLevel(ABC):
    """
    Abstract Base Class for all game levels.
    
    This class provides a template for creating levels with different configurations
    using inheritance and polymorphism. Each level can customize:
    - Number of enemies
    - Enemy speed
    - Enemy behavior (shooting frequency)
    - Level layout and patterns
    
    Design Principles:
    - Reusability: Common level logic is implemented once in base class
    - Modularity: Each level is self-contained with its own configuration
    - Inheritance: Subclasses inherit common behavior and customize specifics
    - Encapsulation: Level state and logic are encapsulated in the class
    """
    
    def __init__(self, screen_width, screen_height, level_number):
        """
        Initialize the base level.
        
        Args:
            screen_width: Width of the game screen
            screen_height: Height of the game screen
            level_number: The level number (1, 2, 3, etc.)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level_number = level_number
        self.enemy_group = pygame.sprite.Group()
        self.is_complete = False
        self.total_enemies = 0
        self.enemies_killed = 0
        
        # Boss support
        self.has_boss = self.level_has_boss()
        self.boss = None
        self.boss_spawned = False
        self.enemies_phase_complete = False
        
    @abstractmethod
    def get_level_name(self):
        """
        Return the name of the level.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def get_enemy_count(self):
        """
        Return the number of enemies in this level.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def get_enemy_speed_multiplier(self):
        """
        Return the speed multiplier for enemies (1.0 = normal, >1.0 = faster).
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def get_enemy_shoot_chance_multiplier(self):
        """
        Return the shoot chance multiplier for enemies (1.0 = normal, >1.0 = more frequent).
        Must be implemented by subclasses.
        """
        pass
    
    def level_has_boss(self):
        """
        Return whether this level has a boss.
        Can be overridden by subclasses (default: False).
        """
        return False
    
    def create_boss(self):
        """
        Create the boss for this level.
        Should be overridden by subclasses that have bosses.
        
        Returns:
            Boss instance or None if no boss
        """
        return None
    
    def create_enemy(self, x, y):
        """
        Create an enemy with level-specific attributes.
        This method applies the level's difficulty modifiers to the enemy.
        
        Args:
            x: X position for the enemy
            y: Y position for the enemy
            
        Returns:
            Enemy instance configured for this level
        """
        enemy = Enemy(x, y, self.screen_width)
        enemy.speed *= self.get_enemy_speed_multiplier()
        enemy.shoot_chance *= self.get_enemy_shoot_chance_multiplier()
        return enemy
    
    def spawn_enemies(self):
        """
        Spawn all enemies for this level based on the pattern defined by subclass.
        This is a template method that calls get_enemy_positions() which must be
        implemented by subclasses.
        """
        self.enemy_group.empty()
        positions = self.get_enemy_positions()
        
        for x, y in positions:
            enemy = self.create_enemy(x, y)
            self.enemy_group.add(enemy)
        
        self.total_enemies = len(positions)
        self.enemies_killed = 0
        self.is_complete = False
        
        # Reset boss state
        self.boss = None
        self.boss_spawned = False
        self.enemies_phase_complete = False
    
    @abstractmethod
    def get_enemy_positions(self):
        """
        Return a list of (x, y) tuples representing initial enemy positions.
        Must be implemented by subclasses to define the level layout.
        
        Returns:
            List of (x, y) tuples
        """
        pass
    
    def update(self):
        """
        Update the level state.
        Handles both regular enemies and boss encounters.
        """
        self.enemy_group.update()
        
        # Check if all regular enemies are defeated
        if len(self.enemy_group) == 0 and not self.enemies_phase_complete:
            self.enemies_phase_complete = True
            
            # If this level has a boss, spawn it
            if self.has_boss and not self.boss_spawned:
                self.boss = self.create_boss()
                self.boss_spawned = True
            elif not self.has_boss:
                # No boss, level is complete
                self.is_complete = True
        
        # Update boss if it exists
        if self.boss and not self.boss.is_defeated():
            self.boss.update()
        elif self.boss and self.boss.is_defeated() and not self.is_complete:
            # Boss is defeated, level is complete
            self.is_complete = True
    
    def get_boss(self):
        """
        Get the current boss instance.
        
        Returns:
            Boss instance or None if no boss or boss not spawned
        """
        return self.boss if self.boss_spawned else None
    
    def enemy_killed(self):
        """
        Called when an enemy is killed.
        Tracks the number of enemies killed for stats/scoring.
        """
        self.enemies_killed += 1
    
    def boss_killed(self):
        """
        Called when the boss is killed.
        This can be used for special scoring or effects.
        """
        pass  # Default implementation does nothing
    
    def get_progress(self):
        """
        Get the level completion progress.
        
        Returns:
            Tuple of (enemies_killed, total_enemies)
        """
        return (self.enemies_killed, self.total_enemies)
    
    def is_level_complete(self):
        """
        Check if the level is complete (all enemies defeated).
        
        Returns:
            True if level is complete, False otherwise
        """
        return self.is_complete
    
    def reset(self):
        """
        Reset the level to its initial state.
        Useful for restarting a level.
        """
        self.spawn_enemies()
        # Boss state will be reset in spawn_enemies()
    
    def get_info(self):
        """
        Get information about the level.
        
        Returns:
            Dictionary containing level information
        """
        return {
            'level_number': self.level_number,
            'level_name': self.get_level_name(),
            'total_enemies': self.total_enemies,
            'enemies_killed': self.enemies_killed,
            'is_complete': self.is_complete,
            'progress_percentage': (self.enemies_killed / self.total_enemies * 100) if self.total_enemies > 0 else 0
        }
