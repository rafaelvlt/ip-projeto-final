import sys
import os

if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
    sys.path.append(os.path.join(base_path, 'source'))
else:

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))


import pygame
from settings import *
from game import Game

def main():
    pygame.init()
    pygame.mixer.init()


    game = Game()
    game.run()
    
    pygame.quit()

if __name__ == "__main__":
    main()
