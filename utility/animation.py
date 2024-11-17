import pygame
from pygame.locals import *
import os

pygame.init()

def load_sprites(folder):
    sprites = []
    for file in sorted(os.listdir(folder)):
        if file.endswith('.png'):
            sprite_path = os.path.join(folder, file)
            sprite = pygame.image.load(sprite_path).convert_alpha()
            scaled_sprite = (sprite.get_width() * 4, sprite.get_height() * 4)
            sprite = pygame.transform.scale(sprite,scaled_sprite)
            sprites.append(sprite)
    return sprites
        
def get_center(surface,element):
    center_x = (surface.get_width() - element.get_width()) // 2
    center_y = (surface.get_height() - element.get_height()) // 2
    return [center_x, center_y]

class Float(pygame.sprite.Sprite):
    """
    A sprite class that represents a floating animation effect.

    The Float class is responsible for managing the animation of a sprite that floats upwards on the screen. It loads a set of sprite frames from a folder, and handles the animation logic, including fading in the sprite, smoothly moving it upwards, and cycling through the sprite frames to create a floating effect.

    The class provides the following methods:

    - `__init__(self, sprites)`: Initializes the Float object with the folder containing the sprite frames.
    - `update_sprite(self, surface)`: Draws the current sprite frame on the provided surface, with a fading in effect.
    - `start_animation(self, surface, start_height, target_height)`: Starts the animation by positioning the sprite at the `start_height` and smoothly moving it to the `target_height`.
    - `after_animation(self, surface)`: Handles the floating effect and sprite animation after the upward movement is complete.
    """

    def __init__(self, sprites, hover_sprites=None, clicked_sprites=None):
        super().__init__()
        self.sprite_folder = sprites
        self.sprite_frames = load_sprites(self.sprite_folder)
        if hover_sprites:
            self.hover_frames = load_sprites(hover_sprites)
        else:
            self.hover_frames = self.sprite_frames
        if clicked_sprites:
            self.press_sprite = load_sprites(clicked_sprites)
        else:
            self.press_sprite = self.sprite_frames
        self.current_frame = 0
        self.current_sprite = self.sprite_frames[int(self.current_frame)]
        self.animation_speed = 0.1
        self.position = None
        self.animation_done = False
        self.fade_alpha = 0
        self.is_clicked = False
        self.is_hovering = False
        
    def update_sprite(self, surface):
        if not self.animation_done:
            # Fade in effect
            self.fade_alpha = min(255, self.fade_alpha + 3)
            self.current_sprite.set_alpha(self.fade_alpha)
        surface.blit(self.current_sprite, self.position)

    def start_animation(self,surface,start_height,target_height,speed):
        # Start from bottom of screen
        if self.position is None:
            self.position = get_center(surface,self.current_sprite)
            self.position[1] = start_height  # Start below screen
            
        # Smooth upward movement with easing
        target_y = target_height  # Final Y position
        if self.position[1] > target_y:
            # Smooth easing motion
            distance = self.position[1] - target_y
            self.position[1] -= distance * speed  # Adjust speed here
        
            self.animation_done = True
            
    def after_animation(self, surface):
        if self.animation_done:
            # Floating effect and sprite animation
            self.current_frame = (
                self.current_frame + self.animation_speed
            ) % len(self.sprite_frames)
            self.current_sprite = self.sprite_frames[int(self.current_frame)]
            self.current_sprite.set_alpha(255)
            self.center = get_center(surface,self.current_sprite)
            self.position[0] = self.center[0]  # Keep centered horizontally

