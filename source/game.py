import pygame
import random
import json
from os.path import join
from settings import *
from player import Player 
from menu import *
from hud import *
from enemies import InimigoBug, InimigoListaIP, InimigoErro, BossInimigo, InimigoLadrao, InimigoPython
from weapon import Arma_Loop, ArmaLista, Dicionario_Divino, ArmaByte
from grupos import AllSprites
from colaboradores import TelaColaboradores
from ranking import Ranking 
from levelup import *
from mapa import Mapa
from weapon import Arma_Loop, ArmaLista, Dicionario_Divino


class Game:
    def __init__(self):
        #configurações
        self.config = self._carregar_config()
        self.tela, self.tela_virtual = self._aplicar_config_tela()
        pygame.display.set_caption("IP-ocalipse Cin-vivors")

        #variáveis de jogo
        self.running = True
        self.clock = pygame.time.Clock()
        self.estado_do_jogo = "menu_principal"

        # Sprites e grupos
        self.all_sprites = AllSprites()
        self.item_group = pygame.sprite.Group()
        self.projeteis_grupo = pygame.sprite.Group()
        self.auras_grupo = pygame.sprite.Group()
        self.inimigos_grupo = pygame.sprite.Group()

        # Menus
        self.menu_principal = MenuPrincipal(self)
        self.menu_pausa = MenuPausa(self)
        self.menu_opcoes = MenuOpcoes(self)
        self.tela_game_over = TelaGameOver(self)
        self.tela_colaboradores = TelaColaboradores(self)
        self.ranking = Ranking(self)
        self.tela_colaboradores = TelaColaboradores(self)

        #musica
        self.musicas = {
            'menu': join('assets', 'sounds', 'musica_menu.ogg'),
            'jogo': join('assets', 'sounds', 'musica_tema.wav')
        }
        self.musica_atual = None

        # Player e HUD
        self.player = None
        self.hud = HUD(self)
        self.tela_de_upgrade_ativa = None
        self.buff = False

        # Controle de spawn
        self.tempo_proximo_spawn = 0
        self.intervalo_spawn_atual = 2.0
        self.intervalo_minimo = 0.5
        self.fator_dificuldade = 0.01
        self.hordas_contagem = 0

    def _carregar_config(self):
        try:
            with open('config.json', 'r') as f: return json.load(f)
        except FileNotFoundError:
            return {"resolucao": [1280, 960], "tela_cheia": False, "volume_musica": 0.3}

    def _salvar_config(self):
        with open('config.json', 'w') as f: json.dump(self.config, f, indent=4)

    def _aplicar_config_tela(self):
        largura, altura = self.config['resolucao']
        flags = 0
        if self.config['tela_cheia']:
            flags = pygame.FULLSCREEN
        
        tela = pygame.display.set_mode((largura, altura), flags)
        tela_virtual = pygame.Surface((LARGURA_LOGICA, ALTURA_LOGICA))
        return tela, tela_virtual
    
    def _gerenciar_musica(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        musica_desejada = None
        if self.estado_do_jogo in ['menu_principal', 'opcoes', 'ranking', 'colaboradores', 'game_over']:
            musica_desejada = self.musicas['menu']
        elif self.estado_do_jogo == 'jogando':
            musica_desejada = self.musicas['jogo']

        if musica_desejada and musica_desejada != self.musica_atual:

            pygame.mixer.music.stop()
            

            pygame.mixer.music.load(musica_desejada)
            pygame.mixer.music.set_volume(self.config['volume_musica'])
            pygame.mixer.music.play(-1) 
            

            self.musica_atual = musica_desejada
        
        elif musica_desejada is None and self.musica_atual is not None:
             pygame.mixer.music.pause()
             self.musica_atual = None

    def iniciar_novo_jogo(self):
        self.all_sprites.empty()
        self.item_group.empty()
        self.projeteis_grupo.empty()
        self.inimigos_grupo.empty()
        self.tempo_proximo_spawn = 0
        self.intervalo_spawn_atual = 2.0
        self.hordas_contagem = 0

        # Inicializa player
        self.player = Player(
            posicao_inicial=(self.mapa.largura_mapa_pixels / 2, self.mapa.altura_mapa_pixels),
            sheet_player=join('assets', 'img', 'player.png'),
            grupos=self.all_sprites,
            game=self
        )
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
                elif escolha == 'Opções':
                    self.estado_do_jogo = 'opcoes'
                if escolha == 'Colaboradores':
                    self.estado_do_jogo = 'colaboradores'
                if escolha == 'Ranking':
                    self.estado_do_jogo = 'ranking'
                elif escolha == 'Colaboradores':
                    self.estado_do_jogo = 'colaboradores'
                elif escolha == 'Sair':
                    self.running = False

            # JOGANDO
            elif self.estado_do_jogo == "jogando":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    self.estado_do_jogo = "pausa"

            # PAUSA
            elif self.estado_do_jogo == 'opcoes':
                acao = self.menu_opcoes.handle_event(evento)
                if acao == 'voltar_para_menu_principal':
                    self.estado_do_jogo = 'menu_principal'

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
           
                    if escolha_idx is not None and escolha_idx < len(self.tela_de_upgrade_ativa.opcoes_de_armas_obj):
                        arma_escolhida = self.tela_de_upgrade_ativa.opcoes_de_armas_obj[escolha_idx]
                        nome_da_arma = arma_escolhida.nome
                        
                        #upgrade em arma no inventario
                        if nome_da_arma in self.player.armas:
                            self.player.armas[nome_da_arma].upgrade()
                        #nova arma
                        else:
                            self.player.armas[nome_da_arma] = arma_escolhida 
                            arma_escolhida.equipar()
                        
                        self.estado_do_jogo = 'jogando'
                        self.tela_de_upgrade_ativa = None
            
            #tela de colaboradores
            elif self.estado_do_jogo == 'colaboradores':
                self.tela_colaboradores.handle_event(evento)
            #tela de ranking
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
            if self.player:
                for arma in self.player.armas.values():
                    arma.update(delta_time)

            if self.tempo_proximo_spawn >= self.intervalo_spawn_atual:
                self.tempo_proximo_spawn = 0
                self.hordas_contagem += 1
                
                for _ in range(4):
                    self.spawnar_inimigo()

                if self.hordas_contagem % 5 == 0:
                    self.spawnar_inimigo(tipo='boss')
                if self.hordas_contagem > 0 and self.hordas_contagem % 100 == 0:
                # Spawna o inimigo especial que aparece a cada 100 hordas
                    self.spawnar_inimigo(tipo='inimigo_horda_100')

            if self.intervalo_spawn_atual > self.intervalo_minimo:
                self.intervalo_spawn_atual -= self.fator_dificuldade * delta_time

            self.colisao(delta_time)

            if self.player.vida_atual <= 0:
                #atualizacao pos morte para o ranking
                self.player.pontuacao += self.player.experiencia_atual
                for tipo, contagem in self.player.coletaveis.items():
                    if tipo == 'exp_shard':
                        self.player.pontuacao += contagem
                    elif tipo == 'big_shard':
                        self.player.pontuacao += contagem * 2
                    elif tipo == 'life_orb':
                        self.player.pontuacao += contagem * 3
                    elif tipo == 'cafe':
                        self.player.pontuacao += 10
                self.estado_do_jogo = 'game_over'


    def draw(self):
        self.tela_virtual.fill('black')

        if self.estado_do_jogo == "menu_principal":
            self.menu_principal.draw(self.tela_virtual)

        elif self.estado_do_jogo in ['jogando', 'pausa', 'level_up', 'game_over']:
            deslocamento = self.mapa.get_camera_offset(self.player.posicao, (largura_tela, altura_tela))
            self.mapa.draw(self.tela_virtual, deslocamento)

            self.all_sprites.draw(self.player.posicao, self.tela_virtual)

            self.hud.draw(self.tela_virtual)

            if self.estado_do_jogo == 'pausa':
                self.menu_pausa.draw(self.tela_virtual)

            elif self.estado_do_jogo == 'level_up' and self.tela_de_upgrade_ativa:
                self.tela_de_upgrade_ativa.draw(self.tela_virtual)

            elif self.estado_do_jogo == 'game_over':
                self.tela_game_over.draw(self.tela_virtual)
            
        elif self.estado_do_jogo == 'opcoes':
            self.menu_opcoes.draw(self.tela_virtual)
            
        elif self.estado_do_jogo == 'colaboradores':
            self.tela_colaboradores.draw(self.tela_virtual)

        elif self.estado_do_jogo == 'ranking':
            self.ranking.draw(self.tela_virtual)
        
        self._projetar_na_tela_real()
        pygame.display.update()
    
    def _projetar_na_tela_real(self):
        """Pega a tela_virtual, redimensiona e desenha na tela_real."""
        self.tela.fill((0, 0, 0))

        
        escala_x = self.tela.get_width() / LARGURA_LOGICA
        escala_y = self.tela.get_height() / ALTURA_LOGICA
        fator_escala = min(escala_x, escala_y)

        
        nova_largura = int(LARGURA_LOGICA * fator_escala)
        nova_altura = int(ALTURA_LOGICA * fator_escala)
        tela_escalada = pygame.transform.scale(self.tela_virtual, (nova_largura, nova_altura))
        
        
        pos_x = (self.tela.get_width() - nova_largura) / 2
        pos_y = (self.tela.get_height() - nova_altura) / 2

        
        self.tela.blit(tela_escalada, (pos_x, pos_y))
    
    def iniciar_novo_jogo(self):
        self.all_sprites.empty()
        self.item_group.empty()
        self.projeteis_grupo.empty()
        self.inimigos_grupo.empty()

        self.tempo_proximo_spawn = 0
        self.intervalo_spawn_inicial = 2.0
        self.intervalo_spawn_atual = self.intervalo_spawn_inicial
        self.intervalo_minimo = 0.3
        self.fator_dificuldade = 0.04

        self.mapa = Mapa(all_sprites=self.all_sprites)
        self.player = Player(
            posicao_inicial=(self.mapa.largura_mapa_pixels / 2, self.mapa.altura_mapa_pixels),
            sheet_player=join('assets', 'img', 'player.png'),
            grupos=self.all_sprites,
            game=self
        )



        if not hasattr(self.player, 'armas'):
            self.player.armas = {}

        #arma inicial
        arma_Loop = Arma_Loop(
            jogador=self.player,
            grupos=(self.all_sprites, self.projeteis_grupo, self.inimigos_grupo),
            game=self
        )

        #arma_listas = ArmaLista(jogador=self.player,
                                #grupos=(self.all_sprites, self.projeteis_grupo),
                                #game=self)
                        
        #arma_dicionario = Dicionario_Divino(jogador=self.player,
                     #grupos=(self.all_sprites, self.auras_grupo),
                     #game=self)
        #arma_byte = ArmaByte(
    #jogador=self.player,
    #grupos=(self.all_sprites, self.inimigos_grupo, self.item_group),
    #game=self)

        self.player.armas[arma_Loop.nome] = arma_Loop
        #self.player.armas['Listas'] = arma_listas
        #self.player.armas['Nova'] = arma_dicionario
        #self.player.armas['Byte'] = arma_byte

        self.estado_do_jogo = 'jogando'
    
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
            pos = (random.uniform(borda_esquerda,
                   borda_direita), borda_baixo + 50)
        elif lado == 'left':
            pos = (borda_esquerda - 50, random.uniform(borda_topo, borda_baixo))
        else:  # 'right'
            pos = (borda_direita + 50, random.uniform(borda_topo, borda_baixo))

        # --- Lógica de qual inimigo criar ---
        if tipo == 'boss':
            # Se o tipo for 'boss', cria uma instância do BossInimigo
            BossInimigo(posicao=pos, grupos=(self.all_sprites,
                        self.inimigos_grupo), jogador=self.player)
        elif tipo == 'inimigo_horda_100':
            # Inimigo especial que aparece a cada 100 hordas
            InimigoLadrao(posicao=pos, grupos=(
                self.all_sprites, self.inimigos_grupo), jogador=self.player)    
        else:  # Se o tipo for 'normal'
            tipos_de_inimigos_possiveis = [
                InimigoErro, InimigoListaIP, InimigoBug, InimigoPython]
            inimigo_escolhido = random.choice(tipos_de_inimigos_possiveis)
            inimigo_escolhido(posicao=pos, grupos=(
                self.all_sprites, self.inimigos_grupo), jogador=self.player)


    def colisao(self, delta_time):
        # Coleta de itens
        itens_coletados = pygame.sprite.spritecollide(self.player, self.item_group, dokill=True)
        for item in itens_coletados:
            self.player.coletar_item(item)

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
        # colisao com dot
        if self.auras_grupo:
            colisoes_aura = pygame.sprite.groupcollide(
                self.inimigos_grupo, 
                self.auras_grupo, 
                False, 
                False, 
                pygame.sprite.collide_circle
            )
            for inimigo, auras in colisoes_aura.items():
                for aura in auras: 
                    dano_neste_frame = aura.dano_por_segundo * delta_time
                    inimigo.vida -= dano_neste_frame


        # Morte de inimigos
        for inimigo in list(self.inimigos_grupo):
            if inimigo.vida <= 0:
                inimigo.morrer((self.all_sprites, self.item_group))
    def run(self):
        while self.running:
            self._gerenciar_musica()

            delta_time = self.clock.tick(fps) / 1000
            self.eventos()
            self.update(delta_time)
            self.draw()
