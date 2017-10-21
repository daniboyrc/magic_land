#!/usr/bin/env python
# coding: utf-8
# (c) 2017 Daniel Coura, UFCG

import pygame


class Door():
    def __init__(self, coordinate, direction, scenario, coord_player, door_open=True, size=32):
        self.coordinate = coordinate
        self.scenario = scenario
        self.coord_player = coord_player
        self.door_open = door_open
        self.size = size
        self.rect = pygame.Rect(
            self.coordinate[0], self.coordinate[1], self.size, 16)

        if direction == 'down':
            self.interaction_area = pygame.Rect(
                self.coordinate[0], self.coordinate[1] + 16, self.size, 12)
        elif direction == 'up':
            self.interaction_area = pygame.Rect(
                self.coordinate[0], self.coordinate[1] - 12, self.size, 12)


if __name__ == "__main__":
    print("door module")
