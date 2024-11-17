import pygame
from pygame.locals import *
import sys
import ui_components.Header as Header
import ui_components.Buttons as Buttons

pygame.init()

screen_width = 1400
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Fonts
my_font = pygame.font.SysFont('Comic Sans MS', 20)

class Startup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.header = Header.Render(screen)
        self.play_button = Buttons.PlayButton(screen)
        self.option_button = Buttons.OptionButton(screen)
        self.exit_button = Buttons.ExitButton(screen)
    
    def update(self):

        # Header
        self.header.initialize()

        # Buttons
        self.play_button.initialize(2000, (screen_width // 2) - (88 / 0.7), 340, 0.05)
        self.option_button.initialize(2000, (screen_width // 2) - (88 / 0.7), 465, 0.04)
        self.exit_button.initialize(2000, (screen_width // 2) - (88 / 0.7), 590, 0.03)

class UI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pass


if __name__ == "__main__":
    
    startup = Startup()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        # Clear the screen
        screen.fill((0,0,0))
        startup.update()

        pygame.display.flip()
        clock.tick(60)
    
