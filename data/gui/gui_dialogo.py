import pygame
from gui import *
from ..constantes import *
import os

IMG_BACK = [os.path.join(os.getcwd(), 'resources', 'miscelania', 'dialogo_0.png'),
            os.path.join(os.getcwd(), 'resources', 'miscelania', 'dialogo_1.png'),
            os.path.join(os.getcwd(), 'resources', 'miscelania', 'dialogo_2.png'),
            os.path.join(os.getcwd(), 'resources', 'miscelania', 'dialogo_3.png'),]
IMG_ARROW = os.path.join(os.getcwd(), 'resources', 'miscelania', 'cursor.png')


class GUIDialogo():
    def __init__(self, screen, clock, font, player):
        self.screen = screen
        self.clock = clock
        self.player = player
        self.quest = fase.questDisponivel()
        self._loop = True

        self.gui = GUI(screen, self.font, clock, (0, 465), [800, 135])
        self.gui.generate_surface('name', (0, 0), [145, 30])
        self.gui.generate_surface('face', (0, 35), [100, 100])
        self.gui.generate_surface('select', (100, 35), [30, 100])
        self.gui.generate_surface('text', (130, 35), [670, 100])

        self.gui.load_image('select', [IMG_BACK[2]], [(0, 0)])

    def _exit(self, npc):
        npc.indice_dialogo = 1
        npc.selected = None
        self._loop = False

    def _draw_name(self, turn, npc):
        if turn == 0:
            text = self.player.name
        else:
            text = npc.name

        self.gui.load_image('name', [IMG_BACK[0]], [(0, 0)])
        self.gui.text_menu_vert('name', [text], (5, 5))

    def _draw_face(self, turn, npc):
        if turn == 0:
            face = self.player.face
        else:
            face = npc.face

        self.gui.load_image('face', [IMG_BACK[1], face], [(0, 0), (0, 0)])

    def _talk(self, npc, select):
        frase, quest, turn = npc.speak(
            self.quest, self.player, select)

        if turn == 3:
            self._exit(npc)
        if quest:
            frase.append('Exit')

        self.gui.load_image('text', [IMG_BACK[3]], [(0, 0)])
        self.gui.text_menu_vert('text', frase, (0, 10))
        self._draw_face(turn, npc)
        self._draw_name(turn, npc)
        return quest, len(frase) - 1

    def main(self, npc):
        self._loop = True
        select = 0
        var, maximo = self._talk(npc, select)

        while self._loop:
            self.gui.drawMain(['name', 'face', 'select', 'text'])
            self.gui.drawScreen()
            self.gui.select_menu_vert('select', select, IMG_BACK[2],
                                      IMG_ARROW, (5, 10), maximo, 20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        var, maximo = self._talk(npc, select)
                        if select is None:
                            self._exit(npc)
                    if event.key == pygame.K_w:
                        select -= 1
                        if select < 0:
                            select = 0
                    if event.key == pygame.K_s:
                        select += 1
                        if select > maximo - 1:
                            select = maximo - 1

            pygame.display.update()
            self.clock.tick(27)
