# coding: utf-8

import pygame
import sys
from data import *
import cPickle


pygame.init()
pygame.font.init()
pygame.display.set_caption('Magic Land')

# Screen e clock
screen = pygame.display.set_mode((Screen.width, Screen.height))
clock = pygame.time.Clock()

# Fase e movimento
fase = '1'
fase = cPickle.load(file('resources/fases/cPickle' + fase + '.dat'))
draw = Draw(screen, fase)

# Desenvolvedor
desenvolvedor = Desenvolvedor(screen, clock, fase)

# Interacao com NPC e portas
interacao = Interacao(screen, clock, fase)

# GUI quests
gui_quest = guiQuest(screen, clock, fase)

move = 0
while True:
    draw.move()

    # desenvolvedor
    # desenvolvedor.visualizaColisao()
    desenvolvedor.dados()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move = 1
                fase.player.direcao = 1
            if event.key == pygame.K_s:
                move = 2
                fase.player.direcao = 2
            if event.key == pygame.K_a:
                move = 3
                fase.player.direcao = 3
            if event.key == pygame.K_d:
                move = 4
                fase.player.direcao = 4
            if event.key == pygame.K_q:
                gui_quest.main()
                move = 0

            if event.key == pygame.K_SPACE:
                if interacao.verificaColisao():
                    move = 0

            if event.key == pygame.K_F10:
                pygame.display.toggle_fullscreen()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w and move == 1:
                move = 0
            if event.key == pygame.K_s and move == 2:
                move = 0
            if event.key == pygame.K_a and move == 3:
                move = 0
            if event.key == pygame.K_d and move == 4:
                move = 0

    draw.movimentaPersonagem(move)

    pygame.display.update()
    clock.tick(30)
