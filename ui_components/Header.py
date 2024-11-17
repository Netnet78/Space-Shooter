import pygame
from pygame.locals import *
import utility.animation as ani

pygame.init()
sprite_folder = "assets/Heading Space Shooting"

class Render:
    """
    Renders the header animation on the screen.
        
    The `Render` class is responsible for initializing and updating the header animation. It takes a `screen` object as a parameter, which is used to display the animation.
        
    The `initialize()` method starts the header animation by calling `start_animation()` on the `header` animation object. It then updates the sprite and calls `after_animation()` to complete the animation.
    """
        
    def __init__(self,screen):
        super().__init__()
        self.sprite_folder = sprite_folder
        self.screen = screen
        self.header_animation = ani.Float(self.sprite_folder)
        self.animation_speed = 0.05

    def initialize(self):
        self.header_animation.start_animation(self.screen, 
            self.screen.get_width() + 100, 40, self.animation_speed)
        self.header_animation.update_sprite(self.screen)
        self.header_animation.after_animation(self.screen)