from PIL import Image
import pygame
import os
from constantes import *


class Cenario():
    def __init__(self, img, pos):
        self.img = img
        self.pos = pos
        self.mov = [0, 0]

        self.size = pygame.image.load(self.img).get_size()
        self.limites = []
        self.collision = []

    def setSize(self):
        self.size = pygame.image.load(self.img).get_size()

    def setImg(self, img):
        self.img = img

    def setPosicao(self, local='', pos=(0, 0)):
        if local == 'up':
            self.pos[0] = Screen.width / 2 - self.size[0] / 2
            self.pos[1] = 0
        elif local == 'left':
            self.pos[0] = 0
            self.pos[1] = Screen.height / 2 - self.size[1] / 2
        elif local == 'center':
            self.pos[0] = Screen.width / 2 - self.size[0] / 2
            self.pos[1] = Screen.height / 2 - self.size[1] / 2
        elif local == 'right':
            self.pos[0] = Screen.width - self.size[0]
            self.pos[1] = Screen.height / 2 - self.size[1] / 2
        elif local == 'down':
            self.pos[0] = Screen.width / 2 - self.size[0] / 2
            self.pos[1] = Screen.height - self.size[1]
        else:
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]

    def setLimites(self):
        self.limites = []
        if self.pos[1] > 0:
            self.limites.append(self.pos[1])
        else:
            self.limites.append(0)
        if self.size[0] >= Screen.width:
            self.limites.append(Screen.width)
        else:
            self.limites.append(self.size[0] + self.pos[0])
        if self.size[1] >= Screen.height:
            self.limites.append(Screen.height)
        else:
            self.limites.append(self.size[1] + self.pos[1])
        if self.pos[0] > 0:
            self.limites.append(self.pos[0])
        else:
            self.limites.append(0)

    def setCollision(self):
        self.collision = []
        local = self.img.split()
        word = local[-1][0:-3] + 'txt'
        local.pop()
        local.append(word)
        local = '/'.join(local)
        arq = open(local, 'r')
        for i in arq:
            i = i.split()
            self.collision.append(pygame.Rect(int(i[0]), int(i[1]), 16, 16))
        arq.close()

    def moveCenario(self):
        self.pos[0] += self.mov[0]
        self.pos[1] += self.mov[1]

        self.mov[0] = 0
        self.mov[1] = 0
