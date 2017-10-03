from gui import *
import pygame
import sys
from .. import code_editor
from ..constantes import *
from ..control import *


IMG_BACK = ['resources/miscelania/guiquest_0.png',
            'resources/miscelania/guiquest_1.png',
            'resources/miscelania/guiquest_2.png',
            'resources/miscelania/guiquest_3.png']
IMG_CURSOR = 'resources/miscelania/cursor.png'


class guiQuest():
    def __init__(self, screen, clock, fase):
        self.screen = screen
        self.clock = clock
        self.font = Fontes.london
        self.cen = fase.cenario
        self.prot = fase.player
        self.loop = True
        self.img_back = IMG_BACK
        self.img_cursor = IMG_CURSOR

        self.gui = GUI(screen, self.font, clock, (0, 0), [230, 320])
        self.gui.addSurface('tabs', (0, 0), [230, 30])
        self.gui.addSurface('select', (0, 30), [30, 290])
        self.gui.addSurface('nome', (30, 30), [85, 290])
        self.gui.addSurface('descricao', (115, 30), [115, 290])

    def sair(self):
        self.loop = False

    def drawPanel(self):
        self.gui.setImage('tabs', [self.img_back[0]], [(0, 0)])
        self.gui.setImage('select', [self.img_back[1]], [(0, 0)])
        self.gui.setImage('nome', [self.img_back[2]], [(0, 0)])
        self.gui.setImage('descricao', [self.img_back[3]], [(0, 0)])

    def drawTabs(self, select):
        self.gui.setImage('tabs', [self.img_back[0]], [(0, 0)])
        self.gui.selectTabs('tabs', ['Quests', 'Feiticos'],
                            select, (27, 5), 5, self.img_back[0])

    def drawText(self, select, nome, descricao, etapas=''):
        if nome:
            self.gui.selectVert('select', select, self.img_back[1],
                                self.img_cursor, (3, 10), 20)
        self.gui.setImage('nome', [self.img_back[2]], [(0, 0)])
        self.gui.setTextMenu('nome', nome, (0, 10))
        self.gui.setImage('descricao', [self.img_back[3]], [(0, 0)])
        self.gui.setTextMenu('descricao', descricao, (0, 10))



    def main(self):
        self.loop = True
        self.drawPanel()
        tab = 0
        self.drawTabs(tab)
        select = 0
        quest, descricao_q, etapas = getQuest(self.prot)
        id_feitico, feitico, descricao_f = getFeitico(self.prot)

        while self.loop:
            self.gui.drawMain(['tabs', 'select', 'nome', 'descricao'])
            self.gui.drawScreen()
            if tab == 0:
                self.drawText(select, quest, descricao_q, etapas)
            else:
                self.drawText(select, feitico, descricao_f)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        tab = 0
                        select = 0
                        self.drawTabs(tab)
                    elif event.key == pygame.K_d:
                        tab = 1
                        select = 0
                        self.drawTabs(tab)
                    if event.key == pygame.K_w:
                        select -= 1
                        if select < 0:
                            select = 0
                    if event.key == pygame.K_s:
                        select += 1
                        if select > len(quest) - 1:
                            select = len(quest) - 1
                    elif event.key == pygame.K_q:
                        self.sair()
                    elif event.key == pygame.K_e:
                        self.sair()
                        return True
                    elif event.key == pygame.K_SPACE:
                        if tab == 1 and len(id_feitico) > 0:
                            code_editor.code_editor(self.screen, id_feitico[select])
                            self.sair()

            pygame.display.update()
            self.clock.tick(27)
