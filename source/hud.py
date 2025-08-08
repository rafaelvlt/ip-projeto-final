import pygame
from settings import *
from player import *

class HUD:
    def __init__(self, game):
        self.game = game
        #seta fonte para o numero da hud
        self.font = pygame.font.Font(None, 36)
        
        #pega imagem e da scale para ficar menor
        #xp
        self.icone_exp_shard = pygame.image.load(join('assets', 'img', 'expShard.png')).convert_alpha()
        self.icone_exp_shard = pygame.transform.scale(self.icone_exp_shard, (30, 30))
        #big shard
        self.icone_big_shard = pygame.image.load(join('assets', 'img', 'bigShard.png')).convert_alpha()
        self.icone_big_shard = pygame.transform.scale(self.icone_big_shard, (30, 30))
        #life orb
        self.icone_life_orb = pygame.image.load(join('assets', 'img', 'lifeOrb.png')).convert_alpha()
        self.icone_life_orb = pygame.transform.scale(self.icone_life_orb, (30, 30))
    
    def draw(self, tela):
        #pega quantidade de cada coletavel
        contagem_exp = self.game.player.coletaveis['exp_shard']
        contagem_big = self.game.player.coletaveis['big_shard']
        contagem_life = self.game.player.coletaveis['life_orb']

        #texto
        life_surf = self.font.render(f'{contagem_life}', True, 'white')
        life_rect = life_surf.get_rect(midleft = (60, 40))

        exp_surf = self.font.render(f'{contagem_exp}', True, 'white')
        exp_rect = exp_surf.get_rect(midleft = (60, 90))

        big_surf = self.font.render(f'{contagem_big}', True, 'white')
        big_rect = big_surf.get_rect(midleft = (60, 140))


        tela.blit(self.icone_life_orb, (20, 25))
        tela.blit(life_surf, life_rect)


        tela.blit(self.icone_exp_shard, (20, 75))
        tela.blit(exp_surf, exp_rect)

        tela.blit(self.icone_big_shard, (20, 125))
        tela.blit(big_surf, big_rect)