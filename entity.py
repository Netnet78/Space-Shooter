import pygame
import math
import random
from pygame.locals import *
from obstacles import Bullet

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("Player.png")
        self.image = pygame.transform.scale(self.original_image, (50, 50))  # Initial scaling
        self.rect = self.image.get_rect(center=(520, 320))
        self.hitbox = pygame.Rect(self.rect.centerx - 20, self.rect.centery - 20, 40, 40)  # Hitbox of the player
        self.bullets = pygame.sprite.Group()  # Initialize the bullets group
        self.last_angle = 0  # Store the last angle the player was facing
        self.bullet_cooldown = 350  # Cooldown in milliseconds
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_sfx = pygame.mixer.Sound("sfx/laserShoot.wav")
        self.hit_ship = pygame.mixer.Sound("sfx/explosion.wav")
        self.death_sound = pygame.mixer.Sound("sfx/player_explode.wav")
        self.player_score = 0
        self.player_dead = False

    def update(self, enemies):
        if self.player_dead:  # Check if the player is dead  
            return # If the player is dead then return True
        
        # Update hitbox
        self.hitbox.center = self.rect.center

        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate direction and distance to the mouse
        direction_x, direction_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        distance = math.hypot(direction_x, direction_y)

        if distance > 40:  # To avoid division by zero
            # Normalize direction
            direction_x, direction_y = direction_x / distance, direction_y / distance

            # Calculate the angle for rotation
            angle = (180 / math.pi) * -math.atan2(direction_y, direction_x) - 90  # Adjust by 90 degrees
            self.last_angle = angle  # Update the last angle when the player moves

            # Rotate the scaled image
            scaled_image = pygame.transform.scale(self.original_image, (50, 50))  # Scaling the image
            self.image = pygame.transform.rotate(scaled_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)  # Update rect to keep the center

            # Move the player towards the mouse
            move_step = 5  # Movement step size
            if distance <= move_step:
                move_step = distance  # Adjust step size to stop exactly at the cursor

            self.rect.move_ip(direction_x * move_step, direction_y * move_step)
        else:
            # If the player is not moving, use the last angle
            angle = self.last_angle

        # Fire bullets
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_shot_time >= self.bullet_cooldown:
            self.bullet = Bullet(self.rect.centerx, self.rect.centery, (180 / math.pi) * math.atan2(direction_y, direction_x))
            self.bullets.add(self.bullet)
            self.last_shot_time = self.current_time  # Update the last shot time
            self.shoot_sfx.play()

        # Update the bullets
        self.bullets.update()

        # Check collisions with enemies
        for bullet in self.bullets:
            enemies_hit = pygame.sprite.spritecollide(bullet, enemies, True)
            if enemies_hit:
                self.player_score += len(enemies_hit)  # Update the score for each enemy hit
                self.hit_ship.play()  # Play the explosion sound
                bullet.kill()

        hits = pygame.sprite.spritecollide(self, enemies, False)  # False to not delete on collision
        if hits:
            self.handle_collision(hits[0])
            self.death_sound.play()

    def handle_collision(self, enemy):
        # Handle what happens when the player collides with an enemy
        print("Player got hit!")
        self.player_dead = True

    def draw_self(self, surface):
        surface.blit(self.image, self.rect)
        # Draw bullets
        self.bullets.draw(surface)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player = Player()
        self.original_image = pygame.image.load("Enemy.png")
        self.scaled_image = pygame.transform.scale(self.original_image, (50, 50))  # Scaling the image
        self.image = self.scaled_image
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(self.rect.centerx - 20, self.rect.centery - 20, 40, 40)  # Hitbox of the enemy
        self.position = [1400,0]
        self.rect.center = (random.choice(self.position), random.randint(0, 800) * 2)  # Start at a random position

    def move_towards_player(self, player):
        # Calculate direction towards the player
        direction_x, direction_y = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        distance = math.hypot(direction_x, direction_y)

        if distance > 0:  # To avoid division by zero
            # Normalize the direction
            direction_x /= distance
            direction_y /= distance

            # Move the enemy towards the player
            move_step = 2  # Enemy movement speed
            self.rect.move_ip(direction_x * move_step, direction_y * move_step)

            # Update the hitbox position to match the enemy's position
            self.hitbox.center = self.rect.center

            # Rotate to face the player
            angle = (180 / math.pi) * -math.atan2(direction_y, direction_x) - 90
            self.image = pygame.transform.rotate(self.scaled_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, player):
        self.move_towards_player(player)
