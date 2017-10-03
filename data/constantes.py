import pygame

pygame.init()
pygame.font.init()


class Fontes():
    london = pygame.font.Font(
        "resources/font/old_englished.ttf", 26)
    diploma = pygame.font.Font(
        "resources/font/diploma.ttf", 22)
    dados = pygame.font.SysFont(
        'Sans', 16)


class Screen():
    width = 800
    height = 600
