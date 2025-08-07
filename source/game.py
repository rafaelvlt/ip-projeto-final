import pygame
from settings import *
from player import *
from items import *
from weapon import *
from os.path import join

#CÓDIGO PARA TESTAR ARMA, SERÁ REMOVIDO DEPOIS
class InimigoDeTeste(pygame.sprite.Sprite):
    def __init__(self, posicao, grupos):
        super().__init__(grupos)
        self.image = pygame.Surface((40, 40)); self.image.fill('white')
        self.rect = self.image.get_rect(center=posicao)
        self.posicao = pygame.math.Vector2(self.rect.center)
    def update(self, delta_time):
        pass # Inimigo fica parado

class Game:
    def __init__(self, tela):
        self.tela = tela
        self.clock = pygame.time.Clock() 
        self.running = True

        self.player = Player(x=100, y=100, sheet_player=join('assets', 'img', 'player.png'))
        self.life_orb = Items(x=300, y=300, sheet_item=join('assets', 'img', 'lifeOrb.png'))
        self.expShard = Items(x=700, y=500, sheet_item=join('assets', 'img', 'expShard.png'))
        self.bigShard = Items(x=200, y=400, sheet_item=join('assets', 'img', 'bigShard.png'))


        self.all_sprites = pygame.sprite.Group() #grupo de sprites
        self.all_sprites.add(self.life_orb)
        self.all_sprites.add(self.expShard)
        self.all_sprites.add(self.bigShard)
        self.item_group = pygame.sprite.Group()#grupo de itens
        self.item_group.add(self.life_orb)
        self.item_group.add(self.expShard)
        self.item_group.add(self.bigShard)

        self.inimigos_grupo = pygame.sprite.Group()
        self.projeteis_grupo = pygame.sprite.Group()
        
        #CÓDIGO DE TESTE, DEVE SER REMOVIDO DEPOIS
        if not hasattr(self.player, 'armas'):
            self.player.armas = {}
        InimigoDeTeste(posicao=(1000, 360), grupos=(self.all_sprites, self.inimigos_grupo))
        InimigoDeTeste(posicao=(200, 200), grupos=(self.all_sprites, self.inimigos_grupo))

        for item in self.item_group.copy():
            if self.player.rect.colliderect(item.rect):
                self.item_group.remove(item)

        #CODIGO PARA TESTES, DEVE SER RETIRADO DEPOIS
        arma_Loop = Arma_Loop(
            jogador=self.player,
            cooldown=1500,
            grupo_projeteis=self.projeteis_grupo,
            grupo_inimigos=self.inimigos_grupo
        )
        self.player.armas['Laço'] = arma_Loop
        
        

    def run(self):
        while self.running:
            delta_time = self.clock.tick(fps) / 1000 #define o fps do jogo e retorna o delta time em milisegundo, por isso divide por 1k
            self.eventos() #avalia acoes do jogador (cima, baixo, saiu do jogo, etc...)
            self.update(delta_time) #movimentacao
            self.paint() #coloca cores na tela
    
    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False #sai do jogo
    
    
    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.player.update(keys, delta_time)
        self.inimigos_grupo.update(delta_time)
        self.projeteis_grupo.update(delta_time)
        self.all_sprites.update(delta_time)
        
        #CODIGO PARA TESTE, DEVE SER REMOVIDO DEPOIS
        for arma in self.player.armas.values():
            arma.update()

        for item in self.item_group.copy():
            if self.player.rect.colliderect(item.rect):
                self.item_group.remove(item)

    def paint(self):
        self.tela.fill(cores["preto"])
        self.item_group.draw(self.tela)
        self.inimigos_grupo.draw(self.tela)
        self.projeteis_grupo.draw(self.tela)
        self.tela.blit(self.player.image, self.player.rect)

        pygame.display.update() #pinta a tela
