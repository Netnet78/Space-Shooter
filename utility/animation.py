import pygame
from pygame.locals import *
import utility.utility as utility

pygame.init()
SCALE_FACTOR = 4


def load_sprite_frames(is_folder, sprites, default=None):
    if not sprites:
        return default
    sprites = sprites if is_folder is False else utility.load_sprites(sprites)
    return sprites


class BaseAnimation(pygame.sprite.Sprite):
    def __init__(self,is_folder=False, sprites=None ,hover_sprites=None ,press_sprites=None ,animation_speed=0.1):
        super().__init__()
        self.is_folder = is_folder
        self.sprite_frames = load_sprite_frames(is_folder, sprites)
        self.hover_frames = load_sprite_frames(is_folder, hover_sprites, self.sprite_frames)
        self.press_frames = load_sprite_frames(is_folder, press_sprites, self.sprite_frames)
        self.current_frame = 0
        self.current_sprite = self.sprite_frames[int(self.current_frame)] if is_folder else self.sprite_frames
        self.position = None
        self.fade_alpha = 0
        self.sprite_rect = None
        self.is_hovering = False
        self.animation_speed = animation_speed
        self.animation_done = False
        self.is_clicked = False

    def handle_mouse_interaction(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        if self.sprite_rect.collidepoint(mouse_pos):
            self.is_hovering = True
            return self.press_frames if mouse_click is True else self.hover_frames
        
        self.is_hovering = False
        return self.sprite_frames

    def scale_sprite(self, surface, scale_factor):

        if not self.sprite_frames:
            return

        scale_factor = max(0.1, scale_factor)
        current_scale = getattr(self, 'current_scale', 1.0)
        
        if self.is_folder is True:
            for frames in [self.sprite_frames, self.hover_frames, self.press_frames]:
                if frames:
                    for i, frame in enumerate(frames):
                        original_size = (frame.get_width() / current_scale, frame.get_height() / current_scale)
                        new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                        frames[i] = pygame.transform.scale(frame, new_size)
        else:
            original_size = (self.sprite_frames.get_width() / current_scale, self.sprite_frames.get_height() / current_scale)
            new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
            self.sprite_frames = pygame.transform.scale(self.sprite_frames, new_size)
        
        self.current_scale = scale_factor
        self.current_sprite = self.sprite_frames[int(self.current_frame)] if self.is_folder else self.sprite_frames
        self.sprite_rect = self.current_sprite.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))


class Float(BaseAnimation):
    def __init__(self, is_folder=False, sprites="", hover_sprites=None, clicked_sprites=None, speed=0.1, x=0):
        super().__init__(is_folder, sprites, hover_sprites, clicked_sprites, speed)
        self.x_position = x
        
    def start_animation(self, surface, start_height, target_height, speed):
        self.start_y = start_height
        self.target_y = target_height
        if self.position is None:
            self.position = [self.x_position, utility.get_center(surface, self.current_sprite)[1]]
            self.position[1] = start_height
        
        if self.position[1] > target_height:
            distance = self.position[1] - target_height
            self.position[1] -= distance * speed
            self.animation_done = True

    def update(self, surface):
        surface.blit(self.current_sprite, self.position)

    def update_sprite(self, surface):
        if not self.animation_done:
            self.fade_alpha = min(255, self.fade_alpha + 3)
            self.current_sprite.set_alpha(self.fade_alpha)
        surface.blit(self.current_sprite, self.position)

    def update_animation(self):
        if self.animation_done:
            if self.is_folder:
                self.current_frame = (self.current_frame + self.animation_speed) % len(self.sprite_frames)
                self.current_sprite = self.sprite_frames[int(self.current_frame)]
            else:
                self.current_frame = self.current_frame + self.animation_speed
                self.current_sprite = self.sprite_frames

            self.current_sprite.set_alpha(255)
            self.position[1] -= 1

            if self.position[1] < self.target_y:
                self.position[1] = self.target_y
                self.animation_done = True

    def after_animation(self, surface):
        if self.animation_done:
            self.current_frame = (self.current_frame + self.animation_speed) % len(self.sprite_frames) if self.is_folder else self.current_frame
            self.current_sprite = self.sprite_frames[int(self.current_frame)] if self.is_folder else self.sprite_frames
            self.current_sprite.set_alpha(255)
            self.center = utility.get_center(surface, self.current_sprite)
            self.position[0] = self.center[0]


class Slide(BaseAnimation):
    def __init__(self, is_folder=False, sprites=str or list or tuple, hover_sprites=None, clicked_sprites=None, y=0):
        super().__init__(is_folder, sprites, hover_sprites, clicked_sprites)
        self.y = y

    def start_animation(self, start_width, target_width, speed=0.05):
        if self.position is None:
            self.position =[start_width, self.y]

        if self.position[0] != target_width:
            distance = abs(target_width - self.position[0])
            self.position[0] += (target_width - self.position[0]) * speed
            self.animation_done = True

    def after_animation(self):
        if self.animation_done:
            self.current_frame = (self.current_frame + self.animation_speed) % len(self.sprite_frames) if self.is_folder else self.current_frame
            self.current_sprite = self.sprite_frames[int(self.current_frame)] if self.is_folder else self.sprite_frames
            self.current_sprite.set_alpha(255)

    def update_sprite(self, surface):
        if not self.position:
            return
            
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        self.sprite_rect.topleft = self.position
        
        frames = self.sprite_frames
        if self.sprite_rect.collidepoint(mouse_pos):
            self.is_hovering = True
            frames = self.press_frames if mouse_click else self.hover_frames
            self.is_clicked = mouse_click
        else:
            self.is_hovering = False

        if not self.animation_done:
            self.fade_alpha = min(255, self.fade_alpha + 3)
            self.current_sprite.set_alpha(self.fade_alpha)
        
        if self.is_folder:
            self.current_frame = (self.current_frame + self.animation_speed) % len(frames)
            self.current_sprite = frames[int(self.current_frame)]
        
        surface.blit(self.current_sprite, self.position)


class FadeIn(BaseAnimation):
    def __init__(self, is_folder=False, sprites=str or list or tuple, fade_duration=1000, x=0, y=0):
        super().__init__(is_folder, sprites)
        self.x = x
        self.y = y
        self.fade_duration = fade_duration
        self.alpha = 0
        self.done_animated = False

    def start_animation(self, screen):
        if self.alpha < 255 and not self.done_animated:
            self.alpha += min(5, 255 // self.fade_duration)
            alpha = self.alpha
        else:
            self.done_animated = True
            alpha = 255
            
        if self.is_folder:
            for image in self.sprite_frames:
                image.set_alpha(alpha)
                screen.blit(image, (self.x, self.y))
        else:
            self.sprite_frames.set_alpha(alpha)
            screen.blit(self.sprite_frames, (self.x, self.y))


class FadeOut(FadeIn):
    def __init__(self, is_folder=False, sprites=str or list or tuple, fade_duration=1000, x=0, y=0):
        super().__init__(is_folder, sprites, fade_duration, x, y)
        self.alpha = 255
        self.done_animated = False

    def start_animation(self, screen):
        if self.alpha > 0 and not self.done_animated:
            self.alpha -= (255 * -self.fade_duration)
            alpha = self.alpha
        else:
            self.done_animated = True
            alpha = 0
            
        if self.is_folder is True:
            for image in self.sprite_frames:
                image.set_alpha(alpha)
                screen.blit(image, (self.x, self.y))
        else:
            self.sprite_frames.set_alpha(alpha)
            screen.blit(self.sprite_frames, (self.x, self.y))