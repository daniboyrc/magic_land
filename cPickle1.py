# coding: utf-8

from data import *
import cPickle

PLAYER = 'resources/personagens/prot.png'
CENARIO = 'resources/cenarios/cenario_1.png'

# Player e Cenário
player = Player('sir. Daniel', PLAYER, [70, 220])
cenario = Cenario(CENARIO, [0, 0])
cenario.setLimites()
cenario.setCollision()

# Instanciando NPCs
mago = Npc(
    'Mago',
    'resources/personagens/mago.png',
    [64, 256],)
cavaleiro = Npc(
    'Cavaleiro',
    'resources/personagens/cavaleiro.png',
    [288, 96],)
porto = Npc(
    'Homem do porto',
    'resources/personagens/porto.png',
    [380, 616],)
vendedor = Npc(
    'vendedor',
    'resources/personagens/vendedor.png',
    [736, 48],)


# Instanciando portas
d_cenario = Door([272, 416], 'up',
                 {'img': 'resources/cenarios/cenario_1.png',
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

# Instanciando Itens
feitico = controllFeitico(player)
mago_feitico = feitico.addFeitico()
carta = itemQuest('Carta do mago', '../local')
manual = itemQuest('Manual da chave', '../local')
chave = itemQuest('Chave da porta', '../local')

# Instanciando Quests


key_quest = Quest('A chave',
                  'Encontre a chave para abrir a porta',
                  ['Falar com o mago',
                   'Buscar o manual',
                   'Falar com o mago',
                   'Forjar chave'],
                  [mago_feitico, manual, None, chave],
                  [None, mago_feitico, None, manual],
                  True)

key_quest.setDialogo([['0/Estou em busca de uma chave',
                       '1/Va ao bibliotecario e entregue essa carta',
                       '0/Farei isso'],
                      ['0/O mago mandou entregar essa carta',
                       '0/Preciso de uma manual de uma chave',
                       '1/Tenho o que procura, vou ver se encontro',
                       '1/Aqui está'],
                      ['0/Consegui o manual',
                       '1/Muito bem, agora va ao ferreiro',
                       '1/Peca para forjar sua chave'],
                      ['0/Pode forjar um ngc pra mim?',
                       '1/Posso sim',
                       '0/Aqui esta como deve fazer']])

# Fechando conexão
feitico.conn.close()

# Dando quest aos npcs
cavaleiro.setQuest([key_quest],
                   [3],)
mago.setQuest([key_quest, key_quest],
              [0, 2],)
vendedor.setQuest([key_quest],
                  [1],)

# Diálogo aleatório dos NPCs
npc = [mago, cavaleiro, porto, vendedor]
frases = ['Hello my friend', 'Quer pipoca, jubileu?', 'Imposto eh roubo!']
for i in npc:
    i.setFrase(frases)


npc_atual = [mago, vendedor]
door = [d_cenario, d_player, d_mago, d_ferreiro,
        d_lord, d_bibliotec, d_vendedor]
door_atual = [d_player, d_mago, d_lord, d_ferreiro,
              d_bibliotec, d_vendedor]
quests = [key_quest]

fase1 = Fase(
    player,
    cenario,
    npc,
    npc_atual,
    door,
    door_atual,
    quests,
)

cPickle.dump(fase1, file("resources/fases/cPickle1.dat", "w"))
