import pygame
import math
from items import *
from random import randint
from player import Player



class InimigoBase(pygame.sprite.Sprite):
    # 'posicao_x' e 'posicao_y' sao as coordenadas de onde ele vai aparecer.
    # 'jogador' é o objeto do jogador, para que o inimigo saiba quem ele deve seguir.
    def __init__(self, posicao, grupos, jogador):
        super().__init__(grupos)

        # --- Atributos Padrão ---
        self.velocidade = 100  # Velocidade do inimigo 
        self.jogador = jogador
        self.vida = 1
        self.dano = 10
        # --- Parte Visual do Inimigo PADRÃO ---
        self.image = pygame.Surface((40, 40))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=posicao)

        # --- Parte de Posição e Colisão ---
        self.posicao = pygame.math.Vector2(self.rect.center)

    def morrer(self, grupos):
        #drop
        dado = randint(0, 1000)
        if dado == 1000:
            Items(posicao=self.posicao, sheet_item=join('assets', 'img', 'racket.png'), tipo='racket', grupos=grupos)
        elif dado >= 990:
            Items(posicao=self.posicao, sheet_item=join('assets', 'img', 'bigShard.png'), tipo='big_shard', grupos=grupos)
        #life orb
        elif dado >= 970:
            Items(posicao=self.posicao, sheet_item=join('assets', 'img', 'lifeOrb.png'), tipo='life_orb',  grupos=grupos)
                #exp shard
        else:
            Items(posicao=self.posicao, sheet_item=join('assets', 'img', 'expShard.png'), tipo='exp_shard', grupos=grupos)
        
        self.kill()
            
    def update(self, delta_time):
         # A lógica de seguir o jogador
        direcao = self.jogador.rect.center - self.posicao
        if direcao.length() > 0:
            direcao.normalize_ip()
        self.posicao += direcao * self.velocidade * delta_time
        self.rect.center = self.posicao

class InimigoCirculo(InimigoBase):
    def __init__(self, posicao, grupos, jogador):
        super().__init__(posicao, grupos, jogador)
        
        # --- Parte Visual do Inimigo CIRCULO ---
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA) 
        pygame.draw.circle(self.image, 'cyan', (15, 15), 15)

        self.rect = self.image.get_rect(center=self.posicao)
        
        # Comportamento
        self.velocidade = 110
        self.vida = 1
        self.dano = 10

class InimigoListaIP(InimigoBase):
    def __init__(self, posicao, grupos, jogador):
        super().__init__(posicao, grupos, jogador)

        # Carrega a imagem do inimigo
        self.image = pygame.image.load(join('assets', 'img', 'inimigo_listaIP.png')).convert_alpha()
        self.rect = self.image.get_rect(center=self.posicao)

        # Ajuste os atributos se quiser, exemplo:
        self.velocidade = 90
        self.vida = 2
        self.dano = 15
