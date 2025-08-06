import pygame
from settings import fps, cores
from player import Player
from items import Items

class Game:
    def __init__(self, tela):
        self.tela = tela
        self.clock = pygame.time.Clock() 
        self.running = True

        self.player = Player(x=100, y=100, sheet_player=r'ip-projeto-final\assets\img\player.png')
        self.life_orb = Items(x=300, y=300, sheet_item=r'ip-projeto-final\assets\img\lifeOrb.png')
        self.expShard = Items(x=700, y=500, sheet_item=r'ip-projeto-final\assets\img\expShard.png')
        self.bigShard = Items(x=200, y=400, sheet_item=r'ip-projeto-final\assets\img\bigShard.png')
        self.all_sprites = pygame.sprite.Group() #grupo de sprites
        self.all_sprites.add(self.life_orb)
        self.all_sprites.add(self.expShard)
        self.all_sprites.add(self.bigShard)
        self.item_group = pygame.sprite.Group()#grupo de itens
        self.item_group.add(self.life_orb)
        self.item_group.add(self.expShard)
        self.item_group.add(self.bigShard)

        for item in self.item_group.copy():
            if self.player.rect.colliderect(item.rect):
                self.item_group.remove(item)

        


        
        
        

    def run(self):
        while self.running:
            self.clock.tick(fps) #define o fps do jogo
            self.eventos() #avalia acoes do jogador (cima, baixo, saiu do jogo, etc...)
            self.update() #movimentacao
            self.paint() #coloca cores na tela
    
    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False #sai do jogo
    
    
    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        self.all_sprites.update()
        for item in self.item_group.copy():
            if self.player.rect.colliderect(item.rect):
                self.item_group.remove(item)

    def paint(self):
        self.tela.fill(cores["preto"])
        self.item_group.draw(self.tela)
        self.tela.blit(self.player.image, self.player.rect)
        pygame.display.flip() #pinta a tela
