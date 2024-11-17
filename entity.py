import pygame
import math
import random
from pygame.locals import *
from obstacles import Bullet

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCALE_FACTOR = 2
screen_width = 1400
screen_height = 800


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load and scale the original image once
        self.original_image = pygame.image.load("assets/ships/Blue.png").convert_alpha()
        self.scaled_image = pygame.transform.scale(self.original_image, 
            (32 * SCALE_FACTOR, 
             32 * SCALE_FACTOR))
        self.image = self.scaled_image
        self.rect = self.image.get_rect(center=(520, 320))
        self.hitbox = pygame.Rect(self.rect.centerx - 20 * SCALE_FACTOR, 
                                self.rect.centery - 20 * SCALE_FACTOR, 
                                40 * SCALE_FACTOR, 40 * SCALE_FACTOR)
        
        # Initialize game components
        self.bullets = pygame.sprite.Group()
        self.last_angle = 0
        self.bullet_cooldown = 350
        self.last_shot_time = pygame.time.get_ticks()
        
        # Load sounds
        self.shoot_sfx = pygame.mixer.Sound("sfx/laserShoot.wav")
        self.hit_ship = pygame.mixer.Sound("sfx/explosion.wav")
        self.death_sound = pygame.mixer.Sound("sfx/player_explode.wav")
        
        self.player_score = 0
        self.player_dead = False

    def update(self, enemies):
        if self.player_dead:
            return

        # Keep player fixed at center
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.hitbox.center = self.rect.center

        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Calculate direction for rotation only
        direction_x = mouse_x - self.rect.centerx
        direction_y = mouse_y - self.rect.centery
        
        # Calculate rotation angle
        angle = (180 / math.pi) * -math.atan2(direction_y, direction_x) - 90
        self.last_angle = angle
        
        # Rotate the scaled image
        self.image = pygame.transform.rotate(self.scaled_image, angle)
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))

        # Handle shooting
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_shot_time >= self.bullet_cooldown:
            self.bullet = Bullet(self.rect.centerx, self.rect.centery, 
                               (180 / math.pi) * math.atan2(direction_y, direction_x))
            self.bullets.add(self.bullet)
            self.last_shot_time = self.current_time
            self.shoot_sfx.play()

        # Update bullets and check collisions
        self.bullets.update()
        for bullet in self.bullets:
            enemies_hit = pygame.sprite.spritecollide(bullet, enemies, True)
            if enemies_hit:
                self.player_score += len(enemies_hit)
                self.hit_ship.play()
                bullet.kill()

        if pygame.sprite.spritecollide(self, enemies, False):
            self.handle_collision(enemies.sprites()[0])
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
        # Load and scale enemy image
        self.original_image = pygame.image.load("Enemy.png").convert_alpha()
        self.scaled_image = pygame.transform.scale(self.original_image, 
            (32 * SCALE_FACTOR, 32 * SCALE_FACTOR))
        self.image = self.scaled_image
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(self.rect.centerx - 20 * SCALE_FACTOR, 
                                self.rect.centery - 20 * SCALE_FACTOR,
                                40 * SCALE_FACTOR, 40 * SCALE_FACTOR)
        
        # Set random starting position
        self.position = [1400, 0]
        self.rect.center = (random.choice(self.position), random.randint(0, 800))
        self.current_speed = 0
    
    def smooth_transition(self, current, target, step):
        if current < target:
            current += step
            if current > target:
                current = target
        else:
            current -= step
            if current < target:
                current = target
        return current        

    def move_towards_player(self, player):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Calculate player's movement vector from mouse position
        player_direction_x = mouse_x - screen_width//2
        player_direction_y = mouse_y - screen_height//2
        
        # Calculate vector to player
        direction_x = player.rect.centerx - self.rect.centerx
        direction_y = player.rect.centery - self.rect.centery
        distance = math.hypot(direction_x, direction_y)
        
        if distance > 0:
            # Normalize vectors
            direction_x /= distance
            direction_y /= distance
            
            player_speed = math.hypot(player_direction_x, player_direction_y)
            if player_speed > 0:
                player_direction_x /= player_speed
                player_direction_y /= player_speed
                
                # Calculate relative movement direction
                dot_product = (direction_x * player_direction_x + direction_y * player_direction_y)
                
                # Base movement speed
                self.base_speed = 1.5 * SCALE_FACTOR
                speed_multiplier = 1

                # Check for close range and adjust speed
                min_distance = 100 * SCALE_FACTOR
                if distance < min_distance:
                    speed_multiplier *= (distance / min_distance)

                target_speed = None
                if player_speed > 300:
                    # When heading towards each other (dot product negative)
                    if dot_product < -0.1:
                        target_speed = 2.75  # Speed up significantly
                    else:
                        target_speed = -1.0  # Move backwards when player moving away
                elif player_speed > 150 and player_speed < 300:
                    if dot_product < -0.1:
                        target_speed = 2.0  # Speed up moderately
                    else:
                        target_speed = 1.5  # Normal forward speed
                else:
                    target_speed = 2.0  # Base pursuit speed
                
                # Adjust speed based on relative movement
                # if (player_speed > 6):  # Only adjust speed when player is moving significantly
                #     if dot_product > 0.7:  # Moving same direction
                #         speed_multiplier = 0.5  # Slower speed
                #     elif dot_product < -0.7:  # Head-on approach
                #         speed_multiplier = 1.25  # Faster speed
                #     else:  # Moving at angles
                #         speed_multiplier = 1
                # if player_speed > 300:  # Player moving at medium speed
                #     if dot_product < 0.7:  # Head-on approach
                #         speed_multiplier = 2.75  # Faster when heading towards each other
                #     else:
                #         speed_multiplier = -1.0  # Normal pursuit speed
                # if player_speed > 150 and player_speed < 300:  # Player moving slowly or stationary
                #     if dot_product < 0.7:  # Head-on approach
                #         while True:
                #             if player_speed > 300:
                #                 speed_multiplier -= 0.01
                #                 if speed_multiplier < 2.5:
                #                     speed_multiplier = 2.5 # Faster when heading towards each other
                #                     break
                #             else:
                #                 speed_multiplier += 0.01
                #                 if speed_multiplier > 2.5:
                #                     speed_multiplier = 2.5
                #                     break
                #     else:
                #         speed_multiplier = 2.0
                # if player_speed < 150: # Player moving very slowly
                #     while True:
                #         speed_multiplier -= 0.01 if speed_multiplier > 2.0 else 0.01
                #         if speed_multiplier < 2.0:
                #             speed_multiplier = 2.0
                #             break

                self.current_speed = self.smooth_transition(self.current_speed, target_speed, 1)
                
                self.move_step = self.base_speed * self.current_speed
                self.move_x = direction_x * self.move_step
                self.move_y = direction_y * self.move_step
                self.rect.move_ip(self.move_x, self.move_y)
                self.hitbox.center = self.rect.center
                
                # Rotate to face the player
                self.angle = (180 / math.pi) * -math.atan2(direction_y, direction_x) - 90
                self.image = pygame.transform.rotate(self.scaled_image, self.angle)
                self.rect = self.image.get_rect(center=self.rect.center)
                
    def update(self, player):
        self.move_towards_player(player)
