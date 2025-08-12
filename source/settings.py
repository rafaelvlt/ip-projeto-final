import pygame
from os.path import join
from random import randint
from abc import ABC, abstractmethod


largura_tela = 1280
altura_tela = 960

LARGURA_MAPA = 4992
ALTURA_MAPA = 4992
TILE_LARGURA = 16
TILE_ALTURA = 16

fps = 60
cores = {
    "preto": (0,0,0),
    "branco": (255,255,255),
    "verde": (0,255,50)
}