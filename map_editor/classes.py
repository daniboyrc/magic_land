# coding: utf-8

from PIL import Image
import pygame


class Tela:

    width = 800
    height = 600


class Cenario():

    def __init__(self, local, posicao=(0, 0)):
        self.local = pygame.image.load(local)
        self.rect = self.local.get_rect()
        self.pos = [posicao[0], posicao[1]]
        self.mov = [0, 0]

        img = Image.open(local)
        self.size = img.size

    def moveCenario(self):
        self.pos[0] += self.mov[0]

        self.pos[1] += self.mov[1]

        self.mov[0] = 0
        self.mov[1] = 0


class Cursor():    
    pos = [Tela.width / 2, Tela.height / 2]
    rect = pygame.Rect(pos[0], pos[1], 8, 8)
