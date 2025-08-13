import pygame
from os.path import join
from random import randint
from items import *
from player import Player
from settings import *


class InimigoBase(pygame.sprite.Sprite):
    def __init__(self, posicao, grupos, jogador, vida_base, dano_base, velocidade_base):
        super().__init__(grupos)
        self.jogador = jogador
        self.vida_base = vida_base
        self.dano_base = dano_base
        self.velocidade_base = velocidade_base
        self.image = pygame.Surface((40, 40))
        self.image.fill('white')
        self.rect = self.image.get_rect(center=posicao)
        self.posicao = pygame.math.Vector2(self.rect.center)
        #settando os status
        self.vida = self.vida_base
        self.dano = self.dano_base
        self.velocidade = self.velocidade_base
        #dificulta baseado no nivel do player
        self.aplicar_dificuldade()

        
    def aplicar_dificuldade(self):
        if 10 >= self.jogador.contador_niveis > 5:
            self.vida *= self.jogador.contador_niveis / 5
            self.dano *= self.jogador.contador_niveis / 5
        elif 15 >= self.jogador.contador_niveis > 10:
            self.vida *= self.jogador.contador_niveis / 2
            self.dano *= self.jogador.contador_niveis / 2
            self.velocidade *= self.jogador.contador_niveis / 10
        elif self.jogador.contador_niveis > 15:
            self.constante_lategame = self.jogador.contador_niveis - 15
            self.vida *= self.constante_lategame * (self.jogador.contador_niveis)
            self.dano *= self.constante_lategame * (self.jogador.contador_niveis)
            self.velocidade *= self.jogador.contador_niveis / 10

    def morrer(self, grupos):
        dado = randint(0, 1000)
        if dado == 1000:
            Items(posicao=self.posicao, sheet_item=join('assets', 'img', 'cafe.png'), tipo='cafe', grupos=grupos)
        elif dado >= 990:
            Items(posicao=self.posicao, sheet_item=join('assets', 'img', 'bigShard.png'), tipo='big_shard', grupos=grupos)
        elif dado >= 970:
            Items(posicao=self.posicao, sheet_item=join('assets', 'img', 'lifeOrb.png'), tipo='life_orb', grupos=grupos)
        else:
            Items(posicao=self.posicao, sheet_item=join('assets', 'img', 'expShard.png'), tipo='exp_shard', grupos=grupos)
        self.kill()

    def update(self, delta_time):
        direcao = self.jogador.rect.center - self.posicao
        if direcao.length() > 0:
            direcao.normalize_ip()
        self.posicao += direcao * self.velocidade * delta_time
        self.rect.center = self.posicao


class InimigoBug(InimigoBase):
    def __init__(self, posicao, grupos, jogador):
        super().__init__(posicao, grupos, jogador, vida_base=1, dano_base=10, velocidade_base=110)
        spritesheet = pygame.image.load(join('assets', 'img', 'bug.png'))
        self.animacoes = self.fatiar_spritesheet(spritesheet)
        self.estado_animacao = 'down'
        self.frame_atual = 0
        self.velocidade_animacao = 150
        self.ultimo_update_animacao = pygame.time.get_ticks()
        self.image = self.animacoes[self.estado_animacao][self.frame_atual]
        self.rect = self.image.get_rect(center=posicao)
        
    def fatiar_spritesheet(self, sheet):
        largura_frame = 32
        altura_frame = 32
        animacoes = {'up': [], 'left': [], 'right': [], 'down': []}
        for linha, nome_animacao in enumerate(['down', 'left', 'right', 'up']):
            for coluna in range(4):
                x = coluna * largura_frame
                y = linha * altura_frame
                frame = sheet.subsurface(pygame.Rect(x, y, largura_frame, altura_frame))
                frame_escalado = pygame.transform.scale(frame, (100, 100))
                animacoes[nome_animacao].append(frame_escalado)
        return animacoes

    def animar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update_animacao > self.velocidade_animacao:
            self.ultimo_update_animacao = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.animacoes[self.estado_animacao])
            self.image = self.animacoes[self.estado_animacao][self.frame_atual]
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, delta_time):
        direcao = (self.jogador.posicao - self.posicao).normalize() if (self.jogador.posicao - self.posicao).length() > 0 else pygame.math.Vector2()
        self.posicao += direcao * self.velocidade * delta_time
        self.rect.center = (round(self.posicao.x), round(self.posicao.y))
        if abs(direcao.y) > abs(direcao.x):
            self.estado_animacao = 'up' if direcao.y < 0 else 'down'
        elif abs(direcao.x) > 0:
            self.estado_animacao = 'left' if direcao.x < 0 else 'right'
        self.animar()


