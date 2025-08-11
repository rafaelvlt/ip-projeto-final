import pygame
from settings import *
from player import *
from game import *

class Arma(ABC):
    def __init__(self, jogador):
        self.jogador = jogador
        #status
        self.nivel = 0
        self.dano = 0
        self.velocidade = 0
        self.cooldown = 0
        self.ultimo_tiro = 0
        #texto
        self.nome = ""
        self.descricao = ""

    
    @abstractmethod
    def disparar(self):
        pass

    def update(self, jogador=None):
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_tiro > self.cooldown:
                self.disparar()
                self.ultimo_tiro = agora
    
    def upgrade(self):
        self.nivel += 1 
    
    @abstractmethod
    def ver_proximo_upgrade(self):
        pass

    @abstractmethod
    def get_estatisticas_para_exibir(self):
        pass

class Arma_Loop(Arma):
    def __init__(self, jogador, grupos):
        #grupos index: 0 = all_sprites, 1= grupo_projeteis 2= grupo_inimigos
        #variáveis padrões
        super().__init__(jogador=jogador)
        #imagem
        self.surface_pinpong = pygame.image.load(join('assets', 'img', 'bola_pingpong.png'))
        novo_tamanho = (80, 80)
        self.surface_pinpong = pygame.transform.scale(self.surface_pinpong, novo_tamanho)

        #conexão com jogador e grupos
        self.all_sprites = grupos[0]
        self.grupo_projeteis = grupos[1]
        self.grupo_inimigos = grupos[2]

        #específicos da arma
        self.nivel = 1
        self.dano = 1
        self.velocidade = 1500
        self.cooldown = 1500
        self.rebatidas = 2
        self.nome = "Bolinha Calderânica"
        self.descricao = """Os projeteis são capazes
de rebater nas paredes!"""
        

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
                jogador=self.jogador,
                velocidade=self.velocidade,
                direcao=direcao_tiro,
                dano=self.dano,
                grupos=(self.all_sprites,self.grupo_projeteis),
                rebatidas=self.rebatidas
        )

            

    def upgrade(self):
        super().upgrade()
        #a cada 3 niveis fica mais rapido

        self.rebatidas += 1
        self.dano += 1
        if self.nivel % 3 == 0 and self.cooldown > 250:
            self.cooldown -= 250

    def ver_proximo_upgrade(self):
        prox_nivel = self.nivel + 1
        prox_dano = self.dano + 1
        prox_rebatidas = self.rebatidas + 1
        if prox_nivel % 3 == 0 and self.cooldown > 250:
            prox_cooldown = (self.cooldown - 250)
        else:
            prox_cooldown = self.cooldown

        return {
            'nivel': prox_nivel,
            'dano': prox_dano,
            'rebatidas': prox_rebatidas,
            'cooldown': prox_cooldown
        }
    def get_estatisticas_para_exibir(self):
        stats_futuros = self.ver_proximo_upgrade()
        cadencia_atual = 1000 / self.cooldown
        cadencia_futura = 1000 / stats_futuros['cooldown']

        stats_formatados = [
            f"Dano: {self.dano} -> {stats_futuros['dano']}",
            f"Rebotes: {self.rebatidas} -> {stats_futuros['rebatidas']}",
            f"Cadência: {cadencia_atual:.2f}/s -> {cadencia_futura:.2f}/s"
        ]

        return stats_formatados
class Projetil(pygame.sprite.Sprite):
    def __init__(self, surface, jogador, velocidade, direcao, dano, grupo_sprites):
        #classe projétil multipropósito, capaz de receber velocidade e imagem diferente dependendo do tipo de arma
        super().__init__(grupo_sprites) 
        #imagem e rect
        self.image = surface
        self.rect = self.image.get_rect(center=jogador.posicao)
        
        #posicao e movimento
        self.posicao = pygame.math.Vector2(jogador.posicao)
        self.direcao = pygame.math.Vector2(direcao)
        self.velocidade = velocidade

        #logica de armas
        self.dano = dano
        self.inimigos_atingidos = set()
    def update(self, delta_time):
        #faz se mover na direção do vetor dado na velocidade correta
        self.posicao +=  self.direcao * self.velocidade * delta_time #atualiza a posição atual se movendo para a direção
        #move o rect do projétil
        self.rect.centerx = round(self.posicao.x)
        self.rect.centery = round(self.posicao.y)


class Projetil_PingPong(Projetil):
    def __init__(self, surface, jogador, velocidade, direcao, dano, grupos, rebatidas):
        super().__init__(surface, jogador, velocidade, direcao, dano, grupos)
        self.rebatidas = rebatidas
        self.jogador = jogador
        self.posicao_inicial = jogador.posicao

    def update(self, delta_time):
        super().update(delta_time)

        #lógica para quicar nas extremidades da tela
        rebateu = False

        camera_borda_esquerda = self.jogador.posicao.x - (largura_tela / 2)
        camera_borda_direita = self.jogador.posicao.x + (largura_tela / 2)
        camera_borda_topo = self.jogador.posicao.y - (altura_tela / 2)
        camera_borda_baixo = self.jogador.posicao.y + (altura_tela / 2)

        #checa paredes horizontais
        if self.posicao.x <= camera_borda_esquerda:
            self.posicao.x = camera_borda_esquerda
            self.direcao.x *= -1
            rebateu = True
        elif self.posicao.x >= camera_borda_direita:
            self.posicao.x = camera_borda_direita
            self.direcao.x *= -1
            rebateu = True

        #checa paredes verticais
        if self.posicao.y <= camera_borda_topo:
            self.posicao.y = camera_borda_topo #
            self.direcao.y *= -1
            rebateu = True
        elif self.posicao.y >= camera_borda_baixo:
            self.posicao.y = camera_borda_baixo 
            self.direcao.y *= -1
            rebateu = True
        
        #so conta uma rebatidade nas bordas
        if rebateu:
            self.rebatidas -= 1

        if self.rebatidas <= 0:
            self.kill()