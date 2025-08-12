import pygame
import pytmx
from settings import *
from grupos import Fundo

class Mapa:
    def __init__(self, all_sprites):        

        self.tmx_data = pytmx.load_pygame(join('assets', 'map', 'mapa_cin.tmx'))

        largura_mapa_pixels = self.tmx_data.width * self.tmx_data.tilewidth
        altura_mapa_pixels = self.tmx_data.height * self.tmx_data.tileheight

        self.map_surface = pygame.Surface((largura_mapa_pixels, altura_mapa_pixels))
        self.map_surface = pygame.transform.scale(self.map_surface, (5000, 5000)
        )
        self.renderizar_mapa()

    def renderizar_mapa(self):

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        self.map_surface.blit(
                            tile_image, 
                            (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight)
                        )

    def draw(self, surface, deslocamento_camera):

        posicao_mapa_na_tela = self.map_surface.get_rect().move(deslocamento_camera)
        surface.blit(self.map_surface, posicao_mapa_na_tela)