import pygame
from abc import ABC, abstractmethod

class Arma(ABC):
    def __init__(self, jogador, nome, cooldown_base, ultimo_tiro,  grupo_projeteis):
        self._jogador = jogador
        self._nome = nome
        self._nivel = 1
        self._cooldown_base = cooldown_base
        self._ultimo_tiro = ultimo_tiro

    @property
    def get_nivel(self):
        return self._nivel

    @property
    #getter de cooldown da arma
    def get_cooldown(self):
        return self._cooldown_base
    
    @abstractmethod
    def disparar(self):
        pass

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self._ultimo_tiro > self.get_cooldown:
            self.disparar()
            self.ultimo_disparo = agora
    
    def upgrade(self):
        self._nivel += 1

    