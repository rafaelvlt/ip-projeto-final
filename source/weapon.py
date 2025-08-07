import pygame
from abc import ABC, abstractmethod

class Arma(ABC):
    def __init__(self, jogador, nome, cooldown_base, ultimo_tiro,  grupo_projeteis):
        self.jogador = jogador
        self.nome = nome
        self.nivel = 0
        self.cooldown_base = cooldown_base
        self.ultimo_tiro = ultimo_tiro

    
    @abstractmethod
    def disparar(self):
        pass

    def update(self):
        if self.nivel > 0:
            agora = pygame.time.get_ticks()
            if agora - self._ultimo_tiro > self.get_cooldown:
                self.disparar()
                self.ultimo_disparo = agora
    
    def upgrade(self):
        self.nivel += 1

    