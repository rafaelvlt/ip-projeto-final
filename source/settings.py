import pygame
from os.path import join
from random import randint
from abc import ABC, abstractmethod



LARGURA_LOGICA = 1280
ALTURA_LOGICA = 720
largura_tela = LARGURA_LOGICA
altura_tela = ALTURA_LOGICA

LARGURA_MAPA = 15360 
ALTURA_MAPA = 10240 
TILE_LARGURA = 30
TILE_ALTURA = 20


fps = 60
cores = {
    "preto": (0,0,0),
    "branco": (255,255,255),
    "verde": (0,255,50)
}
