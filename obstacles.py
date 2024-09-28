import pygame
import math

RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0,255,0)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        
        # Calculate bullet velocity based on the angle
        self.angle = math.radians(angle)
        self.velocity_x = math.cos(self.angle) * self.speed
        self.velocity_y = math.sin(self.angle) * self.speed

    def update(self):
        # Move the bullet in the direction of its velocity
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Remove the bullet if it goes off-screen
        if self.rect.right < 0 or self.rect.left > 1400 or self.rect.bottom < 0 or self.rect.top > 800:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self,x,y,angle):
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.image.fill(ORANGE)
        self.rect =self.image.get_rect(center=(x,y))
        self.speed = 8
