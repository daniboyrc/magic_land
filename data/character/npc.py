#!/usr/bin/env python
# coding: utf-8
# (c) 2017 Daniel Coura, UFCG

import pygame
from random import randint
from character import Character


class NPC(Character):
    def __init__(self, name, sprite_file, coordinate):
        super(NPC, self).__init__(name, sprite_file, coordinate)

        self.rect = pygame.Rect(self.coord[0], self.coord[1], 32, 32)
        self.interaction_area = [
            pygame.Rect(self.coordinate[0] + 8, self.coordinate[1] - 12, 16, 12),
            pygame.Rect(self.coordinate[0] + 8, self.coordinate[1] + 32, 16, 12),
            pygame.Rect(self.coordinate[0] - 12, self.coordinate[1] + 8, 12, 16),
            pygame.Rect(self.coordinate[0] + 32, self.coordinate[1] + 8, 12, 16),
        ]

        self.phrases = []
        self.quests = []
        self.steps = []
        self._dialogue_index = 1

    def _finish_dialogue(self, select, player):
        self.quests[select].set_step(player)
        self.quests.pop(select)
        self.etapa.pop(select)
        self._dialogue_index = 1

    def _get_speak(self, select):
        step = self.quests[select].current_step
        phrase = self.quests[select].dialogo[step][self._dialogue_index].split('/')
        phrase_list = phrase[1]
        turn = int(phrase[0])
        self._dialogue_index += 1

        return [phrase_list], turn

    def list_quests(self, quests_avaible, player):
        phrase_list = []
        for q in range(len(self.quests)):
            step = self.quests[q].current_step
            if self.quests[q] in quests_avaible and step == self.steps[q]:
                phrase_list.append(self.quests[q].dialogue[step][0].split('/')[1])

        return phrase_list

    def speak(self, quests_avaible, player, select=None):
        random_phrase = True
        phrase_list = []
        have_quest = False
        turn = 0

        if select is None:
            phrase_list = self.listQuests(quests_avaible, player)
            have_quest = bool(phrase_list)
            random_phrase = bool(not phrase_list)
        else:
            step = self.quests[select].current_step
            if self._dialogue_index < len(self.quests[select].dialogo[step]):
                phrase_list, turn = self._get_speak(select)
                random_phrase = False
            else:
                self._finish_dialogue(select, player)
                return [], False, 3

        if random_phrase:
            phrase_list.append(self.frases[randint(0, len(self.frases) - 1)])
            turn = 1

        return phrase_list, have_quest, turn


if __name__ == "__main__":
    print("npc module")
