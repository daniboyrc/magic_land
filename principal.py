# coding: utf-8

import pygame
from utils import *
from classes import *

pygame.init()
screen = pygame.display.set_mode((Tela.width, Tela.height))
pygame.display.set_caption('Magic Land')
clock = pygame.time.Clock()

prot = Player('fases/fase1/personagens/prot.png', (480, 450))
cen = Cenario('fases/fase1/cenarios/mapa2.jpg')
cen.setPosicao('down')
cen.setLimites()
collision = positionCollision('fases/fase1/cenarios/collision.txt')

# Instanciando Quests
key_quest = Quest('A chave',
                  'Encontre a chave para abrir a porta',
                  ['falar com mago', 'falar com ferreiro', 'falar com mago'],
                  1,)
sword_quest = Quest('A espada',
                    'Encontre uma espada para enfrentar o inimigo',
                    ['falar com o vendedor', 'falar com mago'],
                    1,)

# Instanciando Portas
door_player = Door('fases/fase1/cenarios/mapa.png', [304, 464])
door_2 = Door('fases/fase1/cenarios/mapa.png', [480, 144])
door_3 = Door('fases/fase1/cenarios/mapa.png', [32, 144])
door_4 = Door('fases/fase1/cenarios/mapa.png', [240, 240])
door_5 = Door('fases/fase1/cenarios/mapa.png', [704, 320])
door_6 = Door('fases/fase1/cenarios/mapa.png', [496, 400])

door_list = [door_player, door_2, door_3, door_4, door_5, door_6]

# Instanciando NPCs
mago = Npc(
    'fases/fase1/personagens/mago.png',
    'mago',
    [64, 256],)
cavaleiro = Npc(
    'fases/fase1/personagens/cavaleiro.png',
    'cavaleiro',
    [500, 222],)
porto = Npc(
    'fases/fase1/personagens/porto.png',
    'homem do porto',
    [380, 616],
    [key_quest],
    ['Estou em busca da chave'],)
vendedor = Npc(
    'fases/fase1/personagens/vendedor.png',
    'vendedor',
    [736, 48],
    [key_quest, sword_quest],
    ['Estou em busca da chave', 'Preciso de uma espada'],)

npc_list = [mago, cavaleiro, porto, vendedor]

# Dando quest ao protagonista
prot.newQuest(key_quest)
prot.newQuest(sword_quest)


move = 0
while True:
    movePlayer(screen, collision, npc_list, door_list, cen, prot)
    visualizaColisao(screen, collision, door_list, npc_list, cen, prot)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move = 1
                prot.direcao = 1
            if event.key == pygame.K_s:
                move = 2
                prot.direcao = 2
            if event.key == pygame.K_a:
                move = 3
                prot.direcao = 3
            if event.key == pygame.K_d:
                move = 4
                prot.direcao = 4
            if event.key == pygame.K_SPACE:
                acao(npc_list, door_list, cen, prot)
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

    movimentaPersonagem(move, cen, prot)

    pygame.display.flip()
    clock.tick(27)
