# coding: utf-8

import pygame
from screen import Screen


def detectaColisao(before, cen, prot):
    p_antx, p_anty = before[0], before[1]
    c_antx, c_anty = before[2], before[3]

    for i in cen.collision:
        if prot.rect.colliderect(i.move(cen.pos[0], cen.pos[1])):
            prot.mov[0] = prot.mov[1] = cen.mov[0] = cen.mov[1] = 0
            prot.pos[0], prot.pos[1] = p_antx, p_anty
            cen.pos[0], cen.pos[1] = c_antx, c_anty

    for door in cen.door_list:
        if door.rect.move(cen.pos[0], cen.pos[1]).colliderect(prot.rect):
            prot.mov[0] = prot.mov[1] = cen.mov[0] = cen.mov[1] = 0
            prot.pos[0], prot.pos[1] = p_antx, p_anty
            cen.pos[0], cen.pos[1] = c_antx, c_anty

    for npc in cen.npc_list:
        colide = False
        for i in range(len(npc.area_interacao)):
            direction = npc.area_interacao[i].move(cen.pos[0], cen.pos[1])
            if prot.rect.colliderect(direction):
                if i == 0:
                    npc.sprite = -96
                elif i == 1:
                    npc.sprite = 0
                elif i == 2:
                    npc.sprite = -32
                elif i == 3:
                    npc.sprite = -64
                colide = True

        if not colide:
            npc.sprite = 0

        area_colisao = npc.rect.move(cen.pos[0], cen.pos[1])
        if prot.rect.colliderect(area_colisao):
            prot.mov[0] = prot.mov[1] = cen.mov[0] = cen.mov[1] = 0
            prot.pos[0], prot.pos[1] = p_antx, p_anty
            cen.pos[0], cen.pos[1] = c_antx, c_anty


def drawnCenario(screen, cen, prot):
    before = [prot.pos[0], prot.pos[1], cen.pos[0], cen.pos[1]]

    cen.moveCenario()
    prot.movePlayer(cen.limites)
    detectaColisao(before, cen, prot)

    screen.fill(0)
    screen.blit(pygame.image.load(cen.img).convert(), (cen.pos[0], cen.pos[1]))
    screen.blit(prot.spriteSheet(), (prot.pos[0], prot.pos[1]))
    for i in cen.npc_list:
        screen.blit(i.spriteSheet(), i.rect.move(cen.pos[0], cen.pos[1]))


def movimentaPersonagem(move, cen, prot):
    center_height = Screen.height / 2 - \
        prot.speed < prot.pos[1] < Screen.height / 2 + prot.speed
    center_width = Screen.height / 2 - \
        prot.speed < prot.pos[1] < Screen.height / 2 + prot.speed
    if move == 1:
        if center_height and cen.pos[1] + cen.mov[1] + prot.speed < 0:
            cen.mov[1] += prot.speed
        else:
            prot.mov[1] -= prot.speed

        prot.sprite[1] = -96
        prot.sprite[0] -= 32
        if prot.sprite[0] < -96:
            prot.sprite[0] = 0
    if move == 2:
        if center_height and Screen.height - cen.size[1] < cen.pos[1] + cen.mov[1] - prot.speed:
            cen.mov[1] -= prot.speed
        else:
            prot.mov[1] += prot.speed

        prot.sprite[1] = 0
        prot.sprite[0] -= 32
        if prot.sprite[0] < -96:
            prot.sprite[0] = 0
    if move == 3:
        if center_width and cen.pos[0] + cen.mov[0] + prot.speed < 0:
            cen.mov[0] += prot.speed
        else:
            prot.mov[0] -= prot.speed

        prot.sprite[1] = -32
        prot.sprite[0] -= 32
        if prot.sprite[0] < -96:
            prot.sprite[0] = 0
    if move == 4:
        if center_width and Screen.width - cen.size[0] < cen.pos[0] + cen.mov[0] - prot.speed:
            cen.mov[0] -= prot.speed
        else:
            prot.mov[0] += prot.speed

        prot.sprite[1] = -64
        prot.sprite[0] -= 32
        if prot.sprite[0] < -96:
            prot.sprite[0] = 0


def desenhaDialogo(screen, font, dialogo):
    screen.blit(pygame.image.load(
        'resources/miscelania/dialogo.jpg'), (0, 500))
    linha = 0
    for text in dialogo:
        text = font.render(text, True, (65, 45, 22))
        screen.blit(text, (130, 510 + linha))
        linha += 20


def interageNpc(cen, prot):
    for npc in cen.npc_list:
        for colide in npc.area_interacao:
            colide = colide.move(cen.pos[0], cen.pos[1])
            if prot.rect.colliderect(colide):
                return npc.speak(cen.quest_list)
    return ''


def interageDoor(cen, prot):
    for door in cen.door_list:
        collid = door.area_interacao.move(cen.pos[0], cen.pos[1])
        if prot.rect.colliderect(collid):
            if door.aberta:
                cen.setImg(door.cenario['img'])
                cen.setSize()
                cen.setPosicao(door.cenario['pos'])
                cen.setLimites()
                cen.setCollision()
                cen.npc_list = door.cenario['npc_list']
                cen.door_list = door.cenario['door_list']

                prot.pos = door.player
            else:
                print 'A porta esta trancada'


def interageQuest(cen, prot):
    for quest in cen.quest_list:
        for colide in quest.area_interacao:
            colide = colide.move(cen.pos[0], cen.pos[1])
            if prot.rect.colliderect(colide) and quest not in prot.quest:
                prot.newQuest(quest)


def visualizaColisao(screen, cen, prot):
    for i in cen.collision:
        pygame.draw.rect(screen, (0, 255, 0),
                         i.move(cen.pos[0], cen.pos[1]), 1)
    for door in cen.door_list:
        pygame.draw.rect(screen, (0, 0, 255),
                         door.rect.move(cen.pos[0], cen.pos[1]), 1)
        pygame.draw.rect(screen, (255, 255, 0), door.area_interacao.move(
            cen.pos[0], cen.pos[1]), 1)
    for npc in cen.npc_list:
        pygame.draw.rect(screen, (255, 0, 0), npc.rect.move(
            cen.pos[0], cen.pos[1]), 1)
        for i in npc.area_interacao:
            pygame.draw.rect(screen, (255, 255, 0), i.move(
                cen.pos[0], cen.pos[1]), 1)
    pygame.draw.rect(screen, (0), prot.rect, 1)


def dados(screen, font, clock):
    text = font.render('FPS: %.2f' % clock.get_fps(), True, (22, 255, 0))
    screen.blit(text, (0, 0))
