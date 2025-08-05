import pygame
from settings import fps, cores
from player import Player
from items import Items

class Game:
    def __init__(self, tela):
        self.tela = tela
        self.clock = pygame.time.Clock() 
        self.running = True

        self.player = Player(x=100, y=100, sheet_player=r'assets\img\player.png')
        self.life_orb = Items(x=300, y=300, sheet_item=r'assets\img\lifeOrb.png')

        self.all_sprites = pygame.sprite.Group() #grupo de sprites
        self.all_sprites.add(self.life_orb)
        self.all_sprites.add(self.player)

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

    def paint(self):
        self.tela.fill(cores["preto"])
        self.all_sprites.draw(self.tela)
        pygame.display.flip() #pinta a tela
