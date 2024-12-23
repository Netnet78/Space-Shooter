import pygame
import sys
from entity import Player, Enemy
import assets
import ui

pygame.init()
pygame.font.init()

# Scaling
SCALE_FACTOR = ui.SCALE_FACTOR

# Fonts
my_font = pygame.font.SysFont('Comic Sans MS', 20 * SCALE_FACTOR)
game_over_font = pygame.font.SysFont('Comic Sans MS', 60 * SCALE_FACTOR)
retry = pygame.font.SysFont('Comic Sans MS', 18 * SCALE_FACTOR)

pygame.display.set_caption("Space shooter")
screen_width = 1400
screen_height = 800
WINDOW = pygame.display.set_mode((screen_width, screen_height))

# Background image
background_image = pygame.image.load("assets/Space Background.png").convert()
game_background = pygame.transform.scale(background_image,(screen_width * 10, screen_height * 12))

map_rect = game_background.get_rect()
MAP_WIDTH = game_background.get_width()
MAP_HEIGHT = game_background.get_height()
map_x = -MAP_WIDTH//2 + screen_width//2
map_y = -MAP_HEIGHT//2 + screen_height//2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

FPS = 60
FramesPerSecond = pygame.time.Clock()

# User interface initialization


# Game map initialization
game_map = assets.GameMap(game_background,WINDOW)

# Entity initialization
P1 = Player()
enemies = pygame.sprite.Group()

# Variables for enemy respawn
respawn_delay = 2000  # Delay in milliseconds (2 seconds)
last_respawn_time = pygame.time.get_ticks()

# Create initial enemies
for _ in range(1):  # Start with a few enemies
    enemy = Enemy()
    enemies.add(enemy)

def show_game_over():
    WINDOW.fill(BLACK)

    pygame.display.flip()
    
def handle_game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    return True
                    
        # Show the game over screen
        show_game_over()
        return False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not P1.player_dead:
        # Update player and enemies
        P1.update(enemies)
        for enemy in enemies:
            enemy.update(P1)

        # Clear screen
        WINDOW.fill(BLACK)

        # Update map position
        game_map.render()
        game_map.update(7 * SCALE_FACTOR)
        
        # Draw everything
        P1.draw_self(WINDOW)
        enemies.draw(WINDOW)

        # Draw the score text
        score_text = f"Score: {P1.player_score}"
        text_surface = my_font.render(score_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(screen_width // 2, 30))  # Center horizontally, adjust vertical position if needed
        WINDOW.blit(text_surface, text_rect)

        # Respawn enemies if necessary
        current_time = pygame.time.get_ticks()
        if len(enemies) == 0 or (current_time - last_respawn_time >= respawn_delay and len(enemies) < 5):
            new_enemy = Enemy()
            enemies.add(new_enemy)
            last_respawn_time = current_time  # Update the last respawn times

    if P1.player_dead:
        # Handle game over
        game_over = ui.GameOver(WINDOW, 0)
        game_over.update()
        if handle_game_over():
            # Restart game logic
            P1 = Player()  # Recreate the player
            enemies.empty()  # Remove all enemies
            
            for _ in range(1):  # Recreate initial enemies
                enemy = Enemy()
                enemies.add(enemy)

    pygame.display.flip()
    FramesPerSecond.tick(FPS)
