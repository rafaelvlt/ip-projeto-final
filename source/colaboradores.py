import pygame
from os.path import join

class Colaboradores:
    def __init__(self, game):
        self.game = game
        self.font_title = pygame.font.Font(None, 60)
        self.font_text = pygame.font.Font(None, 36)

        # Lista de colaboradores
        self.colaboradores = [
            "Projeto desenvolvido por:",
            "",
            "Alvaro Lima",
            "Fulano da Silva",
            "Ciclano Pereira",
            "Beltrano Souza",
            "",
            "Apoio:",
            "Comunidade Pygame",
            "OpenAI",
            "",
            "Obrigado por jogar!"
        ]

        self.scroll_y = 0
        self.scroll_speed = 50  # pixels por segundo

        # --- Carrega a imagem de fundo ---
        self.background = pygame.image.load(join('assets', 'img', 'colaboradores.jpeg')).convert()
        self.background = pygame.transform.scale(self.background, (game.tela.get_width(), game.tela.get_height()))

    def iniciar_input(self):
        """Reseta o estado quando entra na tela"""
        self.scroll_y = 0

    def handle_event(self, evento):
        # Sair com ESC ou Enter
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                return "sair"
        return None

    def update(self, delta_time):
        # Faz o texto rolar automaticamente
        self.scroll_y -= self.scroll_speed * delta_time

    def draw(self, surface):
        # --- Desenha a imagem de fundo ---
        surface.blit(self.background, (0, 0))

        # Título
        titulo = self.font_title.render("Colaboradores", True, (255, 255, 0))
        surface.blit(titulo, (surface.get_width() // 2 - titulo.get_width() // 2, 50 + self.scroll_y))

        # Texto dos colaboradores
        y_offset = 150
        for linha in self.colaboradores:
            texto = self.font_text.render(linha, True, (255, 255, 255))
            surface.blit(texto, (surface.get_width() // 2 - texto.get_width() // 2, y_offset + self.scroll_y))
            y_offset += 40
