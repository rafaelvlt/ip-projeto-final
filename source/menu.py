import pygame
import json
import os
from settings import *

# -----------------------------------------
# Classe: SistemaSaveLoad
# -----------------------------------------
#class SistemaSaveLoad:
#  def __init__(self, arquivo="save.json"):
#        self.arquivo = arquivo
#
#   def salvar(self, dados):
#       with open(self.arquivo, "w") as f:
#          json.dump(dados, f)

#   def carregar(self):
#       if os.path.exists(self.arquivo):
#           with open(self.arquivo, "r") as f:
#               return json.load(f)
#       return {}

# -----------------------------------------
# Classe: MenuPrincipal
# -----------------------------------------
class MenuPrincipal:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.bg = pygame.image.load(join('assets', 'img', 'CInMenu.jpeg'))
        self.opcoes = ["Start Game", "Ranking", "Colaboradores", "Sair"]
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
        tela.blit(self.bg)
        for i, texto in enumerate(self.opcoes):
            cor = (255, 0, 0) if i == self.selecionada else (255, 255, 255)
            txt = self.font.render(texto, True, cor)
            tela.blit(txt, (100, 100 + i * 60))

# -----------------------------------------
# Classe: MenuPausa
# -----------------------------------------
class MenuPausa:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.opcoes = ["Continuar", "Sair para Menu"]
        self.selecionada = 0
        #self.salvador = SistemaSaveLoad()

    def handle_event(self, event, dados_para_salvar=None):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.selecionada = (self.selecionada - 1) % len(self.opcoes)
            elif event.key == pygame.K_s:
                self.selecionada = (self.selecionada + 1) % len(self.opcoes)
            elif event.key == pygame.K_RETURN:
                escolha = self.opcoes[self.selecionada]
                if escolha == "Salvar" and dados_para_salvar:
                    self.salvador.salvar(dados_para_salvar)
                return escolha
        return None

    def draw(self, tela):
        tela.fill((10, 10, 10))
        for i, texto in enumerate(self.opcoes):
            cor = (0, 200, 200) if i == self.selecionada else (200, 200, 200)
            txt = self.font.render(texto, True, cor)
            tela.blit(txt, (120, 120 + i * 50))

# -----------------------------------------
# Classe: TelaGameOver
# -----------------------------------------
class TelaGameOver:
    def __init__(self, game):
        self.font = pygame.font.SysFont(None, 72)

    def draw(self, tela):
        tela.fill((0, 0, 0))
        texto = self.font.render("GAME OVER", True, (255, 0, 0))
        tela.blit(texto, (150, 180))