import pygame
from settings import largura_tela, altura_tela 
from game import Game


def main():
    pygame.init()
    tela = pygame.display.set_mode((largura_tela, altura_tela))  #dimensoes da tela de jogo
    pygame.display.set_caption("Teste") #nome do jogo que vai aparecer em cima da tela

    game = Game(tela) #chama a classe Game

    game.run() #roda o jogo

    pygame.quit() #sai do jogo

if __name__ == "__main__":
    main()