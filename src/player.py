import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sheet_player):
        """
        Inicia o jogador.
        x: Posição x inicial.
        y: Posição y inicial.
        sheet_player: Imagem.
        """
        super().__init__()
        self.x = x
        self.y = y
        self.speed = 5

        self.dimensao_x_boneco = 32
        self.dimensao_y_boneco = 32

        self.frame = pygame.image.load(sheet_player).convert_alpha()

        self.image = self.frame
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, tela):
        """
        Renderiza os elementos do nivel
        """
        tela.all_sprites.draw(tela)

