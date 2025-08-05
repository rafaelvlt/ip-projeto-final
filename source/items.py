import pygame



class Items(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet_item):
        super().__init__()

        self.x = x
        self.y = y
        self.speed = 3
        
        self.frame = pygame.image.load(sheet_item).convert_alpha()
        self.image = self.frame
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def drop(self):
        self.dy = -self.speed
        self.y += self.dy
        pygame.time.delay(500)
        self.dyy = self.speed
        self.y += self.dy


        

