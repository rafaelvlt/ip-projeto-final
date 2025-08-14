import pygame
import math
from settings import *
from player import *

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
    
    def equipar(self):
        """
        apenas para aura e companheiros
        """
        pass 
    
    @abstractmethod
    def ver_proximo_upgrade(self):
        pass

    @abstractmethod
    def get_estatisticas_para_exibir(self):
        pass

class Arma_Loop(Arma):
    def __init__(self, jogador, grupos, game):
        #grupos index: 0 = all_sprites, 1= grupo_projeteis 2= grupo_inimigos
        #variáveis padrões
        super().__init__(jogador=jogador)
        self.game = game
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
        self.descricao = """Capaz de rebater nas paredes!"""
        

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
    
class ArmaLista(Arma):
    def __init__(self, jogador, grupos, game):
        super().__init__(jogador=jogador)
        self.game = game

        #imagem
        self.surface_listas = pygame.image.load(join('assets', 'img', 'listas.png')).convert_alpha()
        self.surface_listas = pygame.transform.scale(self.surface_listas, (45, 80))
        #grupos
        self.all_sprites = grupos[0]
        self.projeteis_grupo = grupos[1]

        #específicos da arma
        self.nome = "Domínio das Lâminas"
        self.descricao = "Protegem o jogador!"
        self.nivel = 1
        self.num_listas = 1
        self.dano = 15
        self.velocidade = 0
        self.cooldown = 5000
        self.duracao = 4000
        self.distancia_orbita = 140
        self.velocidade_rotacao = 90
        

    def disparar(self):
        #para o angulo ficar igualmente espaçado 
        angulo_step = 360 / self.num_listas
        for i in range(self.num_listas):
            angulo = i * angulo_step
            Projetil_Lista(
                surface=self.surface_listas, 
                jogador=self.jogador,
                velocidade=0,
                direcao=(0,0),
                dano=self.dano,
                grupos=(self.all_sprites, self.projeteis_grupo),
                angulo_inicial=angulo,
                distancia_orbita=self.distancia_orbita,
                velocidade_rotacao=self.velocidade_rotacao,
                duracao=self.duracao
            )
    def upgrade(self):
        super().upgrade()
        #a cada 3 niveis fica mais rapido

        self.velocidade_rotacao += 5
        self.dano += 5
        if self.nivel % 3 == 0:
            self.num_listas += 1

    def ver_proximo_upgrade(self):
        prox_nivel = self.nivel + 1
        prox_dano = self.dano + 5
        prox_velocidade_rotacao = self.velocidade_rotacao + 5
        if prox_nivel % 3 == 0:
            prox_listas = self.num_listas + 1
        else:
            prox_listas = self.num_listas

        return {
            'nivel': prox_nivel,
            'dano': prox_dano,
            'velocidade_rotacao': prox_velocidade_rotacao,
            'num_listas': prox_listas
        }
    def get_estatisticas_para_exibir(self):
        stats_futuros = self.ver_proximo_upgrade()

        stats_formatados = [
            f"Dano: {self.dano} -> {stats_futuros['dano']}",
            f"Velocidade Angular: {self.velocidade_rotacao}°/s-> {stats_futuros['velocidade_rotacao']}°/s",
            f"Num. Listas: {stats_futuros['num_listas']} -> {stats_futuros['num_listas']}"
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

class Projetil_Lista(Projetil):
    def __init__(self, surface, jogador, velocidade, direcao, dano, grupos, angulo_inicial, distancia_orbita, velocidade_rotacao, duracao):
        super().__init__(surface, jogador, velocidade, direcao, dano, grupos)
        #atributos
        self.jogador = jogador
        self.angulo = angulo_inicial  #posição angular inicial no círculo
        self.distancia_orbita = distancia_orbita
        self.velocidade_rotacao = velocidade_rotacao #graus por segundo
        self.tempo_criacao = pygame.time.get_ticks()
        self.duracao = duracao

        #colisao
        self.inimigos_atingidos = set()
        
    def update(self, delta_time):
        #atualiza o angulo
        self.angulo += self.velocidade_rotacao * delta_time
        
        # calcula novo x e y com base em trigo
        deslocamento_x = math.cos(math.radians(self.angulo)) * self.distancia_orbita
        deslocamento_y = math.sin(math.radians(self.angulo)) * self.distancia_orbita
        
        #posição do projétil é a posição do jogador + o deslocamento da órbita
        self.posicao = self.jogador.posicao + pygame.math.Vector2(deslocamento_x, deslocamento_y)
        self.rect.center = (round(self.posicao.x), round(self.posicao.y))

        # verifica se acabou a duração
        if pygame.time.get_ticks() - self.tempo_criacao > self.duracao:
            self.kill()

class Dicionario_Divino(Arma):
    def __init__(self, jogador, grupos, game):
        super().__init__(jogador=jogador) 
        self.game = game 

        # Status Iniciais da Arma
        self.nome = "Dicionário Divino"
        self.descricao = "Causa dano por segundo"
        self.nivel = 1
        self.dano_por_segundo = 1
        self.raio = 120
        self.cooldown = float('inf') 
        self.all_sprites, self.auras_grupos = grupos

        self.area_de_dano = None
    def equipar(self):
        if self.area_de_dano is None:
            print("Equipando Dicionário Divino e criando sua aura!")
            self.area_de_dano = Projetil_Area(
                jogador=self.jogador,
                raio=self.raio,
                dano_por_segundo=self.dano_por_segundo,
                grupos=(self.all_sprites, self.auras_grupos)
            )

    def disparar(self):
      
        pass
    
    def update(self, delta_time):

        pass

    def upgrade(self):
        super().upgrade() # Aumenta self.nivel

        if self.area_de_dano:
            self.dano_por_segundo += 1
            self.raio += 15

            self.area_de_dano.atualizar_stats(self.raio, self.dano_por_segundo)

    def ver_proximo_upgrade(self):
        return {
            'nivel': self.nivel + 1,
            'dano_por_segundo': self.dano_por_segundo + 1,
            'raio': self.raio + 15
        }

    def get_estatisticas_para_exibir(self):
        prox = self.ver_proximo_upgrade()
        return [
            f"Dano/s: {self.dano_por_segundo:.2f} -> {prox['dano_por_segundo']:.2f}",
            f"Raio: {self.raio} -> {prox['raio']}"
        ] 

    
    
class Projetil_Area(pygame.sprite.Sprite):
    def __init__(self, jogador, raio, dano_por_segundo, grupos):
        super().__init__(grupos)
        self.jogador = jogador

        # Carrega a imagem dos parênteses uma única vez
        self.imagem_parenteses_original = pygame.image.load(join('assets', 'img', 'dicionario.png')).convert_alpha()
        

        #atributos e img
        self.raio = 0
        self.dano_por_segundo = 0
        self.image = pygame.Surface((1,1))
        self.rect = self.image.get_rect(center=self.jogador.posicao)
        
        self.inimigos_atingidos = set()

        self.atualizar_stats(raio, dano_por_segundo)

    def atualizar_stats(self, novo_raio, novo_dano):
        self.raio = novo_raio
        self.dano_por_segundo = novo_dano
        
        self.image = pygame.Surface((self.raio * 2, self.raio * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 0, 25), (self.raio, self.raio), self.raio)

        self.imagem_parenteses_red = pygame.transform.scale(self.imagem_parenteses_original, (self.raio * 2, self.raio * 2))
            

        self.image.blit(self.imagem_parenteses_red, (0,0))
        self.rect = self.image.get_rect(center=self.jogador.posicao)

    def update(self, delta_time):
        self.rect.center = self.jogador.posicao

class ArmaByte(Arma):
    def __init__(self, jogador, grupos, game):
        super().__init__(jogador=jogador)
        self.game = game 
        
        
        self.all_sprites, self.inimigos_grupo, self.item_grupo = grupos

        # atributos da arma
        self.nome = "Companheiro Byte"
        self.descricao = "Ataca inimigos e coleta itens"
        self.nivel = 1
        self.nivel_maximo = 8
        self.dano = 20
        self.cooldown = float('inf')

        self.sprite_cachorro = None
        #self.sprite_cachorro = CompanheiroCachorro(jogador, [self.all_sprites], self.inimigos_grupo, self.item_grupo)
        #self.sprite_cachorro.dano = self.dano 
    def equipar(self):
        if self.sprite_cachorro is None:
            self.sprite_cachorro = CompanheiroCachorro(
                jogador=self.jogador,
                grupos=self.all_sprites, # Adiciona ao all_sprites
                inimigos_grupo=self.inimigos_grupo,
                item_grupo=self.item_grupo
            )

    def disparar(self):
        
        pass

    def update(self, delta_time):
        
        pass

    def upgrade(self):
        super().upgrade()
        self.dano += 10
        self.sprite_cachorro.dano = self.dano 
        self.sprite_cachorro.velocidade_correr *= 1.2
        self.sprite_cachorro.raio_deteccao_inimigo += 20
        self.sprite_cachorro.raio_deteccao_item += 20
    
    def ver_proximo_upgrade(self):

        if self.sprite_cachorro:
            velocidade_atual = self.sprite_cachorro.velocidade_correr
            raio_ini_atual = self.sprite_cachorro.raio_deteccao_inimigo
            raio_item_atual = self.sprite_cachorro.raio_deteccao_item
        else:
            velocidade_atual = 450 
            raio_ini_atual = 300   
            raio_item_atual = 200  


        prox_nivel = self.nivel + 1
        prox_dano = self.dano + 10
        prox_velocidade = velocidade_atual * 1.2
        prox_raio_ini = raio_ini_atual + 20
        prox_raio_item = raio_item_atual + 20

        return {
            'nivel': prox_nivel,
            'dano': prox_dano,
            'velocidade': prox_velocidade,
            'raio_inimigo': prox_raio_ini,
            'raio_item': prox_raio_item
        }

    def get_estatisticas_para_exibir(self):
        prox = self.ver_proximo_upgrade()
        
        if self.sprite_cachorro:
            velocidade_atual = self.sprite_cachorro.velocidade_correr
            raio_ini_atual = self.sprite_cachorro.raio_deteccao_inimigo
            raio_item_atual = self.sprite_cachorro.raio_deteccao_item
        else:
            velocidade_atual = 450
            raio_ini_atual = 300
            raio_item_atual = 200

        return [
            f"Dano: {self.dano} -> {prox['dano']}",
            f"Velocidade: {int(velocidade_atual)} -> {int(prox['velocidade'])}",
            f"Raio Inimigo: {raio_ini_atual} -> {prox['raio_inimigo']}",
            f"Raio Item: {raio_item_atual} -> {prox['raio_item']}"
        ] 
class CompanheiroCachorro(pygame.sprite.Sprite):
    def __init__(self, jogador, grupos, inimigos_grupo, item_grupo):
        super().__init__(grupos)
        self.jogador = jogador
        self.inimigos_grupo = inimigos_grupo
        self.item_group = item_grupo
        
   
        self.estado_logico = 'SEGUINDO' # SEGUINDO, ATACANDO, COLETANDO
        self.alvo = None
        self.direcao_movimento = pygame.math.Vector2()

        # Atributos de Comportamento
        self.velocidade_andar = 220
        self.velocidade_correr = 450
        self.raio_deteccao_inimigo = 300
        self.raio_deteccao_item = 200
        self.distancia_seguidor = 100 
        self.dano = 0 
        self.cooldown = 500 
        self.ultimo_dano = {} 

        #inatividade
        self.tempo_jogador_parado = 0.0 
        self.limite_tempo_para_sentar = 2.0
        #animacao
        spritesheet = pygame.image.load(join('assets', 'img', 'byte.png')).convert_alpha()
        especificacoes_animacao = {
            'sentado': {'linha': 1, 'frames': 8},
            'correr':   {'linha': 3, 'frames': 8},
            'andar':  {'linha': 4, 'frames': 8}  
        }
        self.animacoes = self.fatiar_animacoes(spritesheet, 384, 288, especificacoes_animacao)

        self.estado_animacao = 'andar' # 'andar' ou 'correr'
        self.direcao_rosto = 'esquerda'
        self.frame_atual = 0
        self.velocidade_animacao = 150
        self.ultimo_update_anim = pygame.time.get_ticks()
        
        self.image = self.animacoes[self.estado_animacao][self.frame_atual]
        self.rect = self.image.get_rect(center = self.jogador.posicao + pygame.math.Vector2(0, self.distancia_seguidor))
        self.posicao = pygame.math.Vector2(self.rect.center)


    def fatiar_animacoes(self, sheet, largura_frame, altura_frame, especificacoes):
        animacoes = {}
        for nome_animacao, dados in especificacoes.items():
            frames = []
            for i in range(dados['frames']):
                frame = sheet.subsurface(pygame.Rect(i * largura_frame, dados['linha'] * altura_frame, largura_frame, altura_frame))
                # escala cada frame individualmente
                frame_escalado = pygame.transform.scale(frame, (384/2, 288/2))
                frames.append(frame_escalado)
            animacoes[nome_animacao] = frames
        return animacoes

    def logica_de_decisao(self):
    
        #1. ataca inimigo
        inimigo_alvo = self.encontrar_alvo_mais_proximo(self.inimigos_grupo, self.raio_deteccao_inimigo)
        if inimigo_alvo:
            self.estado_logico = 'ATACANDO'
            self.alvo = inimigo_alvo
            return

        #2. coleta item
        item_alvo = self.encontrar_alvo_mais_proximo(self.item_group, self.raio_deteccao_item)
        if item_alvo:
            self.estado_logico = 'COLETANDO'
            self.alvo = item_alvo
            return

        #3. segue o player
        self.estado_logico = 'SEGUINDO'
        self.alvo = self.jogador
    
    def encontrar_alvo_mais_proximo(self, grupo, raio):
        sprites_no_raio = [s for s in grupo if self.posicao.distance_to(s.posicao) < raio]
        if sprites_no_raio:
            return min(sprites_no_raio, key=lambda s: self.posicao.distance_to(s.posicao))
        return None
    
    def executar_comportamento(self, delta_time):
       
        velocidade = 0
        if self.estado_logico == 'SEGUINDO':
            self.estado_animacao = 'andar'
            velocidade = self.velocidade_andar
            distancia_do_alvo = self.posicao.distance_to(self.alvo.posicao)
            if distancia_do_alvo < self.distancia_seguidor: 
                self.direcao_movimento = pygame.math.Vector2() 
            else:
                self.direcao_movimento = (self.alvo.posicao - self.posicao).normalize()

        elif self.estado_logico in ['ATACANDO', 'COLETANDO']:
            self.estado_animacao = 'correr'
            velocidade = self.velocidade_correr
            if not self.alvo or not self.alvo.alive():
                self.direcao_movimento = pygame.math.Vector2()
                return

            self.direcao_movimento = (self.alvo.posicao - self.posicao).normalize()
            distancia_do_alvo = self.posicao.distance_to(self.alvo.posicao)

            if distancia_do_alvo < 40: 
                if self.estado_logico == 'ATACANDO':
                    agora = pygame.time.get_ticks()
                    if agora - self.ultimo_dano.get(self.alvo, 0) > self.cooldown:
                        self.ultimo_dano[self.alvo] = agora
                        self.alvo.vida -= self.dano
                elif self.estado_logico == 'COLETANDO':
                    self.jogador.coletar_item(self.alvo) 
                    self.alvo.kill()
        if self.direcao_movimento.x > 0.1:
            self.direcao_rosto = 'direita'
        elif self.direcao_movimento.x < -0.1:
            self.direcao_rosto = 'esquerda'
   
        self.posicao += self.direcao_movimento * velocidade * delta_time
        self.rect.center = (round(self.posicao.x), round(self.posicao.y))

    def animar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_update_anim > self.velocidade_animacao:
            self.ultimo_update_anim = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.animacoes[self.estado_animacao])
            
            imagem_original = self.animacoes[self.estado_animacao][self.frame_atual]
            
            if self.direcao_movimento.x > 0:
                self.image = pygame.transform.flip(imagem_original, True, False)
            else:
                self.image = imagem_original
            
            self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, delta_time):
        self.logica_de_decisao()
        self.executar_comportamento(delta_time)
        self.animar()