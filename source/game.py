import pygame
from settings import *
from player import *
from items import *
from weapon import *
from os.path import join
from menu import *

#CÓDIGO PARA TESTAR ARMA, SERÁ REMOVIDO DEPOIS
class InimigoDeTeste(pygame.sprite.Sprite):
    def __init__(self, posicao, grupos):
        super().__init__(grupos)
        self.image = pygame.Surface((40, 40)); self.image.fill('white')
        self.rect = self.image.get_rect(center=posicao)
        self.posicao = pygame.math.Vector2(self.rect.center)

        self.vida = 5
        self.sendo_colidido = False
    def update(self, delta_time):
        pass # Inimigo fica parado

class Game:
    def __init__(self, tela):
        #configurações
        self.tela = tela
        self.clock = pygame.time.Clock() 
        self.running = True

        #máquina de estado
        self.estado_do_jogo = "menu_principal"
        self.menu_principal = MenuPrincipal(self)
        self.menu_pausa = MenuPausa(self)
        self.tela_game_over = TelaGameOver(self)

        #grupos de sprite
        self.all_sprites = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()
        self.inimigos_grupo = pygame.sprite.Group()
        self.projeteis_grupo = pygame.sprite.Group()

        #self.life_orb = Items(x=300, y=300, sheet_item=join('assets', 'img', 'lifeOrb.png'))
        #self.expShard = Items(x=700, y=500, sheet_item=join('assets', 'img', 'expShard.png'))
        #self.bigShard = Items(x=200, y=400, sheet_item=join('assets', 'img', 'bigShard.png'))

        #self.all_sprites.add(self.life_orb)
        #self.all_sprites.add(self.expShard)
        #self.all_sprites.add(self.bigShard)
        #self.item_group.add(self.life_orb)
        #self.item_group.add(self.expShard)
        #self.item_group.add(self.bigShard)


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
            
            #menus
            if self.estado_do_jogo == "menu_principal":
                escolha = self.menu_principal.handle_event(evento)
                if escolha == 'Start Game':
                    self.iniciar_novo_jogo()
                if escolha == 'Sair':
                    self.running = False
            elif self.estado_do_jogo == "jogando":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    self.estado_do_jogo = "pausa"

            elif self.estado_do_jogo == "pausa":
                escolha = self.menu_pausa.handle_event(evento)
                if escolha == "Continuar":
                    self.estado_do_jogo = "jogando"
                elif escolha == "Sair para Menu":
                    self.estado_do_jogo = "menu_principal"
            
            elif self.estado_do_jogo == "game_over":
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    self.estado_do_jogo = "menu_principal"


    def update(self, delta_time):
        if self.estado_do_jogo == "jogando":
            keys = pygame.key.get_pressed()
            self.player.update(keys, delta_time)
            self.inimigos_grupo.update(delta_time)
            self.projeteis_grupo.update(delta_time)

            #CODIGO PARA TESTE, DEVE SER REMOVIDO DEPOIS
            for arma in self.player.armas.values():
                arma.update()

            self.colisao()

            if self.player.vida <= 0:
                self.estado_do_jogo = 'game_over'

    def paint(self):
        if self.estado_do_jogo == "menu_principal":
            self.menu_principal.draw(self.tela)

        elif self.estado_do_jogo == 'jogando':
            self.tela.fill(cores["preto"])
            self.item_group.draw(self.tela)
            self.inimigos_grupo.draw(self.tela)
            self.projeteis_grupo.draw(self.tela)
            self.all_sprites.draw(self.tela)
        
        elif self.estado_do_jogo == 'pausa':
            self.tela.fill(cores["preto"])
            self.all_sprites.draw(self.tela)
            self.menu_pausa.draw(self.tela)

        elif self.estado_do_jogo == "game_over":
            self.tela_game_over.draw(self.tela)

        pygame.display.update() #pinta a tela
    
    def iniciar_novo_jogo(self):
        #limpa os grupos de sprites de um jogo anterior
        self.all_sprites.empty()
        self.item_group.empty()
        self.projeteis_grupo.empty()
        self.inimigos_grupo.empty()

        #instancia todos objetos iniciais para criálos no mapa
        self.player = Player(sheet_player=join('assets', 'img', 'player.png'), grupos=self.all_sprites)
        self.life_orb = Items(posicao=(300, 300), sheet_item=join('assets', 'img', 'lifeOrb.png'), grupos=(self.all_sprites, self.item_group))
        self.expShard = Items(posicao=(700, 500), sheet_item=join('assets', 'img', 'expShard.png'), grupos=(self.all_sprites, self.item_group))
        self.bigShard = Items(posicao=(200, 400), sheet_item=join('assets', 'img', 'bigShard.png'), grupos=(self.all_sprites, self.item_group))
                
        #CÓDIGO DE TESTE, DEVE SER REMOVIDO DEPOIS
        if not hasattr(self.player, 'armas'):
            self.player.armas = {}
        InimigoDeTeste(posicao=(1000, 360), grupos=(self.all_sprites, self.inimigos_grupo))
        InimigoDeTeste(posicao=(200, 200), grupos=(self.all_sprites, self.inimigos_grupo))

        #cria arma inicial e entrega ela ao jogador
        #CODIGO PARA TESTES, DEVE SER RETIRADO DEPOIS
        arma_Loop = Arma_Loop(
            jogador=self.player,
            cooldown=1500,
            grupo_projeteis=self.projeteis_grupo,
            grupo_inimigos=self.inimigos_grupo
        )
        self.player.armas['Laço'] = arma_Loop

        self.estado_do_jogo = 'jogando'

    def colisao(self):
        colisao_player_items = pygame.sprite.spritecollide(self.player, self.item_group, dokill=True)
        


        colisao_player_inimigos = pygame.sprite.spritecollide(self.player, self.inimigos_grupo, False)
        if colisao_player_inimigos != []:
            self.player.vida -= 1
        
        colisao_inimigo_projetil =  pygame.sprite.groupcollide(self.projeteis_grupo, self.inimigos_grupo, False, False)
        for projetil in self.projeteis_grupo:
            inimigos_em_contato_agora = colisao_inimigo_projetil.get(projetil, [])
            #converte para set
            set_inimigos_em_contato_agora = set(inimigos_em_contato_agora)
            #remove os inimigos que já foram acertados durante a colisão
            novos_acertos = set_inimigos_em_contato_agora - projetil.inimigos_atingidos

            for inimigo in novos_acertos:
                inimigo.vida -= projetil.dano
            
            #atualiza a memoria do projétil para quais inimigos estão em contato
            projetil.inimigos_atingidos = set_inimigos_em_contato_agora

        #morte dos inimigos caso vida zere
        for inimigo in self.inimigos_grupo:
            if inimigo.vida <= 0:
                inimigo.kill()
                    
