"""
Level Manager for Galaxy Shooter

This class manages all level-related functionality including:
- Loading and switching between levels
- Tracking progress and statistics
- Managing level transitions
- Providing level information

Design principles used:
- Single Responsibility: Manages only level-related concerns
- Encapsulation: Keeps level state and logic together
- Abstraction: Provides simple interface for level management
"""

from levels import Level1, Level2, Level3, Level4, Level5


class LevelManager:
    """
    Manages all levels in the game.
    
    This class is responsible for:
    - Creating and storing level instances
    - Switching between levels
    - Tracking game progression
    - Providing level information
    """
    
    def __init__(self, screen_width, screen_height):
        """
        Initialize the level manager.
        
        Args:
            screen_width: Width of the game screen
            screen_height: Height of the game screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Create all level instances
        self.levels = [
            Level1(screen_width, screen_height),
            Level2(screen_width, screen_height),
            Level3(screen_width, screen_height),
            Level4(screen_width, screen_height),
            Level5(screen_width, screen_height)
        ]
        
        # Current level tracking
        self.current_level_index = 0
        self.current_level = None
        
        # Statistics
        self.levels_completed = []  # Track which levels have been completed
        
    def get_level_count(self):
        """Get the total number of levels"""
        return len(self.levels)
    
    def get_current_level_index(self):
        """Get the current level index (0-based)"""
        return self.current_level_index
    
    def get_current_level(self):
        """Get the current level instance"""
        return self.current_level
    
    def load_level(self, level_index):
        """
        Load a specific level by index.
        
        Args:
            level_index: Index of the level to load (0-4 for levels 1-5)
            
        Returns:
            The loaded level instance, or None if invalid index
        """
        if 0 <= level_index < len(self.levels):
            self.current_level_index = level_index
            self.current_level = self.levels[level_index]
            self.current_level.spawn_enemies()
            return self.current_level
        return None
    
    def load_next_level(self):
        """
        Load the next level in sequence.
        
        Returns:
            The next level instance, or None if no next level exists
        """
        next_index = self.current_level_index + 1
        if next_index < len(self.levels):
            return self.load_level(next_index)
        return None
    
    def restart_current_level(self):
        """Restart the current level"""
        if self.current_level:
            self.current_level.reset()
            return self.current_level
        return None
    
    def mark_level_completed(self, level_index):
        """
        Mark a level as completed.
        
        Args:
            level_index: Index of the completed level
        """
        if level_index not in self.levels_completed:
            self.levels_completed.append(level_index)
    
    def is_level_completed(self, level_index):
        """
        Check if a level has been completed.
        
        Args:
            level_index: Index of the level to check
            
        Returns:
            True if level has been completed, False otherwise
        """
        return level_index in self.levels_completed
    
    def get_level_info(self, level_index=None):
        """
        Get information about a level.
        
        Args:
            level_index: Index of the level to get info for (current level if None)
            
        Returns:
            Dictionary with level information
        """
        if level_index is None:
            level = self.current_level
            index = self.current_level_index
        else:
            if 0 <= level_index < len(self.levels):
                level = self.levels[level_index]
                index = level_index
            else:
                return None
        
        if level:
            info = level.get_info()
            info['is_unlocked'] = True  # All levels are unlocked in this implementation
            info['is_completed'] = self.is_level_completed(index)
            return info
        return None
    
    def get_all_levels_info(self):
        """
        Get information about all levels.
        
        Returns:
            List of dictionaries with information for each level
        """
        return [self.get_level_info(i) for i in range(len(self.levels))]
    
    def get_progress_stats(self):
        """
        Get overall game progress statistics.
        
        Returns:
            Dictionary with progress information
        """
        return {
            'total_levels': len(self.levels),
            'completed_levels': len(self.levels_completed),
            'current_level': self.current_level_index + 1 if self.current_level else 0,
            'completion_percentage': (len(self.levels_completed) / len(self.levels)) * 100
        }
    
    def reset_progress(self):
        """Reset all progress (for new game)"""
        self.levels_completed.clear()
        self.current_level_index = 0
        self.current_level = None
        
        # Reset all individual levels
        for level in self.levels:
            level.reset()