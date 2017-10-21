#!/usr/bin/env python
# coding: utf-8
# (c) 2017 Daniel Coura, UFCG

import pygame
import sys
from data import *
import cPickle
from os import environ

environ['SDL_VIDEO_CENTERED'] = '1'
pygame.mouse.set_visible(False)
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
gui_quest = guiQuest(screen, clock, Fonts.london, fase.player)

direct = []


def get_move():
    move = 0

    if 'w' in direct and len(direct) == 1:
        move = 1
    elif 's' in direct and len(direct) == 1:
        move = 2
    elif 'a' in direct and len(direct) == 1:
        move = 3
    elif 'd' in direct and len(direct) == 1:
        move = 4
    elif 'w' in direct and 'a' in direct and len(direct) == 2:
        move = 5
    elif 'a' in direct and 's' in direct and len(direct) == 2:
        move = 6
    elif 's' in direct and 'd' in direct and len(direct) == 2:
        move = 7
    elif 'd' in direct and 'w' in direct and len(direct) == 2:
        move = 8

    return move


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
                direct.append('w')
                fase.player.direcao = 1
            if event.key == pygame.K_s:
                direct.append('s')
                fase.player.direcao = 2
            if event.key == pygame.K_a:
                direct.append('a')
                fase.player.direcao = 3
            if event.key == pygame.K_d:
                direct.append('d')
                fase.player.direcao = 4
            if event.key == pygame.K_q:
                gui_quest.main()
                direct = []

            if event.key == pygame.K_SPACE:
                npc = Interaction.npc(fase.current_npc, fase.scenario.coordinate, fase.player.rect)
                door = Interaction.door(fase.current_door, fase.scenario.coordinate, fase.player.rect)
                if npc:
                    gui_dialog.controleDialogo(npc)
                elif door:
                    fase.setFase(door)
                else:
                    direct = []

            if event.key == pygame.K_F10:
                pygame.display.toggle_fullscreen()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                direct.remove('w')
            if event.key == pygame.K_s:
                direct.remove('s')
            if event.key == pygame.K_a:
                direct.remove('a')
            if event.key == pygame.K_d:
                direct.remove('d')

    draw.movimentaPersonagem(get_move())
    pygame.display.update()
    clock.tick(30)
