# coding: utf-8

from PIL import Image
import pygame
from random import randint


class Tela:
    width = 800
    height = 600


class Cenario():
    def __init__(self, img, posicao=(0, 0)):
        self.img = img
        self.pos = [posicao[0], posicao[1]]
        self.mov = [0, 0]

        img = Image.open(img)
        self.size = img.size
        self.limites = []

    def setSize(self):
        self.img = Image.open(self.img)
        self.size = self.img.size

    def setImg(self, img):
        self.img = img

    def setPosicao(self, local='', pos=(0, 0)):
        if local == 'up':
            self.pos[0] = Tela.width / 2 - self.size[0] / 2
            self.pos[1] = 0
        elif local == 'left':
            self.pos[0] = 0
            self.pos[1] = Tela.height / 2 - self.size[1] / 2
        elif local == 'center':
            self.pos[0] = Tela.width / 2 - self.size[0] / 2
            self.pos[1] = Tela.height / 2 - self.size[1] / 2
        elif local == 'right':
            self.pos[0] = Tela.width - self.size[0]
            self.pos[1] = Tela.height / 2 - self.size[1] / 2
        elif local == 'down':
            self.pos[0] = Tela.width / 2 - self.size[0] / 2
            self.pos[1] = Tela.height - self.size[1]
        else:
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]

    def setLimites(self):
        if self.pos[1] > 0:
            self.limites.append(self.pos[1])
        else:
            self.limites.append(0)
        if self.size[0] >= Tela.width:
            self.limites.append(Tela.width)
        else:
            self.limites.append(self.size[0] + self.pos[0])
        if self.size[1] >= Tela.height:
            self.limites.append(Tela.height)
        else:
            self.limites.append(self.size[1] + self.pos[1])
        if self.pos[0] > 0:
            self.limites.append(self.pos[0])
        else:
            self.limites.append(0)

    def moveCenario(self):
        if self.size[0] > Tela.width:
            if Tela.width - self.size[0] < self.pos[0] + self.mov[0] < 0:
                self.pos[0] += self.mov[0]

        if self.size[1] > Tela.height:
            if Tela.height - self.size[1] < self.pos[1] + self.mov[1] < 0:
                self.pos[1] += self.mov[1]

        self.mov[0] = 0
        self.mov[1] = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, local, pos):
        pygame.sprite.Sprite.__init__(self)
        self.local = local
        self.speed = 8
        self.pos = [pos[0], pos[1]]
        self.mov = [0, 0]
        self.sprite = [0, 0]
        self.rect = pygame.Rect(self.pos[0] + 9, self.pos[1] + 5, 16, 25)
        self.quest = []

    def newQuest(self, quest):
        self.quest.append(quest)

    def spriteSheet(self):
        sprite_sheet = pygame.image.load(self.local)
        image = pygame.Surface([32, 32])
        image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        image.blit(sprite_sheet, (self.sprite[0], self.sprite[1]))
        return image

    def movePlayer(self, limites):
        left = self.pos[0] + self.mov[0]
        right = self.pos[0] + self.mov[0] + 32
        up = self.pos[1] + self.mov[1]
        down = self.pos[1] + self.mov[1] + 32

        if left > limites[3] and right < limites[1]:
            self.pos[0] += self.mov[0]
        if up > limites[0] and down < limites[2]:
            self.pos[1] += self.mov[1]

        self.rect = pygame.Rect(self.pos[0] + 9, self.pos[1] + 5, 16, 25)
        self.mov[0] = 0
        self.mov[1] = 0


class Npc(pygame.sprite.Sprite):
    def __init__(self, local, nome, coord, quest=[], dialogo=[]):
        pygame.sprite.Sprite.__init__(self)
        self.local = local
        self.nome = nome
        self.coord = coord
        self.sprite = 0
        self.rect = pygame.Rect(self.coord[0], self.coord[1], 32, 32)
        self.area_interacao = [
            pygame.Rect(self.coord[0] + 8, self.coord[1] - 12, 16, 12),
            pygame.Rect(self.coord[0] + 8, self.coord[1] + 32, 16, 12),
            pygame.Rect(self.coord[0] - 12, self.coord[1] + 8, 12, 16),
            pygame.Rect(self.coord[0] + 32, self.coord[1] + 8, 12, 16),
        ]
        self.frases = ['bla bla bla',
                       'ble ble ble',
                       'bli bli bli',
                       'blo blo blo',
                       'blu blu blu',
                       ]
        self.quest = quest
        self.dialogo = dialogo

    def speak(self, p_quest):
        aux = True
        for q in range(len(self.quest)):
            if self.quest[q] in p_quest:
                print self.dialogo[q]
                aux = False
        if aux:
            print self.frases[randint(0, 4)]

    def setQuest(self, quest):
        self.quest.append(quest)

    def setDialogo(self, dialogo):
        self.dialogo.append(dialogo)

    def spriteSheet(self):
        sprite_sheet = pygame.image.load(self.local)
        image = pygame.Surface([32, 32])
        image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        image.blit(sprite_sheet, (0, self.sprite))

        return image


class Door():
    def __init__(self, cenario, coord, size=32):
        self.cenario = cenario
        self.coord = coord
        self.size = size
        self.rect = pygame.Rect(self.coord[0], self.coord[1], self.size, 16)
        self.area_interacao = pygame.Rect(
            self.coord[0], self.coord[1] + 16, self.size, 12)


class Quest():
    def __init__(self, nome, descricao, etapas, tipo):
        self.nome = nome
        self.descricao = descricao
        self.etapas = etapas
        self.tipo = tipo
        self.etapa_atual = 0
        self.concluida = False
