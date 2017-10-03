
class Fase():
    def __init__(self, player, cenario, npc, npc_atual,
                 door, door_atual, quests):

        self.player = player
        self.cenario = cenario

        self.npc = npc
        self.npc_atual = npc_atual

        self.door = door
        self.door_atual = door_atual

        self.quests = quests

    def setFase(self, door):
        self.cenario.setImg(door.cenario['img'])
        self.cenario.setSize()
        self.cenario.setPosicao(door.cenario['pos'])
        self.cenario.setLimites()
        self.cenario.setCollision()
        self.npc_atual = door.cenario['npc_list']
        self.door_atual = door.cenario['door_list']
        self.player.coord = door.player

    def questDisponivel(self):
        quests_disponiveis = []
        for q in self.quests:
            if q.disponivel:
                quests_disponiveis.append(q)

        return quests_disponiveis
