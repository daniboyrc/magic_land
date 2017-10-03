import pygame
from personagem import *
from level import *
from status import *

level = Level()
status = Status()


class Player(Personagem):
    def __init__(self, nome, local, coord):
        super(Player, self).__init__(nome, local, coord)
        self.speed = 8
        self.mov = [0, 0]
        self.rect = pygame.Rect(self.coord[0] + 9, self.coord[1] + 5, 16, 25)

        self.level = level
        self.status = status
        self.quest = []
        self.inventario = []

    def setNome(self, nome):
        self.nome = nome

    def newQuest(self, quest):
        self.quest.append(quest)

    def removeQuest(self, quest):
        self.quest.remove(quest)

    def newItem(self, item):
        self.inventario.append(item)

    def removeItem(self, item):
        self.inventario.remove(item)

    def movePlayer(self, limites):
        left = self.coord[0] + self.mov[0]
        right = self.coord[0] + self.mov[0] + 32
        up = self.coord[1] + self.mov[1]
        down = self.coord[1] + self.mov[1] + 32
        if left > limites[3] and right < limites[1]:
            self.coord[0] += self.mov[0]
        if up > limites[0] and down < limites[2]:
            self.coord[1] += self.mov[1]

        self.rect = pygame.Rect(self.coord[0] + 9, self.coord[1] + 5, 16, 25)
        self.mov[0] = 0
        self.mov[1] = 0
