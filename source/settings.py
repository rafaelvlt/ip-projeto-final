from settings import *  # importa largura_tela e altura_tela
import os
import pygame

class TelaGameOver:
    def __init__(self, game):
        self.bg = pygame.image.load(os.path.join('assets', 'img', 'game_over.png')).convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (largura_tela, altura_tela))

    def draw(self, tela):
        tela.blit(self.bg, (0, 0))
