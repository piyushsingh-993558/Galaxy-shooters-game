import pygame
import random
from pygame.locals import *
from entities.player import Player
from entities.enemy import Enemy
from entities.explosion import Explosion
from menus import MainMenu, GameOverMenu, PauseMenu, LevelCompleteMenu, LevelSelectMenu
from levels import Level1, Level2, Level3, Level4, Level5
from managers.level_manager import LevelManager

# Game states
MAIN_MENU = "MAIN_MENU"
LEVEL_SELECT = "LEVEL_SELECT"
PLAYING = "PLAYING"
PAUSED = "PAUSED"
GAME_OVER = "GAME_OVER"
LEVEL_COMPLETE = "LEVEL_COMPLETE"

def main():
    pygame.init()

    clock = pygame.time.Clock()
    fps = 50

    screenWidth = 600
    screenHeight = 800

    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption('Galaxy Shooter')

    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    bg = pygame.image.load('assets/images/background2.png')

    bg_x = 0
    bg_y = 0

    def draw_bg():
        screen.blit(bg, (bg_x, bg_y))
    
    # Initialize menus
    main_menu = MainMenu(screenWidth, screenHeight)
    level_select_menu = LevelSelectMenu(screenWidth, screenHeight)
    game_over_menu = GameOverMenu(screenWidth, screenHeight)
    pause_menu = PauseMenu(screenWidth, screenHeight)
    level_complete_menu = LevelCompleteMenu(screenWidth, screenHeight)
    
    # Game state
    current_state = MAIN_MENU
    
    level_manager = LevelManager(screenWidth, screenHeight)
    current_level = None

    player = None
    player_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    enemy_bullet_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    boss_group = pygame.sprite.Group()  # New boss group

    def initialize_game(level_index=0):
        """
        Initialize/reset the game to starting state with specified level.
        
        Args:
            level_index: Index of the level to start (0 = Level 1, 1 = Level 2, etc.)
        """
        nonlocal player, current_level
        
        # Load the level using level manager
        current_level = level_manager.load_level(level_index)
        
        # Clear all sprite groups
        bullet_group.empty()
        enemy_group.empty()
        enemy_bullet_group.empty()
        explosion_group.empty()
        player_group.empty()
        boss_group.empty()  # Clear boss group too
        
        # Create new player
        player = Player(screenWidth // 2, screenHeight - 130, screenWidth)
        player_group.add(player)
        
        # Copy enemies from level to game enemy_group
        if current_level:
            for enemy in current_level.enemy_group:
                enemy_group.add(enemy)
        
        # Reset game over menu timer
        game_over_menu.reset_timer()

    run = True
    while run:
        dt = clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                # Handle state-specific input
                if current_state == MAIN_MENU:
                    action = main_menu.handle_input(event)
                    if action == "START_GAME":
                        initialize_game()  # Start with Level 1
                        current_state = PLAYING
                    elif action == "SELECT_LEVEL":
                        current_state = LEVEL_SELECT
                    elif action == "QUIT_GAME":
                        run = False
                
                elif current_state == LEVEL_SELECT:
                    action = level_select_menu.handle_input(event)
                    if action == "MAIN_MENU":
                        current_state = MAIN_MENU
                    elif action and action.startswith("LEVEL_"):
                        # Extract level number from action (LEVEL_1, LEVEL_2, etc.)
                        level_num = int(action.split("_")[1])
                        initialize_game(level_num - 1)  # Convert to 0-based index
                        current_state = PLAYING
                
                elif current_state == PLAYING:
                    # Pause key
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        current_state = PAUSED
                    # Shooting
                    elif event.key == pygame.K_SPACE:
                        bullet = player.shoot()
                        if bullet:
                            bullet_group.add(bullet)
                
                elif current_state == PAUSED:
                    # Resume with ESC or P
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        current_state = PLAYING
                    else:
                        action = pause_menu.handle_input(event)
                        if action == "RESUME_GAME":
                            current_state = PLAYING
                        elif action == "RESTART_GAME":
                            current_level_index = level_manager.get_current_level_index()
                            initialize_game(current_level_index)
                            current_state = PLAYING
                        elif action == "MAIN_MENU":
                            current_state = MAIN_MENU
                
                elif current_state == GAME_OVER:
                    action = game_over_menu.handle_input(event)
                    if action == "RESTART_GAME":
                        # Restart current level
                        current_level_index = level_manager.get_current_level_index()
                        initialize_game(current_level_index)
                        current_state = PLAYING
                    elif action == "MAIN_MENU":
                        current_state = MAIN_MENU
                
                elif current_state == LEVEL_COMPLETE:
                    action = level_complete_menu.handle_input(event)
                    if action == "NEXT_LEVEL":
                        # Load next level
                        next_level = level_manager.load_next_level()
                        if next_level:
                            initialize_game(level_manager.get_current_level_index())
                            current_state = PLAYING
                    elif action == "RESTART_LEVEL":
                        # Restart current level
                        current_level_index = level_manager.get_current_level_index()
                        initialize_game(current_level_index)
                        current_state = PLAYING
                    elif action == "SELECT_LEVEL":
                        current_state = LEVEL_SELECT
                    elif action == "MAIN_MENU":
                        current_state = MAIN_MENU

        # Update game logic based on current state
        if current_state == PLAYING:

            for enemy in enemy_group:
                enemy_bullet = enemy.shoot()
                if enemy_bullet:
                    enemy_bullet_group.add(enemy_bullet)
            
            boss = current_level.get_boss() if current_level else None
            if boss and not boss.is_defeated():
                boss_bullet = boss.update_shooting(dt)
                if boss_bullet:
                    if isinstance(boss_bullet, list):
                        for bullet in boss_bullet:
                            enemy_bullet_group.add(bullet)
                    else:
                        enemy_bullet_group.add(boss_bullet)
                
                if boss not in boss_group:
                    boss_group.add(boss)

            for bullet in bullet_group:
                hit_enemies = pygame.sprite.spritecollide(bullet, enemy_group, True)
                if hit_enemies:
                    bullet.kill()
                    for enemy in hit_enemies:
                        explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                        explosion_group.add(explosion)
                        current_level.enemy_killed()
            
            if boss and not boss.is_defeated():
                hit_bullets = pygame.sprite.spritecollide(boss, bullet_group, True)
                for bullet in hit_bullets:
                    if not boss.take_damage(1):
                        
                        explosion = Explosion(boss.rect.centerx, boss.rect.centery)
                        explosion_group.add(explosion)
                        current_level.boss_killed()
                        boss_group.remove(boss)
            
            for enemy in enemy_group:
                if enemy.rect.bottom >= screenHeight - 100:  # Near bottom edge
                    explosion = Explosion(player.rect.centerx, player.rect.centery)
                    explosion_group.add(explosion)
                    player.kill()
                    game_over_menu.reset_timer()
                    current_state = GAME_OVER
                    break
            
            # Player-enemy bullet collision (game over)
            if pygame.sprite.spritecollide(player, enemy_bullet_group, True):
                explosion = Explosion(player.rect.centerx, player.rect.centery)
                explosion_group.add(explosion)
                player.kill()
                game_over_menu.reset_timer()
                current_state = GAME_OVER
            
            # Check for level completion
            if current_level and current_level.is_level_complete():
                level_manager.mark_level_completed(level_manager.get_current_level_index())
                level_complete_menu.set_level_info(
                    current_level.level_number,
                    current_level.get_level_name()
                )
                current_state = LEVEL_COMPLETE
            
            # Update all game sprites
            player_group.update()
            bullet_group.update()
            enemy_group.update()
            enemy_bullet_group.update()
            explosion_group.update()
            boss_group.update(dt)  # Boss group needs dt for timing
            
            # Update level
            if current_level is not None:
                current_level.update()
        
        elif current_state == GAME_OVER:
            # Only update explosions in game over state
            explosion_group.update()
            game_over_menu.update(dt)
        
        elif current_state == LEVEL_COMPLETE:
            # Update explosions and level complete menu timer
            explosion_group.update()
            level_complete_menu.update(dt)

        # Drawing
        draw_bg()
        
        if current_state in [PLAYING, PAUSED, GAME_OVER, LEVEL_COMPLETE]:
            # Draw game objects
            player_group.draw(screen)
            bullet_group.draw(screen)
            enemy_group.draw(screen)
            enemy_bullet_group.draw(screen)
            explosion_group.draw(screen)
            boss_group.draw(screen)  # Draw bosses
            
            # Draw boss HP bar if boss exists
            if current_state == PLAYING and current_level:
                boss = current_level.get_boss()
                if boss and not boss.is_defeated():
                    # Draw boss HP bar at top of screen
                    boss_name = boss.get_boss_name()
                    boss_text = small_font.render(f"Boss: {boss_name}", True, (255, 255, 255))
                    screen.blit(boss_text, (screenWidth // 2 - boss_text.get_width() // 2, 10))
                    boss.draw_hp_bar(screen, screenWidth // 2 - 100, 35, 200, 15)
            
            # Draw level info HUD during gameplay
            if current_state == PLAYING and current_level is not None:
                level_info = f"Level {current_level.level_number}: {current_level.get_level_name()}"
                level_text = small_font.render(level_info, True, (255, 255, 255))
                screen.blit(level_text, (10, 10))
                
                # Draw enemy count (only if no boss or boss not spawned)
                boss = current_level.get_boss()
                if not boss:
                    progress = current_level.get_progress()
                    enemy_text = small_font.render(f"Enemies: {len(enemy_group)}/{progress[1]}", True, (255, 255, 255))
                    screen.blit(enemy_text, (10, 40))
        
        # Draw menus on top
        if current_state == MAIN_MENU:
            main_menu.draw(screen)
        elif current_state == LEVEL_SELECT:
            level_select_menu.draw(screen)
        elif current_state == PAUSED:
            pause_menu.draw(screen)
        elif current_state == GAME_OVER:
            game_over_menu.draw(screen)
        elif current_state == LEVEL_COMPLETE:
            level_complete_menu.draw(screen)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
