import pygame
import os
from os.path import join
from settings import *  # largura_tela, altura_tela, fps
# ------------------- MENUS -------------------

class MenuPrincipal:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.bg = pygame.image.load(join('assets', 'img', 'CInMenu.jpeg'))
        self.bg = pygame.transform.scale(self.bg, (largura_tela, altura_tela))
        self.bg_rect = self.bg.get_rect(center=self.game.tela.get_rect().center)
        self.opcoes = ["Start Game", "Opções", "Ranking", "Colaboradores", "Sair"]
        self.selecionada = 0



    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.selecionada = (self.selecionada - 1) % len(self.opcoes)
            elif event.key == pygame.K_s:
                self.selecionada = (self.selecionada + 1) % len(self.opcoes)
            elif event.key == pygame.K_RETURN:
                return self.opcoes[self.selecionada]
        return None

    def draw(self, tela):
        tela.blit(self.bg, (0, 0))
        for i, texto in enumerate(self.opcoes):
            cor = (255, 0, 0) if i == self.selecionada else (255, 255, 255)
            txt = self.font.render(texto, True, cor)
            tela.blit(txt, (100, 100 + i * 60))


class MenuPausa:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.opcoes = ["Continuar", "Sair para Menu"]
        self.selecionada = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.selecionada = (self.selecionada - 1) % len(self.opcoes)
            elif event.key == pygame.K_s:
                self.selecionada = (self.selecionada + 1) % len(self.opcoes)
            elif event.key == pygame.K_RETURN:
                return self.opcoes[self.selecionada]
        return None

    def draw(self, tela):
        tela.fill((10, 10, 10))
        for i, texto in enumerate(self.opcoes):
            cor = (0, 200, 200) if i == self.selecionada else (200, 200, 200)
            txt = self.font.render(texto, True, cor)
            tela.blit(txt, (120, 120 + i * 50))


class TelaGameOver:
    def __init__(self, game):
        self.game = game
        self.bg = pygame.image.load(join('assets', 'img', 'game_over.png')).convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (largura_tela, altura_tela))
        self.som = pygame.mixer.Sound(join('assets', 'sounds', 'game_over.wav'))
        self.som_tocado = False

    def draw(self, tela):
        if not self.som_tocado:
            self.som.play()
            self.som_tocado = True
        tela.blit(self.bg, (0, 0))

