# coding: utf-8:

import pygame
from classes import *

pygame.init()

pygame.display.set_caption('RPG game')
clock = pygame.time.Clock()

prot = Protagonista('../fases/fase1/personagens/prot.png', (70, 200))
cen = Cenario('../fases/fase1/cenarios/mapa2.jpg', prot, (10, 10))
cen.setPosicao((0, 0))

screen = pygame.display.set_mode((cen.size[0], cen.size[1]))


def getCor(tipo):
    if tipo == 'c':
        cor = (0, 255, 0)
    elif tipo == 'e':
        cor = (0, 0, 255)
    elif tipo == 'f':
        cor = (255, 0, 0)
    return cor


def desenhaCenario():
    cen.moveCenario()
    prot.moveProtagonista(cen.limites)
    screen.blit(pygame.image.load(cen.local), (cen.pos[0], cen.pos[1]))
    screen.blit(prot.spriteSheet(), (prot.pos[0], prot.pos[1]))
    for i in coordenadas:
        rect = pygame.Rect(i[0] * 16 + cen.mov[0], i[1]
                           * 16 + cen.mov[1], 16, 16)
        pygame.draw.rect(screen, getCor(
            i[2]), rect.move(cen.pos[0], cen.pos[1]))


def movimentaPersonagem(move):
    if move == 1:
        cen.mov[1] += prot.velocidade
        prot.mov[1] -= prot.velocidade

        prot.sprite[1] = -96
        prot.sprite[0] -= 32
        if prot.sprite[0] < -96:
            prot.sprite[0] = 0
    elif move == 2:
        cen.mov[1] -= prot.velocidade
        prot.mov[1] += prot.velocidade

        prot.sprite[1] = 0
        prot.sprite[0] -= 32
        if prot.sprite[0] < -96:
            prot.sprite[0] = 0
    elif move == 3:
        cen.mov[0] += prot.velocidade
        prot.mov[0] -= prot.velocidade

        prot.sprite[1] = -32
        prot.sprite[0] -= 32
        if prot.sprite[0] < -96:
            prot.sprite[0] = 0
    elif move == 4:
        cen.mov[0] -= prot.velocidade
        prot.mov[0] += prot.velocidade

        prot.sprite[1] = -64
        prot.sprite[0] -= 32
        if prot.sprite[0] < -96:
            prot.sprite[0] = 0


tipo = 'c'
move = 0
coordenadas = []

arq = open('mapa2.txt', 'r')
for i in arq:
    i = i.split()
    coordenadas.append([int(i[0]) / 16, int(i[1]) / 16, i[2]])
arq.close()

pos = [0, 0]
while True:
    desenhaCenario()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            colisao = []
            personagem = []
            porta = []
            arq = open('mapa.txt', 'w')
            for i in coordenadas:
                if i[2] == 'c':
                    colisao.append(i)
                if i[2] == 'e':
                    porta.append(i)
                if i[2] == 'f':
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
            for i in 'cef':
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
                tipo = 'c'  # colidir
            if event.key == pygame.K_k:
                tipo = 'e'  # entrar
            if event.key == pygame.K_l:
                tipo = 'f'  # falar
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

    movimentaPersonagem(move)

    pygame.display.flip()
    clock.tick(27)
