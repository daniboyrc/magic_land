#!/usr/bin/env python
# coding: utf-8
# (c) 2017 Daniel Coura, UFCG

import pygame
from character import Character
from status import Status


class Player(Character):
    def __init__(self, name, sprite_file, coordinate):
        super(Player, self).__init__(name, sprite_file, coordinate)
        self.speed = 8
        self.move = [0, 0]
        self.rect = pygame.Rect(
            self.coordinate[0] + 9, self.coordinate[1] + 5, 16, 25)

        self.status = Status()
        self._quests = []
        self._inventory = []

    def new_quest(self, quest):
        self._quests.append(quest)

    def remove_quest(self, quest):
        self._quests.remove(quest)

    def new_item(self, item):
        self._inventory.append(item)

    def remove_item(self, item):
        self._inventory.remove(item)

    def get_quests(self):
        quests = []
        description = []
        stages = []

        for i in self.quest:
            quests.append(i.name)
            description.append(i.description)
            stg = []
            for j in range(len(i.stages)):
                if i.current_stage > j > 0:
                    stg.append(i.stages[j])
            stages.append(stg)

        return quests, description, stages

    def get_spell(self):
        id_spell = []
        spells = []
        descriptions = []
        for item in self.inventory:
            if str(item) == 'spell':
                id_spell.append(item.id)
                spells.append(item.name)
                descriptions.append(item.description)

        return id_spell, spells, descriptions

    def move(self, limits):
        left = self.coordinate[0] + self.move[0]
        right = self.coordinate[0] + self.move[0] + 32
        up = self.coordinate[1] + self.move[1]
        down = self.coordinate[1] + self.move[1] + 32

        if left > limits[3] and right < limits[1]:
            self.coordinate[0] += self.move[0]
        if up > limits[0] and down < limits[2]:
            self.coordinate[1] += self.move[1]

        self.rect = pygame.Rect(
            self.coordinate[0] + 9, self.coordinate[1] + 5, 16, 25)
        self.move = [0, 0]


if __name__ == "__main__":
    print("player module")
