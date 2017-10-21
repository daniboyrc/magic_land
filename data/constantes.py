#!/usr/bin/env python
# coding: utf-8
# (c) 2017 Daniel Coura, UFCG

import pygame

pygame.init()
pygame.font.init()


class Fonts():
    london = pygame.font.Font(
        "resources/font/old_englished.ttf", 26)
    diploma = pygame.font.Font(
        "resources/font/diploma.ttf", 22)
    dados = pygame.font.SysFont(
        'Sans', 16)


class Screen():
    width = 800
    height = 600


if __name__ == "__main__":
    print("constants module")
