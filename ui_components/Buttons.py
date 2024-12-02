import pygame
from pygame.locals import *
import utility.animation as animation

# Essential sprites
play_button_sprites = "assets/Buttons/Play button"
option_button_sprites = "assets/Buttons/Option button"
quit_button_sprites = "assets/Buttons/Exit button"

# Button hovering assets
play_button_hover = "assets/Buttons/Play button/Hovering"
option_button_hover = "assets/Buttons/Option button/Hovering"
quit_button_hover = "assets/Buttons/Exit button/Hovering"

# Button pressing assets
play_button_press = "assets/Buttons/Play button/Pressing"
option_button_press = "assets/Buttons/Option button/Pressing"
quit_button_press = "assets/Buttons/Exit button/Pressing"

# Scale factor
scale_factor = 0.7


class PlayButton(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.sprites = play_button_sprites
        self.hover_sprites = play_button_hover
        self.clicked_sprites = play_button_press
        self.animation = animation.Slide(True,self.sprites, self.hover_sprites, self.clicked_sprites, y=340)

    def initialize(self,start_position,end_position, speed):
        self.animation.scale_sprite(self.screen, scale_factor)
        self.animation.start_animation(start_position,end_position, speed)
        self.animation.after_animation()
        self.animation.update_sprite(self.screen)


class OptionButton(PlayButton):
    def __init__(self,screen):
        super().__init__(screen)
        self.sprites = option_button_sprites
        self.hover_sprites = option_button_hover
        self.clicked_sprites = option_button_press
        self.animation = animation.Slide(True,self.sprites, self.hover_sprites, self.clicked_sprites, 465)


class ExitButton(PlayButton):
    def __init__(self,screen):
        super().__init__(screen)
        self.sprites = quit_button_sprites
        self.hover_sprites = quit_button_hover
        self.clicked_sprites = quit_button_press
        self.animation = animation.Slide(True,self.sprites, self.hover_sprites, self.clicked_sprites, 590)



if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()