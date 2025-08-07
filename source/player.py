import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet_player):
        """
        Inicia o jogador.
        x: Posição x inicial.
        y: Posição y inicial.
        sheet_player: Imagem.
        """
        super().__init__()
        self.direcao = pygame.math.Vector2()
        self.velocidade = 500
        self.frame = pygame.image.load(sheet_player).convert_alpha()
        self.image = self.frame
        self.rect = self.image.get_frect(center = (altura_tela/2, largura_tela/2))

    def update(self, keys, delta_time):#movimentacao do player
        #delta_time serve pra o jogador sempre se mover na mesma velocidade independente do fps

        #muda os vetores se eles estão sendo pressionados ou não
        #direita = 1, esquerda = -1, cima = 1, baixo = -1
        #se a tecla está sendo pressionada, ela é True, true quando convertido pra int é 1
        self.direcao.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direcao.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        #caso a direção não for parado(dá erro), normaliza o vetor para que ao se mover na diagonal, não se mova mais rápido
        if self.direcao != (0,0):
            self.direcao = self.direcao.normalize()

        self.rect.center +=  self.direcao * self.velocidade * delta_time #atualiza a posição atual

   