class InimigoListaIP(InimigoBase):
    def __init__(self, posicao, grupos, jogador):
        super().__init__(posicao, grupos, jogador, vida_base=2, dano_base=15, velocidade_base=90)
        self.image = pygame.image.load(join('assets', 'img', 'inimigo_listaIP.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 80))
        self.rect = self.image.get_rect(center=self.posicao)
        self.velocidade = 90
        self.vida = 2
        self.dano = 15


class InimigoErro(InimigoBase):
    def __init__(self, posicao, grupos, jogador):
        super().__init__(posicao, grupos, jogador, vida_base=1, dano_base=10, velocidade_base=110)
        imagem_original = pygame.image.load(join('assets', 'img', 'erro.png')).convert_alpha()
        self.image = pygame.transform.scale(imagem_original, (100, 100))
        self.rect = self.image.get_rect(center=self.posicao)

class BossInimigo(InimigoBase):
    def __init__(self, posicao, grupos, jogador):
        super().__init__(posicao, grupos, jogador, vida_base=100, dano_base=20, velocidade_base=35)
        self.image = pygame.image.load(join('assets', 'img', 'bossInimigo.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(center=posicao)
        self.posicao = pygame.math.Vector2(self.rect.center)
        self.grupos_gerais = grupos
        self.tempo_invocacao = 0
        self.cooldown_invocacao = 5000

    def invocar_ajudantes(self):
        InimigoErro(posicao=self.posicao, grupos=self.grupos_gerais, jogador=self.jogador)

    def morrer(self, grupos):
        Items(posicao=self.posicao, sheet_item=join('assets', 'img', 'cafe.png'), tipo='cafe', grupos=grupos)
        for _ in range(5):
            posicao_drop = self.posicao + pygame.math.Vector2(randint(-30, 30), randint(-30, 30))
            Items(posicao=posicao_drop, sheet_item=join('assets', 'img', 'bigShard.png'), tipo='big_shard', grupos=grupos)
        self.kill()

    def update(self, delta_time):
        super().update(delta_time)
        self.tempo_invocacao += delta_time * 1000
        if self.tempo_invocacao >= self.cooldown_invocacao:
            self.tempo_invocacao = 0
            self.invocar_ajudantes()
            
class InimigoPython(InimigoBase):
    def __init__(self, posicao, grupos, jogador):
        super().__init__(posicao, grupos, jogador, vida_base=1,dano_base=10, velocidade_base=75)
        spritesheet = pygame.image.load(join('assets', 'img', 'python.png'))
        self.image = pygame.transform.scale(spritesheet, (600, 600))
        self.animacoes = self.fatiar_spritesheet(self.image)
        self.estado_animacao = 'down'
        self.frame_atual = 0
        self.velocidade_animacao = 150
        self.ultimo_update_animacao = pygame.time.get_ticks()
        self.image = self.animacoes[self.estado_animacao][self.frame_atual]
        self.rect = self.image.get_rect(center=posicao)

    def fatiar_spritesheet(self, sheet):
        largura_frame = 150
        altura_frame = 150
        animacoes = {'up': [], 'left': [], 'right': [], 'down': []}
        for linha, nome_animacao in enumerate(['down', 'left', 'right', 'up']):
            for coluna in range(4):
                x = coluna * largura_frame
                y = linha * altura_frame
                frame = sheet.subsurface(pygame.Rect(x, y, largura_frame, altura_frame))
                frame_escalado = pygame.transform.scale(frame, (100, 100))
                animacoes[nome_animacao].append(frame_escalado)
        return animacoes

    def animar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update_animacao > self.velocidade_animacao:
            self.ultimo_update_animacao = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.animacoes[self.estado_animacao])
            self.image = self.animacoes[self.estado_animacao][self.frame_atual]
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, delta_time):
        direcao = (self.jogador.posicao - self.posicao).normalize() if (self.jogador.posicao - self.posicao).length() > 0 else pygame.math.Vector2()
        self.posicao += direcao * self.velocidade * delta_time
        self.rect.center = (round(self.posicao.x), round(self.posicao.y))
        if abs(direcao.y) > abs(direcao.x):
            self.estado_animacao = 'up' if direcao.y < 0 else 'down'
        elif abs(direcao.x) > 0:
            self.estado_animacao = 'left' if direcao.x < 0 else 'right'
        self.animar()

class InimigoLadrao(InimigoBase):
    def __init__(self, posicao, grupos, jogador):
        super().__init__(posicao, grupos, jogador)
        spritesheet = pygame.image.load(join('assets', 'img', 'ladrao.png'))
        self.image = pygame.transform.scale(spritesheet, (600, 600))
        self.animacoes = self.fatiar_spritesheet(self.image)
        self.estado_animacao = 'down'
        self.frame_atual = 0
        self.velocidade_animacao = 150
        self.ultimo_update_animacao = pygame.time.get_ticks()
        self.image = self.animacoes[self.estado_animacao][self.frame_atual]
        self.rect = self.image.get_rect(center=posicao)
        self.velocidade = 300
        self.vida = 50
        self.dano = 50

    def fatiar_spritesheet(self, sheet):
        largura_frame = 150
        altura_frame = 150
        animacoes = {'up': [], 'left': [], 'right': [], 'down': []}
        for linha, nome_animacao in enumerate(['down', 'left', 'right', 'up']):
            for coluna in range(4):
                x = coluna * largura_frame
                y = linha * altura_frame
                frame = sheet.subsurface(pygame.Rect(x, y, largura_frame, altura_frame))
                frame_escalado = pygame.transform.scale(frame, (100, 100))
                animacoes[nome_animacao].append(frame_escalado)
        return animacoes

    def animar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update_animacao > self.velocidade_animacao:
            self.ultimo_update_animacao = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.animacoes[self.estado_animacao])
            self.image = self.animacoes[self.estado_animacao][self.frame_atual]
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, delta_time):
        direcao = (self.jogador.posicao - self.posicao).normalize() if (self.jogador.posicao - self.posicao).length() > 0 else pygame.math.Vector2()
        self.posicao += direcao * self.velocidade * delta_time
        self.rect.center = (round(self.posicao.x), round(self.posicao.y))
        if abs(direcao.y) > abs(direcao.x):
            self.estado_animacao = 'up' if direcao.y < 0 else 'down'
        elif abs(direcao.x) > 0:
            self.estado_animacao = 'left' if direcao.x < 0 else 'right'
        self.animar()