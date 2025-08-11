import pygame #aa
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, sheet_player, grupos):
        """
        Inicia o jogador.
        sheet_player: Imagem.
        grupos: grupos de sprite
        """
        super().__init__(grupos)
        #envolve movimentação
        self.direcao = pygame.math.Vector2()
        self.velocidade = 500
        self.frame = pygame.image.load(sheet_player).convert_alpha()

        #imagem e posicao
        self.image = self.frame
        self.rect = self.image.get_rect(center = (altura_tela/2, largura_tela/2))
        self.posicao = pygame.math.Vector2(self.rect.center)

        #armas do player
        self.armas = {}

        #status
        self.vida_maxima = 100
        self.vida_atual = self.vida_maxima
        
        #exp
        self.experiencia_level_up_base = 100 
        self.experiencia_level_up = self.experiencia_level_up_base
        self.experiencia_atual = 0

        self.coletaveis = {
            "exp_shard": 0,
            "life_orb": 0,
            "big_shard":0
        }

        #invencibilidade
        self.invencivel = False
        self.tempo_ultimo_dano = 0
        self.duracao_invencibilidade = 200
    def input(self):
        #muda os vetores se eles estão sendo pressionados ou não
        #direita = 1, esquerda = -1, cima = 1, baixo = -1
        #se a tecla está sendo pressionada, ela é True, true quando convertido pra int é 1
        keys = pygame.key.get_pressed()
        self.direcao.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direcao.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        #caso a direção não for parado(dá erro), normaliza o vetor para que ao se mover na diagonal, não se mova mais rápido
        if self.direcao != (0,0):
            self.direcao = self.direcao.normalize()

    def movimentacao(self, delta_time):
        #delta_time serve pra o jogador sempre se mover na mesma velocidade independente do fps
        self.posicao +=  self.direcao * self.velocidade * delta_time #atualiza a posição atual
        self.rect.centerx = self.posicao.x
        self.rect.centery = self.posicao.y

    def tomar_dano(self, inimigo):
        if not self.invencivel:
            self.vida_atual -= inimigo.dano
            self.invencivel = True
            self.tempo_ultimo_dano = pygame.time.get_ticks()

    def level_up(self):
        self.experiencia_atual = self.experiencia_atual - self.experiencia_level_up
        self.experiencia_level_up *= 2 
        self.vida_maxima += 25
        self.vida_atual += 25

    def update(self, delta_time):
        self.input()
        self.movimentacao(delta_time)
        if self.invencivel:
            agora = pygame.time.get_ticks()
            if agora - self.tempo_ultimo_dano > self.duracao_invencibilidade:
                self.invencivel = False
            
            #pisca player
            alpha = 255 if int(pygame.time.get_ticks() / 50) % 2 == 0 else 0
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
            
        if self.experiencia_atual >= self.experiencia_level_up:
            self.level_up()



   


