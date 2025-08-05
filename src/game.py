import pygame
from settings import fps, cores
from player import Player

class Game:
    def __init__(self, tela):
        self.tela = tela
        self.clock = pygame.time.Clock() 
        self.running = True
        self.player = Player(x=100, y=100, sheet_player=r'projeto ip1/assets/img/sheets/personagem principal/mc (2).png')
        
        self.all_sprites = pygame.sprite.Group() #grupo de sprites
        self.all_sprites.add(self.player)

    def run(self):
        while self.running:
            self.clock.tick(fps) #define o fps do jogo
            self.eventos() #avalia acoes do jogador (cima, baixo, saiu do jogo, etc...)
            self.update() #incompleto
            self.paint() #coloca cores na tela
    
    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False #sai do jogo
    
    def update(self):
        pass

    def paint(self):
        self.tela.fill(cores["preto"])
        self.all_sprites.draw(self.tela)
        pygame.display.flip() #pinta a tela
