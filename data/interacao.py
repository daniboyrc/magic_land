from gui import *


class Interacao():
    def __init__(self, screen, clock, fase):
        self.cenario = fase.cenario
        self.player = fase.player
        self.fase = fase
        self.gui_dialog = guiDialogo(screen, clock, fase)

    def verificaColisao(self):
        npc = self.Npc()
        door = self.Door()

        if npc or door:
            return True

    def Npc(self):
        for npc in self.fase.npc_atual:
            for colide in npc.area_interacao:
                colide = colide.move(self.cenario.pos[0], self.cenario.pos[1])
                if self.player.rect.colliderect(colide):
                    self.gui_dialog.controleDialogo(npc)
                    return True

    def Door(self):
        for door in self.fase.door_atual:
            collid = door.area_interacao.move(self.cenario.pos[0],
                                              self.cenario.pos[1])
            if self.player.rect.colliderect(collid):
                if door.aberta:
                    self.fase.setFase(door)
                    return True
                else:
                    print 'A porta esta trancada'
