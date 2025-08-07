import pygame
from settings import *
from player import *
from items import *

class Game:
    def __init__(self, tela):
        self.tela = tela
        self.clock = pygame.time.Clock() 
        self.running = True

        self.player = Player(x=100, y=100, sheet_player=join('assets', 'img', 'player.png'))
        self.life_orb = Items(x=300, y=300, sheet_item=join('assets', 'img', 'lifeOrb.png'))
        self.expShard = Items(x=700, y=500, sheet_item=join('assets', 'img', 'expShard.png'))
        self.bigShard = Items(x=200, y=400, sheet_item=join('assets', 'img', 'bigShard.png'))
        
        #import
        pinpong_surface = pygame.image.load(join('assets', 'img', 'bola_pingpong.png'))

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
            delta_time = self.clock.tick(fps) / 1000 #define o fps do jogo e retorna o delta time em milisegundo, por isso divide por 1k
            self.eventos() #avalia acoes do jogador (cima, baixo, saiu do jogo, etc...)
            self.update(delta_time) #movimentacao
            self.paint() #coloca cores na tela
    
    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False #sai do jogo
    
    
    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.player.update(keys, delta_time)
        self.all_sprites.update(delta_time)
        for item in self.item_group.copy():
            if self.player.rect.colliderect(item.rect):
                self.item_group.remove(item)

    def paint(self):
        self.tela.fill(cores["preto"])
        self.item_group.draw(self.tela)
        self.tela.blit(self.player.image, self.player.rect)
        pygame.display.flip() #pinta a tela