class Slide(pygame.sprite.Sprite):
    """
    Initializes the Slide object with the folder containing the sprite frames.
    
    Args:
        sprites (str): The folder containing the sprite frames.
    
    Attributes:
        sprite (str): The folder containing the sprite frames.
        sprite_frames (list): The list of sprite frames loaded from the folder.
        current_frame (float): The current frame index of the animation.
        current_sprite (pygame.Surface): The current sprite frame.
        animation_speed (float): The speed of the animation.
        position (list): The position of the sprite on the screen.
        animation_done (bool): Whether the animation is done.
        fade_alpha (int): The alpha value for the fade-in effect.
    
    Methods:
        start_animation(self, surface, start_width, target_width):
            Starts the animation by positioning the sprite at the `start_width` and smoothly moving it to the `target_width`.

        after_animation(self, y):
            End the animation with the target Y position of the element

        update_sprite(self, surface):
            Update the sprite depending on the mouse state (hovering, pressing or none)

        scale_sprite(self,surface,scale_factor):
            Changes the sprite size depending on the scale factor 

    """
    
    def __init__(self, sprites, hover_sprites=None, clicked_sprites=None):
        super().__init__()
        self.sprite_folder = sprites
        self.sprite_frames = load_sprites(self.sprite_folder)
        if hover_sprites:
            self.hover_frames = load_sprites(hover_sprites)
        else:
            self.hover_frames = self.sprite_frames
        if clicked_sprites:
            self.press_sprite = load_sprites(clicked_sprites)
        else:
            self.press_sprite = self.sprite_frames
            
        self.current_frame = 0
        self.current_sprite = self.sprite_frames[int(self.current_frame)]
        self.sprite_rect = self.current_sprite.get_rect()
        self.animation_speed = 0.1
        self.position = None
        self.animation_done = False
        self.fade_alpha = 0
        self.is_hovering = False
        self.is_clicked = False

    def start_animation(self, surface, start_width, target_width, speed=0.05):
        # Start from bottom of screen
        if self.position is None:
            self.position = get_center(surface, self.current_sprite)
            self.position[0] = start_width

        target_x = target_width  # Final X position
        distance = None
        if self.position[0] > target_x:
            # Smooth easing motion
            distance = self.position[0] - target_x
            self.position[0] -= distance * speed  # Adjust speed here
            self.animation_done = True
        if self.position[0] < target_x:
            # Smooth easing motion
            distance = target_x - self.position[0]
            self.position[0] += distance * speed  # Adjust speed here
            self.animation_done = True

    def after_animation(self, y):
        if self.animation_done:
            # Floating effect and sprite animation
            self.current_frame = (
                self.current_frame + self.animation_speed
            ) % len(self.sprite_frames)
            self.current_sprite = self.sprite_frames[int(self.current_frame)]
            self.current_sprite.set_alpha(255)
            self.position[1] = y

    def update_sprite(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        if self.position:  # Only check collision if position is set
            self.sprite_rect.topleft = self.position
            if self.sprite_rect.collidepoint(mouse_pos):
                self.is_hovering = True
                frames = self.press_sprite if mouse_click else self.hover_frames
                self.is_clicked = True if mouse_click else False
            else:
                self.is_hovering = False
                frames = self.sprite_frames
            
            if not self.animation_done:
                self.fade_alpha = min(255, self.fade_alpha + 3)
                self.current_sprite.set_alpha(self.fade_alpha)
            
            self.current_frame = (self.current_frame + self.animation_speed) % len(frames)
            self.current_sprite = frames[int(self.current_frame)]
            surface.blit(self.current_sprite, self.position)

    def scale_sprite(self, surface, scale_factor):
        # Ensure minimum scale factor
        scale_factor = max(0.1, scale_factor)  # Prevent scaling to zero
        
        # Scale both normal and hover frames
        for self.frames in [self.sprite_frames, self.hover_frames, self.press_sprite]:
            for i in range(len(self.frames)):
                original_width = self.frames[i].get_width() / self.current_scale if hasattr(self, 'current_scale') else self.frames[i].get_width()
                original_height = self.frames[i].get_height() / self.current_scale if hasattr(self, 'current_scale') else self.frames[i].get_height()
                
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                
                self.frames[i] = pygame.transform.scale(self.frames[i], (new_width, new_height))
        
        self.current_scale = scale_factor
        self.current_sprite = self.sprite_frames[int(self.current_frame)]
        self.sprite_rect = self.current_sprite.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
