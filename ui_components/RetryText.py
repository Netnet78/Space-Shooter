import pygame
from pygame.locals import *
import utility.animation as ani


# Retry button sprites
retry_sprite_folder = "assets/Game over screen/Retry"


class Initialize(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.sprites = retry_sprite_folder
        self.animation = ani.Float(True,self.sprites,x=580)
        self.animation_speed = 0.05

    def start(self):
        self.animation.scale_sprite(self.screen,0.9)
        self.animation.start_animation(self.screen,
            self.screen.get_width() + 100, 250, self.animation_speed)
        self.animation.update(self.screen)
        self.animation.after_animation(self.screen)


