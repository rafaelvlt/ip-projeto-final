import pygame
import os
from os.path import join
from settings import *  # Assumo que largura_tela, altura_tela e fps estão aqui

class MenuPrincipal:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.bg = pygame.image.load(join('assets', 'img', 'CInMenu.jpeg'))
        self.opcoes = ["Start Game", "Ranking", "Colaboradores", "Sair"]
        self.selecionada = 0

        # Carrega e toca a música de fundo do menu
        self.musica = join('assets', 'sounds', 'musica_menu.ogg')
        pygame.mixer.music.load(self.musica)
        pygame.mixer.music.play(-1)  # Loop infinito

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.selecionada = (self.selecionada - 1) % len(self.opcoes)
            elif event.key == pygame.K_s:
                self.selecionada = (self.selecionada + 1) % len(self.opcoes)
            elif event.key == pygame.K_RETURN:
                # Para a música do menu quando sair
                pygame.mixer.music.stop()
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
        self.bg = pygame.image.load(os.path.join('assets', 'img', 'game_over.png')).convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (largura_tela, altura_tela))

        # Carrega o som de game over
        self.som = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'game_over.wav'))
        self.som_tocado = False

    def draw(self, tela):
        if not self.som_tocado:
            self.som.play()
            self.som_tocado = True

        tela.blit(self.bg, (0, 0))


# Exemplo de Game com música tema no jogo
class Game:
    def __init__(self, tela):
        self.tela = tela
        self.clock = pygame.time.Clock()
        self.running = True

        # Inicializa menus e telas
        self.menu_principal = MenuPrincipal(self)
        self.menu_pausa = MenuPausa(self)
        self.tela_game_over = TelaGameOver(self)

        self.estado_do_jogo = "menu_principal"

    def iniciar_novo_jogo(self):
        # Iniciar música tema do jogo
        musica_jogo = join('assets', 'sounds', 'musica_tema.wav')
        pygame.mixer.music.load(musica_jogo)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

        self.estado_do_jogo = 'jogando'
        # Aqui você inicializaria o jogador, inimigos etc.

    def run(self):
        while self.running:
            delta_time = self.clock.tick(fps) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.estado_do_jogo == "menu_principal":
                    escolha = self.menu_principal.handle_event(event)
                    if escolha == 'Start Game':
                        self.iniciar_novo_jogo()
                    elif escolha == 'Sair':
                        self.running = False

                elif self.estado_do_jogo == "jogando":
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.estado_do_jogo = "pausa"

                elif self.estado_do_jogo == "pausa":
                    escolha = self.menu_pausa.handle_event(event)
                    if escolha == "Continuar":
                        self.estado_do_jogo = "jogando"
                    elif escolha == "Sair para Menu":
                        self.estado_do_jogo = "menu_principal"
                        # Volta a tocar a música do menu
                        self.menu_principal = MenuPrincipal(self)

                elif self.estado_do_jogo == "game_over":
                    # Exemplo: voltar ao menu com enter
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.estado_do_jogo = "menu_principal"
                        self.menu_principal = MenuPrincipal(self)

            self.draw()

        pygame.quit()

    def draw(self):
        if self.estado_do_jogo == "menu_principal":
            self.menu_principal.draw(self.tela)
        elif self.estado_do_jogo == "jogando":
            self.tela.fill((0, 0, 0))
            # desenha o jogo aqui
        elif self.estado_do_jogo == "pausa":
            self.menu_pausa.draw(self.tela)
        elif self.estado_do_jogo == "game_over":
            self.tela_game_over.draw(self.tela)

        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Jogo com Música")
    game = Game(tela)
    game.run()
