import pygame
from pygame.locals import *
import os

SCALE_FACTOR = 4

def load_sprites(folder):
    """
    Fetch images inside the folder and sort in order, after that
    it converts png images to have transparent effect then returns
    sprite files inside a list
    """
    sprites = []
    for file in sorted(os.listdir(folder)):
        if file.endswith('.png'):
            sprite_path = os.path.join(folder, file)
            sprite = pygame.image.load(sprite_path).convert_alpha()
            scaled_sprite = (sprite.get_width() * SCALE_FACTOR, sprite.get_height() * SCALE_FACTOR)
            sprite = pygame.transform.scale(sprite,scaled_sprite)
            sprites.append(sprite)
    return sprites
        
def get_center(surface,element):
    center_x = (surface.get_width() - element.get_width()) // 2
    center_y = (surface.get_height() - element.get_height()) // 2
    return [center_x, center_y]