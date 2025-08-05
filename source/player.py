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

    def update(self, keys):#movimentacao do player
        dx, dy = 0,0
        if keys[pygame.K_w]: #cima
            dy = -self.speed
        
        elif keys[pygame.K_s]: #baixo
            dy = self.speed

        if keys[pygame.K_a]: #esquerda
            dx = -self.speed

        elif keys[pygame.K_d]: #direita
            dx = self.speed

        if dx != 0 and dy != 0: #igualar velocidade na diagonal
            dx *= 0.7071
            dy *= 0.7071

        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y) #atualiza o x e y atual

   

