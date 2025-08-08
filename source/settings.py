import pygame
from os.path import join
from random import randint
from abc import ABC, abstractmethod


largura_tela = 1200
altura_tela = 720

LARGURA_MAPA = 5000
ALTURA_MAPA = 5000

fps = 60
cores = {
    "preto": (0,0,0),
    "branco": (255,255,255),
    "verde": (0,255,50)
}



