#!/usr/bin/env python
# coding: utf-8
# (c) 2017 Daniel Coura, UFCG

from __future__ import print_function
import os
import pygame
from constantes import *

PATH = os.path.join(os.getcwd(), 'resources', 'scenario')


class Scenario(object):
    def __init__(self, image_file, coordinate):
        self.image_path = os.path.join(PATH, image_file)
        self.coordinate = coordinate
        self.move = [0, 0]
        self.size = pygame.image.load(img).get_size()
        self.limits = []
        self.collision = []

    def _set_size(self):
        self.size = pygame.image.load(self.image_path).get_size()

    def _set_limits(self):
        self.limits = []

        if self.coordinate[1] > 0:
            self.limits.append(self.coordinate[1])
        else:
            self.limits.append(0)

        if self.size[0] >= Screen.width:
            self.limits.append(Screen.width)
        else:
            self.limits.append(self.size[0] + self.coordinate[0])

        if self.size[1] >= Screen.height:
            self.limits.append(Screen.height)
        else:
            self.limits.append(self.size[1] + self.coordinate[1])

        if self.coordinate[0] > 0:
            self.limits.append(self.coordinate[0])
        else:
            self.limits.append(0)

    def _set_collision(self):
        self.collision = []
        path = os.path.join(os.path.split(self.image_path)[0],
                            os.path.splitext(self.image_path)[0] + '.txt')
        arq = open(path, 'r')
        for i in arq:
            i = i.split()
            self.collision.append(pygame.Rect(int(i[0]), int(i[1]), 16, 16))
        arq.close()

    def refresh(self, image_file, coordinate):
        self.image_path = os.path.join(PATH, image_file)
        self.coordinate = [coordinate[0], coordinate[1]]
        self._setSize()
        self._setLimits()
        self._setCollision()

    def move(self):
        self.position[0] += self.move[0]
        self.position[1] += self.move[1]
        self.move = [0, 0]


if __name__ == "__main__":
    print("scenario module")
