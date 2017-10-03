import pygame
from gui import *
from ..constantes import *

IMG_BACK = ['resources/miscelania/dialogo_0.png',
            'resources/miscelania/dialogo_1.jpg',
            'resources/miscelania/dialogo_2.jpg',
            'resources/miscelania/dialogo_3.jpg', ]
IMG_ARROW = 'resources/miscelania/cursor.png'


class guiDialogo():
    def __init__(self, screen, clock, fase):
        self.screen = screen
        self.clock = clock
        self.font = Fontes.london
        self.cen = fase.cenario
        self.player = fase.player
        self.npc = fase.npc_atual
        self.quest = fase.questDisponivel()
        self.loop = True

        self.img_back = IMG_BACK
        self.img_arrow = IMG_ARROW

        self.gui = GUI(screen, self.font, clock, (0, 465), [800, 135])
        self.gui.addSurface('name', (0, 0), [145, 30])
        self.gui.addSurface('face', (0, 35), [100, 100])
        self.gui.addSurface('select', (100, 35), [30, 100])
        self.gui.addSurface('text', (130, 35), [670, 100])

        self.gui.setImage('select', [self.img_back[2]], [(0, 0)])

    def iniciarDialogo(self):
        for npc in self.npc:
            for colide in npc.area_interacao:
                colide = colide.move(self.cen.pos[0], self.cen.pos[1])
                if self.player.rect.colliderect(colide):
                    self.controleDialogo(npc)

    def sair(self, npc):
        npc.indice_dialogo = 1
        npc.selected = None
        self.loop = False

    def drawName(self, vez, npc):
        if vez == 0:
            text = self.player.nome
        else:
            text = npc.nome

        self.gui.setImage('name', [self.img_back[0]], [(0, 0)])
        self.gui.setTextMenu('name', [text], (5, 5))

    def drawFace(self, vez, npc):
        if vez == 0:
            face = self.player.face
        else:
            face = npc.face

        self.gui.setImage('face', [self.img_back[1], face], [(0, 0), (0, 0)])

    def dialoga(self, npc, select):
        frase, quest, vez = npc.speak(
            self.quest, self.player, select)

        if vez == 3:
            self.sair(npc)
        if quest:
            frase.append('Exit')

        self.gui.setImage('text', [self.img_back[3]], [(0, 0)])
        self.gui.setTextMenu('text', frase, (0, 10))
        self.drawFace(vez, npc)
        self.drawName(vez, npc)
        return quest, len(frase) - 1

    def controleDialogo(self, npc):
        self.loop = True
        select = None
        var, maximo = self.dialoga(npc, select)
        self.gui.drawMain(['name', 'face', 'select', 'text'])
        self.gui.drawScreen()
        if var:
            select = self.gui.selectVertical('select', self.img_back[2],
                                             self.img_arrow, (5, 10), maximo, 20)
            if select == maximo:
                self.sair(npc)
            else:
                var, maximo = self.dialoga(npc, select)
        else:
            select = None

        while self.loop:
            self.gui.drawMain(['name', 'face', 'select', 'text'])
            self.gui.drawScreen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        var, maximo = self.dialoga(npc, select)
                        if select is None:
                            self.sair(npc)

            pygame.display.update()
            self.clock.tick(27)
