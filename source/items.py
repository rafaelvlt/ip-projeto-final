import pygame
from settings import *



class Items(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet_item):
        super().__init__()

        self.x = x
        self.y = y
        self.y_original = self.y
        self.speed = -5
        self.gravidade = 0.4
        self.dropping = True
        self.frame = pygame.image.load(sheet_item).convert_alpha()
        self.image = self.frame
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, delta_time):
        if self.dropping:
            self.speed += self.gravidade
            self.y += self.speed
            self.rect.y = self.y

            if self.speed > 0 and self.y >= self.y_original:
                self.y = self.y_original
                self.rect.y = self.y
                self.speed = 0
                self.dropping = False
    
        


        

