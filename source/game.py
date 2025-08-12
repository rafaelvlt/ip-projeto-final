import pygame
import pytmx
import random
from settings import *
from player import *
from items import *
from weapon import *
from os.path import join
from menu import *
from hud import *
from enemies import InimigoBase, InimigoCirculo, InimigoListaIP
from grupos import AllSprites
from ranking import Ranking 
from levelup import *

class Game:
    def __init__(self, tela):
        self.tela = tela
        self.clock = pygame.time.Clock()
        self.running = True
        self.hud = HUD(self)
        

        # Carregue a imagem do mapa aqui:
        #self.tmx_data = pytmx.load_pygame('assets', 'img', 'mapa.tmx')
        #largura_mapa_pixels = self.tmx_data.width * self.tmx_data.tilewidth
        #altura_mapa_pixels = self.tmx_data.height * self.tmx_data.tileheight
        #self.mapa_surface = pygame.Surface((largura_mapa_pixels, altura_mapa_pixels))

        
        #máquina de estado
        self.estado_do_jogo = "menu_principal"
        self.menu_principal = MenuPrincipal(self)
        self.menu_pausa = MenuPausa(self)
        self.tela_game_over = TelaGameOver(self)
        self.ranking = Ranking(self)
        self.tela_de_upgrade_ativa = None

        #grupos de sprite
        self.all_sprites = AllSprites()
        self.item_group = pygame.sprite.Group()
        self.inimigos_grupo = pygame.sprite.Group()
        self.projeteis_grupo = pygame.sprite.Group()
        #buff
        self.buff = False


    def run(self):
        while self.running:
            delta_time = self.clock.tick(fps) / 1000 #define o fps do jogo e retorna o delta time em milisegundo, por isso divide por 1k
            self.eventos()#avalia acoes do jogador (cima, baixo, saiu do jogo, etc...)
            self.update(delta_time) #movimentacao
            self.draw()#desenha os sprites na tela
    
    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False #sai do jogo
            
            #menus
            if self.estado_do_jogo == "menu_principal":
                escolha = self.menu_principal.handle_event(evento)
                if escolha == 'Start Game':
                    self.iniciar_novo_jogo()
                if escolha == 'Ranking':
                    self.estado_do_jogo = 'ranking'
                if escolha == 'Sair':
                    self.running = False
            elif self.estado_do_jogo == "jogando":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    self.estado_do_jogo = "pausa"

            elif self.estado_do_jogo == "pausa":
                escolha = self.menu_pausa.handle_event(evento)
                if escolha == "Continuar":
                    self.estado_do_jogo = "jogando"
                elif escolha == "Sair para Menu":
                    self.estado_do_jogo = "menu_principal"
            elif self.estado_do_jogo == 'level_up':
                if self.tela_de_upgrade_ativa:
                    escolha_idx = self.tela_de_upgrade_ativa.handle_event(evento)
                    
                    if escolha_idx is not None:
                        #pega a arma escolhida a partir do índice
                        arma_escolhida = self.tela_de_upgrade_ativa.opcoes_de_armas[escolha_idx]
                        arma_escolhida.upgrade()
                        
                        self.estado_do_jogo = 'jogando' # Volta para o jogo
                        self.tela_de_upgrade_ativa = None # Limpa a tela de upgrade

            
            elif self.estado_do_jogo == 'ranking':
                action = self.ranking.handle_event(evento)
                if action == 'exit_to_menu':
                    self.estado_do_jogo = 'menu_principal'
            
            elif self.estado_do_jogo == "game_over":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    self.ranking.start_name_input(self.player.pontuacao)
                    self.estado_do_jogo = "ranking"

    def update(self, delta_time):
        if self.estado_do_jogo == "jogando":
            self.all_sprites.update(delta_time)

            self.tempo_proximo_spawn += delta_time
            
            #horda de inimigos
            if self.tempo_proximo_spawn >= self.intervalo_spawn_atual:
                self.tempo_proximo_spawn = 0
                for _ in range(5): # Cria 5 inimigos de uma vez
                    self.spawnar_inimigo()

            #o cronômetro já atingiu o tempo
            if self.tempo_proximo_spawn >= self.intervalo_spawn_atual:
                self.tempo_proximo_spawn = 0 # zera o cronômetro para a próxima contagem
                self.spawnar_inimigo()#cria o inimigo
            
            #Deixa o jogo mais difícil com o tempo
            if self.intervalo_spawn_atual > self.intervalo_minimo:
                 # Diminui um pouquinho o tempo de espera a cada segundo que passa
                self.intervalo_spawn_atual -= self.fator_dificuldade * delta_time

            #CODIGO PARA TESTE, DEVE SER REMOVIDO DEPOIS
            for arma in self.player.armas.values():
                arma.update()

            self.colisao()

            if self.player.vida_atual <= 0:
                self.estado_do_jogo = 'game_over'
                pygame.mixer.music.pause()  # pausa a música no game over

    def draw(self):
        if self.estado_do_jogo == "menu_principal":
            self.menu_principal.draw(self.tela)

        elif self.estado_do_jogo == 'jogando':
            self.tela.fill('black')
            self.all_sprites.draw(self.player.posicao)
            self.hud.draw(self.tela)

        elif self.estado_do_jogo == 'pausa':
            self.tela.fill('black')
            self.all_sprites.draw(self.player.posicao)
            self.menu_pausa.draw(self.tela)

        elif self.estado_do_jogo == 'ranking':
            self.ranking.draw(self.tela)

        elif self.estado_do_jogo == "game_over":
            self.tela_game_over.draw(self.tela)

        elif self.estado_do_jogo == "level_up":
            self.all_sprites.draw(self.player.posicao)
            self.hud.draw(self.tela)
            self.tela_de_upgrade_ativa.draw(self.tela)

        pygame.display.update()  #pinta a tela
    
    def iniciar_novo_jogo(self):
        self.all_sprites.empty()
        self.item_group.empty()
        self.projeteis_grupo.empty()
        self.inimigos_grupo.empty()

        self.tempo_proximo_spawn = 0
        self.intervalo_spawn_inicial = 2.0
        self.intervalo_spawn_atual = self.intervalo_spawn_inicial
        self.intervalo_minimo = 0.3
        self.fator_dificuldade = 0.05

        self.player = Player(
            sheet_player=join('assets', 'img', 'player.png'),
            grupos=self.all_sprites
        )

        # Certifique que o mixer está inicializado (melhor garantir)
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.stop()
        pygame.mixer.music.load(join('assets', 'sounds', 'musica_tema.wav'))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        if not hasattr(self.player, 'armas'):
            self.player.armas = {}

        arma_Loop = Arma_Loop(
            jogador=self.player,
            grupos=(self.all_sprites, self.projeteis_grupo, self.inimigos_grupo),
            game=self
        )
        self.player.armas['Laço'] = arma_Loop

        self.estado_do_jogo = 'jogando'
    
    def spawnar_inimigo(self):
        camera_center_x = self.player.posicao.x
        camera_center_y = self.player.posicao.y

        borda_esquerda = camera_center_x - largura_tela / 2
        borda_direita = camera_center_x + largura_tela / 2
        borda_topo = camera_center_y - altura_tela / 2
        borda_baixo = camera_center_y + altura_tela / 2
    
        lado = random.choice(['top', 'bottom', 'left', 'right'])
        if lado == 'top':
            pos = (random.uniform(borda_esquerda, borda_direita), borda_topo - 50)
        elif lado == 'bottom':
            pos = (random.uniform(borda_esquerda, borda_direita), borda_baixo + 50)
        elif lado == 'left':
            pos = (borda_esquerda - 50, random.uniform(borda_topo, borda_baixo))
        else: # 'right'
            pos = (borda_direita + 50, random.uniform(borda_topo, borda_baixo))
        
        # tipos de inimigos que podem aparecer
        tipos_de_inimigos_possiveis = [InimigoBase, InimigoCirculo, InimigoListaIP]

        # sorteia um tipo de inimigo aleatoriamente
        inimigo_escolhido = random.choice(tipos_de_inimigos_possiveis)
        # Instância do tipo  sorteado
        inimigo_escolhido(posicao=pos, grupos=(self.all_sprites, self.inimigos_grupo), jogador=self.player)


    def colisao(self):
        #coleta de itens
        colisao_player_items = pygame.sprite.spritecollide(self.player, self.item_group, dokill=True)
        if colisao_player_items:
            for item in colisao_player_items:
                if item.tipo in self.player.coletaveis:
                    self.player.coletaveis[item.tipo] += 1
                    #efeitos
                    if item.tipo == 'exp_shard':
                        if (self.player.experiencia_atual + 10) < self.player.experiencia_level_up:
                              self.player.experiencia_atual += 10
                        else:
                            self.player.experiencia_atual = self.player.experiencia_atual + 10 - self.player.experiencia_level_up
                            self.estado_do_jogo = 'level_up'
                            self.player.level_up()
                            self.tela_de_upgrade_ativa = TelaDeUpgrade(self.tela, self.player)
                    elif item.tipo == 'big_shard':
                        if (self.player.experiencia_atual + 50) < self.player.experiencia_level_up:
                              self.player.experiencia_atual += 50
                        else:
                            self.player.experiencia_atual = self.player.experiencia_atual + 50 - self.player.experiencia_level_up
                            self.estado_do_jogo = 'level_up'
                            self.player.level_up()
                            self.tela_de_upgrade_ativa = TelaDeUpgrade(self.tela, self.player)
                    elif item.tipo == 'life_orb':
                        if (self.player.vida_atual + 25) <= self.player.vida_maxima: 
                            self.player.vida_atual += 25
                        else:
                            self.player.vida_atual = self.player.vida_maxima
                    elif item.tipo == 'racket':
                        self.player.vida_atual = self.player.vida_maxima
                        self.player.experiencia_atual = self.player.experiencia_level_up
                        self.estado_do_jogo = 'level_up'
                        self.player.level_up()
                        self.tela_de_upgrade_ativa = TelaDeUpgrade(self.tela, self.player)
                        

                        

  
        #dano para o jogador em caso de colisão
        colisao_player_inimigos = pygame.sprite.spritecollide(self.player, self.inimigos_grupo, False)
        if colisao_player_inimigos != []:
            self.player.tomar_dano(colisao_player_inimigos[0])
        
        #colisão entre inimigos e projétil
        colisao_inimigo_projetil =  pygame.sprite.groupcollide(self.projeteis_grupo, self.inimigos_grupo, False, False)
        for projetil in self.projeteis_grupo:
            inimigos_em_contato_agora = colisao_inimigo_projetil.get(projetil, [])
             #converte para set
            set_inimigos_em_contato_agora = set(inimigos_em_contato_agora)
            #remove os inimigos que já foram acertados durante a colisão
            novos_acertos = set_inimigos_em_contato_agora - projetil.inimigos_atingidos

            for inimigo in novos_acertos:
                inimigo.vida -= projetil.dano
            #atualiza a memoria do projétil para quais inimigos estão em contato
            projetil.inimigos_atingidos = set_inimigos_em_contato_agora

        #morte dos inimigos caso vida zere + DROP
        for inimigo in list(self.inimigos_grupo):  #iterar sobre cópia
            if inimigo.vida <= 0:
                inimigo.morrer((self.all_sprites, self.item_group))
