#!/usr/bin/env python
# coding: utf-8
# (c) 2017 Daniel Coura, UFCG

import pygame
import os

PATH = os.path.join(os.getcwd(), 'resources', 'character')


class Character(object):
    def __init__(self, name, sprite_file, coordinate):
        self.name = name
        self.sprite_path = os.join(PATH, sprite_file)
        self.face_path = os.join(PATH, os.path.splitext(sprite_file)[0] + '_f.png')
        self.sprite = [0, 0]
        self.coordinate = coordinate

    def sprite_sheet(self):
        sprite_sheet = pygame.image.load(self.local)
        image = pygame.Surface([32, 32])
        image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        image.blit(sprite_sheet, (self.sprite[0], self.sprite[1]))

        return image


if __name__ == "__main__":
    print("characeter module is a superclass")
