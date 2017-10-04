# coding: utf-8:

import pygame
from classes import *

CENARIO = '../resources/cenarios/cenario_1.png'
MAPA = 'mapa.txt'
SPEED = 60

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("sans", 16)
pygame.display.set_caption('Map Editor')
clock = pygame.time.Clock()

cen = Cenario(CENARIO, (0, 0))
screen = pygame.display.set_mode((Tela.width, Tela.height))


def getCor(tipo):
    cor = ''
    if tipo == 'collision':
        cor = (0, 255, 0)
    elif tipo == 'door':
        cor = (0, 0, 255)
    elif tipo == 'npc':
        cor = (255, 0, 0)
    return cor


def desenhaCenario():
    screen.fill(0)
    cen.moveCenario()
    screen.blit(pygame.image.load(CENARIO), (cen.pos[0], cen.pos[1]))
    for i in coordenadas:
        rect = pygame.Rect(i[0] * 16 + cen.mov[0], i[1]
                           * 16 + cen.mov[1], 16, 16)
        pygame.draw.rect(screen, getCor(
            i[2]), rect.move(cen.pos[0], cen.pos[1]))


def dados():
    text = font.render('FPS: %.2f' % clock.get_fps(), True, (22, 255, 0))
    screen.blit(text, (0, 0))


def movimentaPersonagem(move):
    if move == 1:
        cen.mov[1] += SPEED
    elif move == 2:
        cen.mov[1] -= SPEED
    elif move == 3:
        cen.mov[0] += SPEED
    elif move == 4:
        cen.mov[0] -= SPEED


tipo = 'collision'
move = 0
coordenadas = []

arq = open(MAPA, 'r')
for i in arq:
    i = i.split()
    print i
    coordenadas.append([int(i[0]) / 16, int(i[1]) / 16, i[2]])
arq.close()

pos = [0, 0]
while True:
    desenhaCenario()
    dados()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

            colisao = []
            personagem = []
            porta = []
            arq = open(MAPA, 'w')
            for i in coordenadas:
                if i[2] == 'collision':
                    colisao.append(i)
                if i[2] == 'door':
                    porta.append(i)
                if i[2] == 'npc':
                    personagem.append(i)

                arq.write(str(i[0] * 16) + ' ' +
                          str(i[1] * 16) + ' ' + i[2] + '\n')

            confirm = raw_input('Deseja salvar? ')

            if confirm == 's':
                collision = open('collision.txt', 'w')
                door = open('door.txt', 'w')
                npc = open('npc.txt', 'w')
                for i in colisao:
                    collision.write(str(i[0] * 16) + ' ' +
                                    str(i[1] * 16) + ' ' + i[2] + '\n')
                for i in porta:
                    door.write(str(i[0] * 16) + ' ' +
                               str(i[1] * 16) + ' ' + '\n')
                for i in personagem:
                    npc.write(str(i[0] * 16) + ' ' +
                              str(i[1] * 16) + ' ' + '\n')

                collision.close()
                door.close()
                npc.close()
                pygame.quit()
            if confirm == 'n':
                pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos[0], pos[1] = pygame.mouse.get_pos()
            pos[0] = (pos[0] - cen.pos[0]) / 16
            pos[1] = (pos[1] - cen.pos[1]) / 16

            var = True
            for i in ['collision', 'npc', 'door']:
                if [pos[0], pos[1], i] in coordenadas:
                    coordenadas.remove([pos[0], pos[1], i])
                    var = False
            if var:
                coordenadas.append([pos[0], pos[1], tipo])

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move = 1
            if event.key == pygame.K_s:
                move = 2
            if event.key == pygame.K_a:
                move = 3
            if event.key == pygame.K_d:
                move = 4
            if event.key == pygame.K_j:
                tipo = 'collision'
            if event.key == pygame.K_k:
                tipo = 'door'
            if event.key == pygame.K_l:
                tipo = 'npc'
            if event.key == pygame.K_SPACE:
                print move

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w and move == 1:
                move = 0
            if event.key == pygame.K_s and move == 2:
                move = 0
            if event.key == pygame.K_a and move == 3:
                move = 0
            if event.key == pygame.K_d and move == 4:
                move = 0

    movimentaPersonagem(move)

    pygame.display.flip()
    clock.tick(27)
