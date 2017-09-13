import pygame
from random import randint


class Npc(pygame.sprite.Sprite):
    def __init__(self, local, nome, coord):
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
        self.quest = []
        self.dialogo = []
        self.indice_dialogo = 0
        self.selected = None

    def speak(self, cen_quest, select=None):
        aux = True
        text = []
        self.selected = select
        if self.selected is None:
            for q in range(len(self.quest)):
                if self.quest[q] in cen_quest:
                    text.append(self.dialogo[q][0])
                    aux = False
        else:
            if self.indice_dialogo < len(self.dialogo[self.selected]):
                text.append(self.dialogo[self.selected][self.indice_dialogo])
                self.indice_dialogo += 1
                aux = False
            else:
                self.indice_dialogo = 0
                self.selected = None
                return ''
        if aux:
            text.append(self.frases[randint(0, 4)])
        return text

    def setQuest(self, quest, dialogo):
        self.quest = quest
        self.dialogo = dialogo

    def addQuest(self, quest, dialogo):
        self.quest.append(quest)
        self.dialogo.append(dialogo)

    def spriteSheet(self):
        sprite_sheet = pygame.image.load(self.local)
        image = pygame.Surface([32, 32])
        image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        image.blit(sprite_sheet, (0, self.sprite))

        return image
