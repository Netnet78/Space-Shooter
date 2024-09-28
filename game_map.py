import pygame
import random

BLACK = (0,0,0)
WHITE = (255,255,255)

class Starfield:
    def __init__(self, width, height, num_stars, star_image):
        self.width = width
        self.height = height
        self.num_stars = num_stars
        self.star_image = pygame.image.load(star_image).convert_alpha()
        self.stars = [pygame.Rect(random.randint(0, width), random.randint(0, height), 
                                self.star_image.get_width(), self.star_image.get_height()) 
                     for _ in range(num_stars)]

    def draw(self, surface, camera):
        for star_rect in self.stars:
            # Apply camera transformation to star position
            adjusted_star_pos = camera.apply_rect(star_rect).topleft
            surface.blit(self.star_image, adjusted_star_pos)
