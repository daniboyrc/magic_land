# coding: utf-8

import pygame
from utils import *
from classes import *

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("sans", 16)
screen = pygame.display.set_mode((Tela.width, Tela.height))
pygame.display.set_caption('Magic Land')
clock = pygame.time.Clock()

# Instanciando Player e Cenário
prot = Player('fases/fase1/personagens/prot.png', (70, 220))
cen = Cenario('fases/fase1/cenarios/mapa2.jpg')
cen.setPosicao((0, 0))
cen.setLimites()
cen.setCollision()

# Instanciando Quests
key_quest = Quest('A chave',
                  'Encontre a chave para abrir a porta',
                  ['falar com mago', 'falar com ferreiro', 'falar com mago'],
                  1,)
sword_quest = Quest('A espada',
                    'Encontre uma espada para enfrentar o inimigo',
                    ['falar com o vendedor', 'falar com mago'],
                    1,)

# Instanciando NPCs
mago = Npc(
    'fases/fase1/personagens/mago.png',
    'mago',
    [64, 256],)
cavaleiro = Npc(
    'fases/fase1/personagens/cavaleiro.png',
    'cavaleiro',
    [288, 96],)
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

cen.npc_list = [mago, porto, vendedor]


# Instanciando Portas


d_cenario = Door([272, 416], 'up',
                 {'img': 'fases/fase1/cenarios/mapa2.jpg',
                     'pos': (0, 0),
                     'npc_list': [mago, porto, vendedor],
                     'door_list': [],
                  }, [400, 270])
d_player = Door([32, 144], 'down',
                {'img': 'fases/fase1/cenarios/house_player.jpg',
                    'pos': 'center',
                    'npc_list': [cavaleiro],
                    'door_list': [d_cenario],
                 }, [400, 300])
d_mago = Door([480, 144], 'down',
              {'img': 'fases/fase1/cenarios/house_player.jpg',
               'pos': 'center',
               'npc_list': [cavaleiro],
               'door_list': [d_cenario],
               }, [400, 300])
d_ferreiro = Door([304, 464], 'down',
                  {'img': 'fases/fase1/cenarios/house_player.jpg',
                   'pos': 'center',
                   'npc_list': [cavaleiro],
                   'door_list': [d_cenario],
                   }, [400, 300])
d_lord = Door([240, 240], 'down',
              {'img': 'fases/fase1/cenarios/house_player.jpg',
               'pos': 'center',
               'npc_list': [cavaleiro],
               'door_list': [d_cenario],
               }, [400, 300])
d_bibliotec = Door([704, 320], 'down',
                   {'img': 'fases/fase1/cenarios/house_player.jpg',
                    'pos': 'center',
                    'npc_list': [cavaleiro],
                    'door_list': [d_cenario],
                    }, [400, 300])
d_vendedor = Door([496, 400], 'down',
                  {'img': 'fases/fase1/cenarios/house_player.jpg',
                   'pos': 'center',
                   'npc_list': [cavaleiro],
                   'door_list': [d_cenario],
                   }, [400, 300])


d_cenario.cenario['door_list'] = [d_player, d_mago, d_lord, d_ferreiro,
                                  d_bibliotec, d_vendedor]

cen.door_list = d_cenario.cenario['door_list']

# Dando quest ao protagonista
prot.newQuest(key_quest)
prot.newQuest(sword_quest)


move = 0
while True:
    movePlayer(screen, cen, prot)
    dados(screen, font, clock)
    visualizaColisao(screen, cen, prot)
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
                interection(screen, cen, prot)
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

    pygame.display.update()
    clock.tick(30)
