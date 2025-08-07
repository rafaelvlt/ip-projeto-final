import pygame
from settings import *
from player import *
from game import *

class Arma(ABC):
    def __init__(self, jogador, cooldown):
        self.jogador = jogador
        self.nivel = 1
        self.cooldown = cooldown
        self.ultimo_tiro = 0

    
    @abstractmethod
    def disparar(self):
        pass

    def update(self):
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_tiro > self.cooldown:
                self.disparar()
                self.ultimo_tiro = agora
    
    def upgrade(self):
        self.nivel += 1 

class Arma_Loop(Arma):
    def __init__(self, jogador, cooldown, grupo_projeteis, grupo_inimigos):
        #variáveis padrões
        super().__init__(jogador=jogador, cooldown=cooldown)
        self.velocidade = 1500
        self.surface_pinpong = pygame.image.load(join('assets', 'img', 'bola_pingpong.png'))

        #conexão com jogador e grupos
        self.grupo_projeteis = grupo_projeteis
        self.grupo_inimigos = grupo_inimigos
        #específicos da arma
        self.rebatidas = 2
        self.dano = 1

    def disparar(self):
        #detecta o inimigo mais próximo
        #se não houver inimigos, não atira
        if not self.grupo_inimigos:
            return
        
        inimigo_mais_proximo = self.grupo_inimigos.sprites()[0]
        menor_distancia = self.jogador.posicao.distance_to(inimigo_mais_proximo.posicao)

        for inimigo in self.grupo_inimigos:
            distancia_atual = self.jogador.posicao.distance_to(inimigo.posicao)
            if distancia_atual < menor_distancia:
                inimigo_mais_proximo = inimigo
                menor_distancia = distancia_atual
        
        #pega um vetor que aponta para o inimigo mais próximo, normalizado
        direcao_tiro = (inimigo_mais_proximo.posicao - self.jogador.posicao).normalize()

        Projetil_PingPong(
                surface=self.surface_pinpong, 
                posicao_inicial=self.jogador.posicao,
                velocidade=self.velocidade,
                direcao=direcao_tiro,
                dano=self.dano,
                grupos=self.grupo_projeteis,
                rebatidas=self.rebatidas
        )

            

    def upgrade(self):
        super().upgrade()
        #a cada 5 niveis ganha um projétil a mais
        self.rebatidas += 1
        self.dano += 1



class Projetil(pygame.sprite.Sprite):
    def __init__(self, surface, posicao_inicial, velocidade, direcao, dano, grupo_sprites):
        #classe projétil multipropósito, capaz de receber velocidade e imagem diferente dependendo do tipo de arma
        super().__init__(grupo_sprites) 
        self.image = surface
        self.rect = self.image.get_rect(center=posicao_inicial)
        self.posicao = pygame.math.Vector2(posicao_inicial)
        self.direcao = pygame.math.Vector2(direcao)
        self.velocidade = velocidade
        self.dano = dano

    def update(self, delta_time):
        #faz se mover na direção do vetor dado na velocidade correta
        self.posicao +=  self.direcao * self.velocidade * delta_time #atualiza a posição atual se movendo para a direção
        #move o rect do projétil
        self.rect.centerx = self.posicao.x
        self.rect.centery = self.posicao.y


class Projetil_PingPong(Projetil):
    def __init__(self, surface, posicao_inicial, velocidade, direcao, dano, grupos, rebatidas):
        super().__init__(surface, posicao_inicial, velocidade, direcao, dano, grupos)
        self.rebatidas = rebatidas
            
    def update(self, delta_time):
        super().update(delta_time)

        #lógica para quicar nas extremidades da tela
        rebateu = False

        #checa paredes horizontais
        if self.posicao.x <= 0:
            self.posicao.x = 0
            self.direcao.x *= -1
            rebateu = True
        elif self.posicao.x >= largura_tela:
            self.posicao.x = largura_tela
            self.direcao.x *= -1
            rebateu = True

        #checa paredes verticais
        if self.posicao.y <= 0:
            self.posicao.y = 0 #
            self.direcao.y *= -1
            rebateu = True
        elif self.posicao.y >= altura_tela:
            self.posicao.y = altura_tela 
            self.direcao.y *= -1
            rebateu = True
        
        #so conta uma rebatidade nas bordas
        if rebateu:
            self.rebatidas -= 1

        if self.rebatidas <= 0:
            self.kill()