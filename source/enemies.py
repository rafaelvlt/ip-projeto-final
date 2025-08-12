import pygame
import math
from items import *
from random import randint
from player import Player
from settings import *


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

class InimigoBug(InimigoBase):
    def __init__(self, posicao, grupos, jogador):
        super().__init__(posicao, grupos, jogador)
        
        # --- Parte Visual do Inimigo bug ---
        spritesheet = pygame.image.load(join('assets', 'img', 'bug.png'))
        self.animacoes = self.fatiar_spritesheet(spritesheet)
        self.estado_animacao = 'down'
        self.frame_atual = 0
        self.velocidade_animacao = 150
        self.ultimo_update_animacao = pygame.time.get_ticks()
        
        self.image = self.animacoes[self.estado_animacao][self.frame_atual]
        self.rect = self.image.get_rect(center = posicao)
        
        # Comportamento
        self.velocidade = 110
        self.vida = 1
        self.dano = 10
    def fatiar_spritesheet(self, sheet):

        largura_frame = 32 # 128px / 4 frames
        altura_frame = 32  # 128px / 4 frames
        
        animacoes = {
            'up': [],
            'left': [],
            'right': [],
            'down': [],
        }

        for linha, nome_animacao in enumerate(['down', 'left', 'right', 'up']):
            for coluna in range(4): # 4 frames por animação
                x = coluna * largura_frame
                y = linha * altura_frame
                #usa .subsurface() para recortar o frame
                frame = sheet.subsurface(pygame.Rect(x, y, largura_frame, altura_frame))
                novo_tamanho = (100, 100)
                frame_escalado =  pygame.transform.scale(frame, novo_tamanho)

                animacoes[nome_animacao].append(frame_escalado)
        return animacoes
    def animar(self):
        agora = pygame.time.get_ticks()
        
        if agora - self.ultimo_update_animacao > self.velocidade_animacao:
            self.ultimo_update_animacao = agora # Reseta o timer
            
            #avança para o próximo frame da animação atual
            self.frame_atual = (self.frame_atual + 1) % len(self.animacoes[self.estado_animacao])
            
            #atualiza a imagem do sprite para o novo frame
            self.image = self.animacoes[self.estado_animacao][self.frame_atual]
            self.rect = self.image.get_rect(center = self.rect.center)

    def update(self, delta_time):
        direcao = (self.jogador.posicao - self.posicao).normalize() if (self.jogador.posicao - self.posicao).length() > 0 else pygame.math.Vector2()
        self.posicao += direcao * self.velocidade * delta_time
        self.rect.center = (round(self.posicao.x), round(self.posicao.y))
        

        if abs(direcao.y) > abs(direcao.x):
            if direcao.y < 0:
                self.estado_animacao = 'up'
            else:
                self.estado_animacao = 'down'
        elif abs(direcao.x) > 0:
            if direcao.x < 0:
                self.estado_animacao = 'left'
            else:
                self.estado_animacao = 'right'

        self.animar()
class InimigoListaIP(InimigoBase):
    def __init__(self, posicao, grupos, jogador):
        super().__init__(posicao, grupos, jogador)

        # Carrega a imagem do inimigo
        self.image = pygame.image.load(join('assets', 'img', 'inimigo_listaIP.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=self.posicao)

        
        self.velocidade = 90
        self.vida = 2
        self.dano = 15