class MenuOpcoes:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 48)

        self.volumes_disponiveis = [round(i * 0.1, 2) for i in range(11)]
        try:
            self.vol_idx_atual = self.volumes_disponiveis.index(self.game.config['volume_musica'])
        except ValueError:
            self.vol_idx_atual = 10 

        self.resolucoes = [
            # Proporção 4:3
            (800, 600),
            (1024, 768),
            (1280, 960),
            # Proporção 16:9 (Widescreen)
            (1280, 720), 
            (1366, 768), 
            (1600, 900), 
            (1920, 1080),
            # Proporção 16:10 (Comum em monitores de PC)
            (1280, 800),
            (1440, 900),
            (1680, 1050)
        ]
        
        try:
            self.res_idx_atual = self.resolucoes.index(tuple(self.game.config['resolucao']))
        except ValueError:
            self.res_idx_atual = self.resolucoes.index((1280, 720))

        self.opcoes_texto = []
        self.opcoes_rects = []
        self.selecionada = 0
        self.atualizar_textos()


        self.bg = pygame.image.load(join('assets', 'img', 'CInMenu.jpeg'))
        self.bg = pygame.transform.scale(self.bg, (largura_tela, altura_tela))
        self.bg_rect = self.bg.get_rect(center=self.game.tela.get_rect().center)
        
    def atualizar_textos(self):
        """Atualiza o texto das opções para refletir o estado atual."""

        res_txt = f"{self.game.config['resolucao'][0]}x{self.game.config['resolucao'][1]}"
        tela_cheia_txt = "Ligado" if self.game.config['tela_cheia'] else "Desligado"

        volume_percentual = int(self.game.config['volume_musica'] * 100)
        musica_txt = f"{volume_percentual}%"
        if volume_percentual == 0:
            musica_txt = "Mudo"


        self.opcoes_texto = [
            f"Resolução: < {res_txt} >",
            f"Tela Cheia: < {tela_cheia_txt} >",
            f"Volume da Música: < {musica_txt} >",
            "Salvar e Voltar"
        ]
        # Recalcula a posição dos retângulos para o mouse
        self.opcoes_rects = []
        for i, texto in enumerate(self.opcoes_texto):
            txt_surf = self.font.render(texto, True, 'white')
            pos_x = (LARGURA_LOGICA - txt_surf.get_width()) / 2
            pos_y = 250 + i * 70
            self.opcoes_rects.append(txt_surf.get_rect(topleft=(pos_x, pos_y)))

    def _selecionar(self):
        """Executa a ação da opção selecionada e retorna um sinal se for para sair."""
        if self.selecionada == 0: # Mudar Resolução
            self.res_idx_atual = (self.res_idx_atual + 1) % len(self.resolucoes)
            self.game.config['resolucao'] = self.resolucoes[self.res_idx_atual]
            self.game.tela_real, self.game.tela_virtual = self.game._aplicar_config_tela()
        elif self.selecionada == 1: # Mudar Tela Cheia
            self.game.config['tela_cheia'] = not self.game.config['tela_cheia']
            self.game.tela_real, self.game.tela_virtual = self.game._aplicar_config_tela()
        elif self.selecionada == 2: # Volume da Música
            self.vol_idx_atual = (self.vol_idx_atual + 1) % len(self.volumes_disponiveis)
            novo_volume = self.volumes_disponiveis[self.vol_idx_atual]
            self.game.config['volume_musica'] = novo_volume
            pygame.mixer.music.set_volume(novo_volume)

        elif self.selecionada == 3: # Voltar
            self.game._salvar_config()
            return 'voltar_para_menu_principal' 
        
        self.atualizar_textos()
        return None 

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP):
                self.selecionada = (self.selecionada - 1) % len(self.opcoes_texto)
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                self.selecionada = (self.selecionada + 1) % len(self.opcoes_texto)
             # --- NOVA LÓGICA PARA NAVEGAÇÃO LATERAL ---
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                self._mudar_opcao('esquerda')
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                self._mudar_opcao('direita')
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self._selecionar() 

        if event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.opcoes_rects):
                if rect.collidepoint(event.pos):
                    self.selecionada = i
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.opcoes_rects[self.selecionada].collidepoint(event.pos):
                return self._selecionar()
                
        return None 
    
    def _mudar_opcao(self, direcao):
        """Muda o valor de uma opção selecionada para a esquerda ou direita."""
        if self.selecionada == 0:
            incremento = 1 if direcao == 'direita' else -1
            self.res_idx_atual = (self.res_idx_atual + incremento) % len(self.resolucoes)
            self.game.config['resolucao'] = self.resolucoes[self.res_idx_atual]
            self.game.tela_real, self.game.tela_virtual = self.game._aplicar_config_tela()

        elif self.selecionada == 1:

            self.game.config['tela_cheia'] = not self.game.config['tela_cheia']
            self.game.tela_real, self.game.tela_virtual = self.game._aplicar_config_tela()
        
        elif self.selecionada == 2:
            incremento = 1 if direcao == 'direita' else -1
            self.vol_idx_atual = (self.vol_idx_atual + incremento) % len(self.volumes_disponiveis)
            novo_volume = self.volumes_disponiveis[self.vol_idx_atual]
            self.game.config['volume_musica'] = novo_volume
            pygame.mixer.music.set_volume(novo_volume)

        self.atualizar_textos()
    
    def draw(self, tela):
        tela.blit(self.bg, (0, 0))
        for i, texto in enumerate(self.opcoes_texto):
            rect = self.opcoes_rects[i]
            cor = (255, 215, 0) if i == self.selecionada else (200, 200, 200)
            txt_surf = self.font.render(texto, True, cor)
            tela.blit(txt_surf, rect)
