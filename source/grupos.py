import pygame
from settings import *

class Fundo(pygame.sprite.Sprite):
    def __init__(self, posicao, surface, grupos):
        super().__init__(grupos)
        self.image = surface
        self.rect = self.image.get_rect(topleft = posicao)

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.deslocamento = pygame.Vector2()




    def draw(self, alvo_posicao, superfice_alvo):

        self.deslocamento.x = -(alvo_posicao[0] - largura_tela / 2)
        self.deslocamento.y = -(alvo_posicao[1] - altura_tela / 2)

        
        sprites_de_fundo = []
        sprites_da_frente = []
        for sprite in self.sprites():
            if isinstance(sprite, Fundo):
                sprites_de_fundo.append(sprite)
            else:
                sprites_da_frente.append(sprite)

        # Desenha o fundo na superfície_alvo (tela_virtual)
        for sprite in sprites_de_fundo:
            posicao_na_tela = sprite.rect.topleft + self.deslocamento
            superfice_alvo.blit(sprite.image, posicao_na_tela)

        # Desenha os sprites da frente na superfície_alvo (tela_virtual)
        for sprite in sorted(sprites_da_frente, key=lambda s: s.rect.centery):
            posicao_na_tela = sprite.rect.topleft + self.deslocamento
            superfice_alvo.blit(sprite.image, posicao_na_tela)
