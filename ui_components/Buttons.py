import pygame
from pygame.locals import *
import utility.animation as animation

pygame.init()

# Essential sprites
play_button_sprites = str("assets/Buttons/Play button")
option_button_sprites = str("assets/Buttons/Option button")
quit_button_sprites = str("assets/Buttons/Exit button")

# Button hovering assets
play_button_hover = str("assets/Buttons/Play button/Hovering")
option_button_hover = str("assets/Buttons/Option button/Hovering")
quit_button_hover = str("assets/Buttons/Exit button/Hovering")

# Button pressing assets
play_button_press = str("assets/Buttons/Play button/Pressing")
option_button_press = str("assets/Buttons/Option button/Pressing")
quit_button_press = str("assets/Buttons/Exit button/Pressing")

# Scale factor
scale_factor = 0.7

class PlayButton(pygame.sprite.Sprite):
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.sprites = play_button_sprites
        self.hover_sprites = play_button_hover
        self.clicked_sprites = play_button_press
        self.animation = animation.Slide(self.sprites, self.hover_sprites, self.clicked_sprites)

    def initialize(self,start_position,end_position, y_position,speed):
        self.animation.scale_sprite(self.screen, scale_factor)
        self.animation.start_animation(self.screen,start_position,end_position, speed)
        self.animation.after_animation(y_position)
        self.animation.update_sprite(self.screen)

class OptionButton(PlayButton):
    def __init__(self,screen):
        super().__init__(screen)
        self.sprites = option_button_sprites
        self.hover_sprites = option_button_hover
        self.clicked_sprites = option_button_press
        self.animation = animation.Slide(self.sprites, self.hover_sprites, self.clicked_sprites)

class ExitButton(PlayButton):
    def __init__(self,screen):
        super().__init__(screen)
        self.sprites = quit_button_sprites
        self.hover_sprites = quit_button_hover
        self.clicked_sprites = quit_button_press
        self.animation = animation.Slide(self.sprites, self.hover_sprites, self.clicked_sprites)
