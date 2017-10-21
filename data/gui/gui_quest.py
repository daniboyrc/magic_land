import pygame
import os
import sys
from gui import *
from .. import code_editor
from ..constantes import *

IMG_BACK = [os.path.join(os.getcwd(), 'resources', 'miscelania', 'guiquest_0.png'),
            os.path.join(os.getcwd(), 'resources', 'miscelania', 'guiquest_1.png'),
            os.path.join(os.getcwd(), 'resources', 'miscelania', 'guiquest_2.png'),
            os.path.join(os.getcwd(), 'resources', 'miscelania', 'guiquest_3.png'),]

IMG_CURSOR = os.path.join(os.getcwd(), 'resources', 'miscelania', 'cursor.png')


class GUIQuest():
    def __init__(self, screen, clock, font, player):
        self.screen = screen
        self.clock = clock
        self.font = font
        self.player = player
        self._loop = True

        self.gui = GUI(screen, clock, self.font, (0, 0), [230, 320])
        self.gui.generate_surface('tabs', (0, 0), [230, 30])
        self.gui.generate_surface('select', (0, 30), [30, 290])
        self.gui.generate_surface('name', (30, 30), [85, 290])
        self.gui.generate_surface('description', (115, 30), [115, 290])

    def _exit(self):
        self._loop = False

    def _draw_panel(self):
        self.gui.load_image('tabs', [IMG_BACK[0]], [(0, 0)])
        self.gui.load_image('select', [IMG_BACK[1]], [(0, 0)])
        self.gui.load_image('name', [IMG_BACK[2]], [(0, 0)])
        self.gui.load_image('description', [IMG_BACK[3]], [(0, 0)])

    def _draw_tabs(self, select):
        self.gui.load_image('tabs', [IMG_BACK[0]], [(0, 0)])
        self.gui.select_menu_horiz('tabs', ['Quests', 'Feiticos'],
                                   select, (27, 5), 5, IMG_BACK[0])

    def _draw_text(self, name, description, select):
        if name:
            self.gui.select_menu_vert('select', select, IMG_BACK[1],
                                      IMG_CURSOR, (3, 10), 20)
        self.gui.load_image('name', [IMG_BACK[2]], [(0, 0)])
        self.gui.text_menu_vert('name', name, (0, 10))
        self.gui.load_image('description', [IMG_BACK[3]], [(0, 0)])
        self.gui.text_menu_vert('description', description, (0, 10))

    def main(self):
        self._loop = True
        self._draw_panel()
        tab = 0
        self._draw_tabs(tab)
        select = 0
        quest, description_quest, etapas = self.player.get_quest
        id_spell, spells, description_spell = self.player.get_spell

        while self._loop:
            self.gui.draw_main(['tabs', 'select', 'name', 'description'])
            self.gui.draw_screen()
            if tab:
                self._draw_text(quest, description_quest, select)
            else:
                self._draw_text(spells, description_spell, select)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys._exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        tab = 0
                        select = 0
                        self._draw_tabs(tab)
                    elif event.key == pygame.K_d:
                        tab = 1
                        select = 0
                        self._draw_tabs(tab)
                    if event.key == pygame.K_w:
                        select -= 1
                        if select < 0:
                            select = 0
                    if event.key == pygame.K_s:
                        select += 1
                        if select > len(quest) - 1:
                            select = len(quest) - 1
                    elif event.key == pygame.K_q:
                        self._exit()
                    elif event.key == pygame.K_SPACE:
                        if tab == 1 and len(id_spell) > 0:
                            code_editor.code_editor(
                                self.screen, id_spell[select])
                            self._exit()

            pygame.display.update()
            self.clock.tick(27)
