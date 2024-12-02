import pygame
from pygame.locals import *
from utility import animation, utility
import font_manager

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

font = font_manager.font

SCALE_FACTOR = utility.SCALE_FACTOR - 1

class Initialize():
    def __init__(self, screen=pygame.display.set_mode((1400, 800))):
        super().__init__()
        self.screen = screen
        self.game_text = pygame.image.load("assets/Game over screen/GAME.png").convert_alpha()
        self.over_text = pygame.image.load("assets/Game over screen/OVER.png").convert_alpha()
        self.game_text = pygame.transform.scale(self.game_text, (self.game_text.get_width() * SCALE_FACTOR, self.game_text.get_height() * SCALE_FACTOR))
        self.over_text = pygame.transform.scale(self.over_text, (self.over_text.get_width() * SCALE_FACTOR, self.over_text.get_height() * SCALE_FACTOR))
        self.game_position = ((screen.get_width() // 2) - self.game_text.get_width() - 50, screen.get_height() // 2)
        self.over_position = ((screen.get_width() // 2) + 50 , screen.get_height() // 2)
        self.game_text_float = animation.Float(False, self.game_text, speed=0.1, x=self.game_position[0])
        self.over_text_float = animation.Float(False, self.over_text, speed=0.1, x=self.over_position[0])
        self.showed_game_over = False
        self.audio = pygame.mixer.Sound("sfx/game_over.wav")
        self.start_time = pygame.time.get_ticks()

    def game_over_text(self, delay=1000):
        current_time = pygame.time.get_ticks() - self.start_time
        if not self.showed_game_over:
            self.game_text.set_alpha(255)
            self.screen.blit(self.game_text, self.game_position)
            
            if current_time >= delay:
                self.over_text.set_alpha(255)
                self.screen.blit(self.over_text, self.over_position)
                self.showed_game_over = True

    def float_effect(self, screen):
        if self.showed_game_over:
            if pygame.time.get_ticks() - self.start_time < 2000:
                self.game_text.set_alpha(255)
                self.screen.blit(self.game_text, self.game_position)
                self.over_text.set_alpha(255)
                self.screen.blit(self.over_text, self.over_position)

            if pygame.time.get_ticks() - self.start_time >= 2000:
                self.game_text_float.start_animation(screen, self.game_position[1], self.game_position[1] - 300, 0.05)
                self.over_text_float.start_animation(screen, self.over_position[1], self.over_position[1] - 300, 0.05)
                self.game_text_float.update(screen)
                self.over_text_float.update(screen)

    def play_audio(self):
        self.audio.set_volume(1)
        if not pygame.mixer.get_busy():
            self.audio.play()
        if pygame.time.get_ticks() - self.start_time >= 2100:
            self.audio.stop()

    def render(self, screen):
        self.game_over_text()
        self.float_effect(screen)
