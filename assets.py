import pygame

BLACK = (0,0,0)
WHITE = (255,255,255)

class GameMap:
    def __init__(self, sprite,screen) -> None:
        super().__init__()
        self.sprite = sprite
        self.screen = screen
        self.sprite_rect = self.sprite.get_rect()
        self.sprite_width = self.sprite.get_width()
        self.sprite_height = self.sprite.get_height()
        self.sprite_x = -self.sprite_width // 2 + screen.get_width() // 2
        self.sprite_y = -self.sprite_height // 2 + screen.get_height() // 2

    def update(self, speed):
        mouse_x , mouse_y = pygame.mouse.get_pos()
        direction_x = (mouse_x - self.screen.get_width() // 2) / self.screen.get_width()
        direction_y = (mouse_y - self.screen.get_height() // 2) / self.screen.get_height()
        self.map_speed = speed
        self.new_map_x = self.sprite_x - direction_x * self.map_speed
        self.new_map_y = self.sprite_y - direction_y * self.map_speed

        self.sprite_x = max(-(self.sprite_width + 10 - self.screen.get_width()), min(10,self.new_map_x))
        self.sprite_y = max(-(self.sprite_height + 10 - self.screen.get_height()), min(10,self.new_map_y))

    def render(self):
        self.screen.blit(self.sprite, (self.sprite_x, self.sprite_y))

if __name__ == "__main__":
    pygame.init()