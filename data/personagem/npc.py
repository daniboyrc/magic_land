import pygame
from random import randint
from personagem import *


class Npc(Personagem):
    def __init__(self, nome, local, coord):
        super(Npc, self).__init__(nome, local, coord)

        self.rect = pygame.Rect(self.coord[0], self.coord[1], 32, 32)
        self.area_interacao = [
            pygame.Rect(self.coord[0] + 8, self.coord[1] - 12, 16, 12),
            pygame.Rect(self.coord[0] + 8, self.coord[1] + 32, 16, 12),
            pygame.Rect(self.coord[0] - 12, self.coord[1] + 8, 12, 16),
            pygame.Rect(self.coord[0] + 32, self.coord[1] + 8, 12, 16),
        ]

        self.frases = []
        self.quest = None
        self.etapa = None
        self.indice_dialogo = 1

    def listaQuests(self, quests_disponiveis, player):
        frase_list = []
        for q in range(len(self.quest)):
            etapa = self.quest[q].etapa_atual
            if self.quest[q] in quests_disponiveis:
                if etapa == self.etapa[q]:
                    # if self.quest[q].itens_dar[etapa] in player.inventario:
                    frase_list.append(self.quest[q].dialogo[etapa][0].split('/')[1])

        return frase_list

    def concluiDialogo(self, select, player):
        self.quest[select].setEtapa(player)
        self.quest.pop(select)
        self.etapa.pop(select)
        self.indice_dialogo = 1

    def getFala(self, select):
        etapa = self.quest[select].etapa_atual
        frase = self.quest[select].dialogo[etapa][self.indice_dialogo].split(
            '/')
        frase_list = frase[1]
        vez = int(frase[0])
        self.indice_dialogo += 1

        return [frase_list], vez

    def speak(self, quests_disponiveis, player, select=None):
        frase_aleatoria = True
        frase_list = []
        quest = False
        vez = 0

        if select is None:
            frase_list = self.listaQuests(quests_disponiveis, player)
            quest = bool(frase_list)
            frase_aleatoria = bool(not frase_list)
        else:
            etapa = self.quest[select].etapa_atual
            if self.indice_dialogo < len(self.quest[select].dialogo[etapa]):
                frase_list, vez = self.getFala(select)
                frase_aleatoria = False
            else:
                self.concluiDialogo(select, player)
                return [], False, 3

        if frase_aleatoria:
            frase_list.append(self.frases[randint(0, len(self.frases) - 1)])
            vez = 1

        return frase_list, quest, vez

    def setQuest(self, quest, etapa):
        self.quest = quest
        self.etapa = etapa

    def setFrase(self, frases):
        self.frases = frases
