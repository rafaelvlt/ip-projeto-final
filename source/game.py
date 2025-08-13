import pygame
import random
from os.path import join
from settings import *
from player import Player
from menu import *
from hud import *
from enemies import InimigoBase, InimigoBug, InimigoListaIP, InimigoErro, BossInimigo
from grupos import AllSprites
from ranking import Ranking
from levelup import *
from colaboradores import Colaboradores

class Game:
    def __init__(self, tela):
        self.tela = tela
        self.running = True
        self.clock = pygame.time.Clock()
        self.estado_do_jogo = "menu_principal"

        # Sprites e grupos
        self.all_sprites = AllSprites()
        self.item_group = pygame.sprite.Group()
        self.projeteis_grupo = pygame.sprite.Group()
        self.inimigos_grupo = pygame.sprite.Group()

        # Menus
        self.menu_principal = MenuPrincipal(self)
        self.menu_pausa = MenuPausa(self)
        self.ranking = Ranking(self)
        self.colaboradores = Colaboradores(self)

        # Player e HUD
        self.player = None
        self.hud = None
        self.tela_de_upgrade_ativa = None

        # Controle de spawn
        self.tempo_proximo_spawn = 0
        self.intervalo_spawn_atual = 2.0
        self.intervalo_minimo = 0.5
        self.fator_dificuldade = 0.01
        self.hordas_contagem = 0

    def iniciar_novo_jogo(self):
        self.all_sprites.empty()
        self.item_group.empty()
        self.projeteis_grupo.empty()
        self.inimigos_grupo.empty()
        self.tempo_proximo_spawn = 0
        self.intervalo_spawn_atual = 2.0
        self.hordas_contagem = 0

        # Inicializa player
        self.player = Player(self, 400, 300)
        self.hud = HUD(self)
        self.estado_do_jogo = "jogando"

    def spawnar_inimigo(self, tipo='normal'):
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
        else:
            pos = (borda_direita + 50, random.uniform(borda_topo, borda_baixo))

        if tipo == 'boss':
            BossInimigo(posicao=pos, grupos=(self.all_sprites, self.inimigos_grupo), jogador=self.player)
        else:
            tipos_de_inimigos = [InimigoErro, InimigoListaIP, InimigoBug]
            inimigo = random.choice(tipos_de_inimigos)
            inimigo(posicao=pos, grupos=(self.all_sprites, self.inimigos_grupo), jogador=self.player)

    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and (evento.mod & pygame.KMOD_ALT):
                    pygame.display.toggle_fullscreen()

            # MENU PRINCIPAL
            if self.estado_do_jogo == "menu_principal":
                escolha = self.menu_principal.handle_event(evento)
                if escolha == 'Start Game':
                    self.iniciar_novo_jogo()
                elif escolha == 'Ranking':
                    self.estado_do_jogo = 'ranking'
                elif escolha == 'Colaboradores':
                    self.estado_do_jogo = 'colaboradores'
                    self.colaboradores.iniciar_input()
                elif escolha == 'Sair':
                    self.running = False

            # JOGANDO
            elif self.estado_do_jogo == "jogando":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    self.estado_do_jogo = "pausa"

            # PAUSA
            elif self.estado_do_jogo == "pausa":
                escolha = self.menu_pausa.handle_event(evento)
                if escolha == "Continuar":
                    self.estado_do_jogo = "jogando"
                elif escolha == "Sair para Menu":
                    self.estado_do_jogo = "menu_principal"
                    self.menu_principal = MenuPrincipal(self)

            # LEVEL UP
            elif self.estado_do_jogo == 'level_up':
                if self.tela_de_upgrade_ativa:
                    escolha_idx = self.tela_de_upgrade_ativa.handle_event(evento)
                    if escolha_idx is not None:
                        arma_escolhida = self.tela_de_upgrade_ativa.opcoes_de_armas[escolha_idx]
                        arma_escolhida.upgrade()
                        self.estado_do_jogo = 'jogando'
                        self.tela_de_upgrade_ativa = None

            # RANKING
            elif self.estado_do_jogo == 'ranking':
                action = self.ranking.handle_event(evento)
                if action == 'exit_to_menu':
                    self.estado_do_jogo = 'menu_principal'

            # COLABORADORES
            elif self.estado_do_jogo == 'colaboradores':
                action = self.colaboradores.handle_event(evento)
                if action == 'sair':
                    self.estado_do_jogo = 'menu_principal'

            # GAME OVER
            elif self.estado_do_jogo == "game_over":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    if hasattr(self, 'player'):
                        self.ranking.start_name_input(self.player.pontuacao)
                    self.estado_do_jogo = "ranking"

    def update(self, delta_time):
        if self.estado_do_jogo == "jogando":
            self.all_sprites.update(delta_time)
            self.tempo_proximo_spawn += delta_time

            if self.tempo_proximo_spawn >= self.intervalo_spawn_atual:
                self.tempo_proximo_spawn = 0
                self.hordas_contagem += 1

                for _ in range(4):
                    self.spawnar_inimigo()

                if self.hordas_contagem % 5 == 0:
                    self.spawnar_inimigo(tipo='boss')

            if self.intervalo_spawn_atual > self.intervalo_minimo:
                self.intervalo_spawn_atual -= self.fator_dificuldade * delta_time

            self.colisao()

            if self.player.vida_atual <= 0:
                self.estado_do_jogo = 'game_over'
                pygame.mixer.music.pause()

    def colisao(self):
        # Coleta de itens
        colisao_items = pygame.sprite.spritecollide(self.player, self.item_group, dokill=True)
        for item in colisao_items:
            if item.tipo in self.player.coletaveis:
                self.player.coletaveis[item.tipo] += 1
                # Adiciona efeitos específicos
                if item.tipo in ['exp_shard', 'big_shard']:
                    self.player.experiencia_atual += 10 if item.tipo == 'exp_shard' else 50
                    if self.player.experiencia_atual >= self.player.experiencia_level_up:
                        self.estado_do_jogo = 'level_up'
                        self.player.level_up()
                        self.tela_de_upgrade_ativa = TelaDeUpgrade(self.tela, self.player)
                elif item.tipo == 'life_orb':
                    self.player.vida_atual = min(self.player.vida_atual + 25, self.player.vida_maxima)
                elif item.tipo == 'racket':
                    self.player.vida_atual = self.player.vida_maxima
                    self.player.experiencia_atual = self.player.experiencia_level_up
                    self.estado_do_jogo = 'level_up'
                    self.player.level_up()
                    self.tela_de_upgrade_ativa = TelaDeUpgrade(self.tela, self.player)

        # Colisão com inimigos
        colisao_inimigos = pygame.sprite.spritecollide(self.player, self.inimigos_grupo, False)
        for inimigo in colisao_inimigos:
            self.player.tomar_dano(inimigo)

        # Colisão projéteis x inimigos
        colisao_projetil = pygame.sprite.groupcollide(self.projeteis_grupo, self.inimigos_grupo, False, False)
        for projetil, inimigos in colisao_projetil.items():
            novos_acertos = set(inimigos) - projetil.inimigos_atingidos
            for inimigo in novos_acertos:
                inimigo.vida -= projetil.dano
            projetil.inimigos_atingidos = set(inimigos)

        # Morte de inimigos
        for inimigo in list(self.inimigos_grupo):
            if inimigo.vida <= 0:
                inimigo.morrer((self.all_sprites, self.item_group))

    def draw(self):
        self.tela.fill((0,0,0))
        if self.estado_do_jogo == "menu_principal":
            self.menu_principal.draw(self.tela)
        elif self.estado_do_jogo == "jogando":
            self.all_sprites.draw(self.tela)
            if self.hud:
                self.hud.draw(self.tela)
        elif self.estado_do_jogo == "pausa":
            self.menu_pausa.draw(self.tela)
        elif self.estado_do_jogo == "ranking":
            self.ranking.draw(self.tela)
        elif self.estado_do_jogo == "colaboradores":
            self.colaboradores.draw(self.tela)
        elif self.estado_do_jogo == "game_over":
            self.tela_game_over.draw(self.tela)
        elif self.estado_do_jogo == "level_up" and self.tela_de_upgrade_ativa:
            self.all_sprites.draw(self.tela)
            self.hud.draw(self.tela)
            self.tela_de_upgrade_ativa.draw(self.tela)

        pygame.display.flip()

    def run(self):
        while self.running:
            delta_time = self.clock.tick(fps) / 1000
            self.eventos()
            self.update(delta_time)
            self.draw()