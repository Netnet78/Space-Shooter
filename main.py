import pygame
import sys
from entity import Player, Enemy

pygame.init()
pygame.font.init()

# Scaling
SCALE_FACTOR = 2

# Fonts
my_font = pygame.font.SysFont('Comic Sans MS', 20 * SCALE_FACTOR)
game_over_font = pygame.font.SysFont('Comic Sans MS', 60 * SCALE_FACTOR)
retry = pygame.font.SysFont('Comic Sans MS', 18 * SCALE_FACTOR)

pygame.display.set_caption("Classic Space Shooter")
screen_width = 1400
screen_height = 800
WINDOW = pygame.display.set_mode((screen_width, screen_height))

# Background image
background_image = pygame.image.load("assets/Space Background.png").convert()
game_background = pygame.transform.scale(background_image,(screen_width * 14, screen_height * 14))
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

P1 = Player()
enemies = pygame.sprite.Group()

# Variables for enemy respawn
respawn_delay = 2000  # Delay in milliseconds (2 seconds)
last_respawn_time = pygame.time.get_ticks()

# Create initial enemies
for _ in range(1):  # Start with a few enemies
    enemy = Enemy()
    enemies.add(enemy)

def update_map():
    global map_x, map_y

    mouse_x, mouse_y = pygame.mouse.get_pos()
    direction_x = (mouse_x - screen_width // 2) / screen_width
    direction_y = (mouse_y - screen_height // 2) / screen_height

    map_speed = 7 * SCALE_FACTOR

    # Update map position
    new_map_x = map_x - direction_x * map_speed
    new_map_y = map_y - direction_y * map_speed

    # Ensure the map stays within the boundaries
    map_x = max(-(MAP_WIDTH + 10 - screen_width), min(10, new_map_x))
    map_y = max(-(MAP_HEIGHT + 10 - screen_height), min(10, new_map_y))

def show_game_over():
    WINDOW.fill(BLACK)
    game_over_surface = game_over_font.render('Game Over', True, RED)
    score_surface = my_font.render(f"Score: {P1.player_score}", True, WHITE)
    retry_surface = retry.render("Press \"R\" to retry!", True, WHITE)
    game_over_rect = game_over_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
    score_rect = score_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 30))
    retry_rect = retry_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 60))
    WINDOW.blit(game_over_surface, game_over_rect)
    WINDOW.blit(score_surface, score_rect)
    WINDOW.blit(retry_surface, retry_rect)
    pygame.display.update()
    
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
        update_map()

        # Draw background
        WINDOW.blit(game_background, (map_x, map_y))
        
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
            last_respawn_time = current_time  # Update the last respawn time

    else:
        # Handle game over
        if handle_game_over():
            # Restart game logic
            P1 = Player()  # Recreate the player
            enemies.empty()  # Remove all enemies
            for _ in range(1):  # Recreate initial enemies
                enemy = Enemy()
                enemies.add(enemy)

    pygame.display.update()
    FramesPerSecond.tick(FPS)
