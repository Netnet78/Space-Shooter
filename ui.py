import pygame
from pygame.locals import *
import sys, os
import ui_components.Buttons
import ui_components.Header as Header
import ui_components.Buttons as Buttons
import ui_components.RetryText
from utility import animation
import font_manager
import ui_components.GameOver
import ui_components.YesNo

pygame.init()

screen_width = 1400
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Fonts
SCALE_FACTOR = int(2)
font= font_manager.font

# Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Startup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.header = Header.Render(screen)
        self.play_button = Buttons.PlayButton(screen)
        self.option_button = Buttons.OptionButton(screen)
        self.exit_button = Buttons.ExitButton(screen)
    
    def render(self):

        # Header
        self.header.initialize()

        # Buttons
        self.play_button.initialize(2000, (screen_width // 2) - (88 / 0.7), 0.05)
        self.option_button.initialize(2000, (screen_width // 2) - (88 / 0.7), 0.04)
        self.exit_button.initialize(2000, (screen_width // 2) - (88 / 0.7), 0.03)

class UI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pass

class GameOver(pygame.sprite.Sprite):
    def __init__(self,screen, score=0):
        super().__init__()
        self.screen = screen
        self.score = score
        self.game_over_text = ui_components.GameOver.Initialize(self.screen)
        self.retry_text = ui_components.RetryText.Initialize(self.screen)
        self.yes_text = ui_components.YesNo.YesText(self.screen)
        self.no_text =ui_components.YesNo.NoText(self.screen)

    def update(self):
        self.game_over_text.render(self.screen)
        self.game_over_text.play_audio()

        # Retry Text
        if pygame.time.get_ticks() >= 3000:
            self.retry_text.start()
        
        # Yes and No buttons
        if pygame.time.get_ticks() >= 4000:
            self.yes_text.start()
            if pygame.time.get_ticks() >= 5000:
                self.no_text.start()

if __name__ == "__main__":
    
    startup = Startup()
    game_over = GameOver(screen, 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Clear the screen
        screen.fill((0,0,0))
        startup.render()

        pygame.display.flip()
        clock.tick(60)
    
