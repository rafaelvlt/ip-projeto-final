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


class Projetil(pygame.sprite.Sprite):
    def __init__(self, pos, cor, grupo_sprites):
        super().__init__(grupo_sprites) 
        self.image = pygame.Surface((8, 15))
        self.image.fill(cor)
        self.rect = self.image.get_rect(center=pos)
        self.velocidade = 10
        self.pos = pygame.math.Vector2(self.rect.center)

    def update(self):
        self.pos.y -= self.velocidade
        self.rect.center = self.pos
        
        if self.rect.bottom < 0:
            self.kill()
            