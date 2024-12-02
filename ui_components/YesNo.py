import pygame
import utility.animation as animation

sprite_path = "assets/Game over screen/YES.png"


class YesText():
    def __init__(self,screen):
        super().__init__()
        self.screen = screen
        self.sprite = pygame.image.load(sprite_path)
        self.animation = animation.Slide(False,sprites=self.sprite,y=500)

    def start(self):
        self.animation.start_animation(self.screen, 0, 300)
        self.animation.scale_sprite(self.screen, 3)
        self.animation.after_animation()
        self.animation.update_sprite(self.screen)


class NoText(YesText):
    def __init__(self, screen):
        super().__init__(screen)
        self.sprite = pygame.image.load("assets/Game over screen/NO.png")
        self.animation = animation.Slide(False,sprites=self.sprite,y=500)
    
    def start(self):
        self.animation.start_animation(self.screen,1400,1000)
        self.animation.scale_sprite(self.screen, 3)
        self.animation.after_animation()
        self.animation.update_sprite(self.screen)