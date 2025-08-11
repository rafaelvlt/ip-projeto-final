import pygame

pygame.init()
pygame.mixer.init()

# Música
pygame.mixer.music.load("assets/msc/musica_menu.ogg")
pygame.mixer.music.play(-1) #repetir msc

# Loop do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False