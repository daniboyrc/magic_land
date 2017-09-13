# coding: utf-8

import pygame
from data import *

pygame.init()
pygame.font.init()
dados_font = pygame.font.SysFont("sans", 16)
dialog_font = pygame.font.Font("resources/font/old_englished.ttf", 26)

screen = pygame.display.set_mode((Screen.width, Screen.height))
pygame.display.set_caption('Magic Land')
clock = pygame.time.Clock()

# Instanciando Player e Cenário
prot = Player('resources/personagens/prot.png', (70, 220))
cen = Cenario('resources/cenarios/mapa2.jpg')
cen.setPosicao((0, 0))
cen.setLimites()
cen.setCollision()

# Instanciando NPCs
mago = Npc(
    'resources/personagens/mago.png',
    'mago',
    [64, 256],)
cavaleiro = Npc(
    'resources/personagens/cavaleiro.png',
    'cavaleiro',
    [288, 96],)
porto = Npc(
    'resources/personagens/porto.png',
    'homem do porto',
    [380, 616],)
vendedor = Npc(
    'resources/personagens/vendedor.png',
    'vendedor',
    [736, 48],)

cen.npc_list = [mago, porto, vendedor]


# Instanciando Portas
d_cenario = Door([272, 416], 'up',
                 {'img': 'resources/cenarios/mapa2.jpg',
                     'pos': (0, 0),
                     'npc_list': [mago, porto, vendedor],
                     'door_list': [],
                  }, [400, 270])
d_player = Door([32, 144], 'down',
                {'img': 'resources/cenarios/house_player.jpg',
                    'pos': 'center',
                    'npc_list': [cavaleiro],
                    'door_list': [d_cenario],
                 }, [400, 300], False)
d_mago = Door([480, 144], 'down',
              {'img': 'resources/cenarios/house_player.jpg',
               'pos': 'center',
               'npc_list': [cavaleiro],
               'door_list': [d_cenario],
               }, [400, 300])
d_ferreiro = Door([304, 464], 'down',
                  {'img': 'resources/cenarios/house_player.jpg',
                   'pos': 'center',
                   'npc_list': [cavaleiro],
                   'door_list': [d_cenario],
                   }, [400, 300])
d_lord = Door([240, 240], 'down',
              {'img': 'resources/cenarios/house_player.jpg',
               'pos': 'center',
               'npc_list': [cavaleiro],
               'door_list': [d_cenario],
               }, [400, 300])
d_bibliotec = Door([704, 320], 'down',
                   {'img': 'resources/cenarios/house_player.jpg',
                    'pos': 'center',
                    'npc_list': [cavaleiro],
                    'door_list': [d_cenario],
                    }, [400, 300])
d_vendedor = Door([496, 400], 'down',
                  {'img': 'resources/cenarios/house_player.jpg',
                   'pos': 'center',
                   'npc_list': [cavaleiro],
                   'door_list': [d_cenario],
                   }, [400, 300])

d_cenario.cenario['door_list'] = [d_player, d_mago, d_lord, d_ferreiro,
                                  d_bibliotec, d_vendedor]

cen.door_list = d_cenario.cenario['door_list']

# Instanciando Quests
key_quest = Quest('A chave',
                  'Encontre a chave para abrir a porta',
                  ['falar com mago', 'falar com ferreiro', 'falar com mago'],
                  cavaleiro.area_interacao)
sword_quest = Quest('A espada',
                    'Encontre uma espada para enfrentar o inimigo',
                    ['falar com o vendedor', 'falar com mago'],
                    mago.area_interacao)

quest_list = [key_quest, sword_quest]
cen.quest_list = quest_list

# Dando quest aos npcs
cavaleiro.setQuest([key_quest], [['Ahoy, preciso da chave']])
mago.setQuest([sword_quest, key_quest], [['Ahoy, preciso do espadao',
                                          'Ahooy, precisa de dinheiro jovem',
                                          'Mas nao tenho dinheiro, bom senhor',
                                          'De-me um feitico entao'],
                                         ['Estou em busca de uma chave']])

move = 0
dialogo = ''
while True:
    drawnCenario(screen, cen, prot)

    # desenvolvedor
    dados(screen, dados_font, clock)
    visualizaColisao(screen, cen, prot)

    if dialogo:
        desenhaDialogo(screen, dialog_font, dialogo)

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
                dialogo = interageNpc(cen, prot)
                interageDoor(cen, prot)
                interageQuest(cen, prot)

            if event.key == pygame.K_q:
                print 'cenQuests: ', cen.quest_list
                print 'playerQuests: ', prot.quest

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
