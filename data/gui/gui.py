# coding: utf-8

import pygame

TRANSPARENCIA = [0, 255, 228]


class GUI():
    def __init__(self, screen, font, clock, pos, size):
        self.screen = screen
        self.font = font
        self.clock = clock
        self.pos = pos
        self.surf_main = pygame.Surface(size)
        self.tranparencia(self.surf_main)
        self.surface = {}

    def tranparencia(self, surf):
        surf.fill(TRANSPARENCIA)
        surf.set_colorkey(TRANSPARENCIA, pygame.RLEACCEL)

    def drawScreen(self):
        self.screen.blit(self.surf_main, self.pos)

    def drawMain(self, surfaces):
        for surf in surfaces:
            self.surf_main.blit(self.surface[surf][0], self.surface[surf][1])

    def drawSurface(self, nome, surf, pos):
        self.surface[nome][0].blit(surf, pos)

    def addSurface(self, nome, pos, size, img=[], pos_img=(), text=[], pos_text=()):
        self.surface[nome] = [pygame.Surface(size), pos]
        self.tranparencia(self.surface[nome][0])
        if img:
            for i in range(len(img)):
                self.surface[nome][0].blit(
                    pygame.image.load(img[i]), pos_img[i])
        if text:
            x, y = pos_text[0], pos_text[1]
            for i in text:
                i = self.font.render(i, True, (0, 0, 0))
                self.surface[nome][0].blit(i, (x, y))
                y += 20

    def setImage(self, nome, img, pos_img):
        for i in range(len(img)):
            self.surface[nome][0].blit(self.geraSurface(img[i]), pos_img[i])

    def setTextMenu(self, nome, text, pos_text):
        x, y = pos_text[0], pos_text[1]
        for i in text:
            frase = self.font.render(i, True, (0, 0, 0))
            self.surface[nome][0].blit(frase, (x, y))
            y += self.font.size(i)[1] - 2

    def setTextMenu(self, nome, text, pos_text):
        x, y = pos_text[0], pos_text[1]
        for i in text:
            frase = self.font.render(i, True, (0, 0, 0))
            self.surface[nome][0].blit(frase, (x, y))
            y += self.font.size(i)[1] - 2

    def setMenuHoriz(self, nome, text, pos_text):
        x, y = pos_text[0], pos_text[1]
        for i in text:
            frase = self.font.render(i, True, (0, 0, 0))
            self.surface[nome][0].blit(frase, (x, y))
            x += self.font.size(i)[0]

    def geraSurface(self, img):
        img = pygame.image.load(img)
        surf = pygame.Surface(img.get_size())
        surf.set_colorkey([0, 255, 228], pygame.RLEACCEL)
        surf.blit(img, (0, 0))

        return surf

    def selectTabs(self, nome, tabs, select, pos, espaco, back):
        x, y = pos
        self.setImage(nome, [back], [(0, 0)])
        separador = ' ' * (espaco // 2) + '/' + ' ' * (espaco // 2)

        for i in range(len(tabs)):
            if i == select:
                self.font.set_italic(1)
                self.font.set_underline(1)

            text = self.font.render(tabs[i], True, (0, 0, 0))
            self.surface[nome][0].blit(text, (x, y))
            self.font.set_italic(0)
            self.font.set_underline(0)
            x += self.font.size(tabs[i])[0]

            if i != len(tabs) - 1:
                text = self.font.render(separador, True, (0, 0, 0))
                self.surface[nome][0].blit(text, (x, y))
                x += self.font.size(separador)[0]

    def selectVert(self, nome, select, back, img, pos, espaco):
        x, y = pos
        y = y + select * espaco
        self.setImage(nome, [back, img], [(0, 0), (x, y)])


    def selectVertical(self, nome, back, img, pos, maior, move):
        select = 0
        x, y = pos
        cursor = self.geraSurface(img)
        self.setImage(nome, [back, img], [(0, 0), (x, y)])
        while True:
            self.drawMain([nome])
            self.drawScreen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.setImage(nome, [back], [(0, 0)])
                        return select
                    if event.key == pygame.K_w:
                        y -= move
                        select -= 1
                        if y < pos[1]:
                            y = pos[1]
                            select = 0
                        self.setImage(nome, [back], [(0, 0)])
                        self.drawSurface(nome, cursor, (x, y))
                    if event.key == pygame.K_s:
                        y += move
                        select += 1
                        if y > pos[1] + maior * move:
                            y = pos[1] + maior * move
                            select = maior
                        self.setImage(nome, [back], [(0, 0)])
                        self.drawSurface(nome, cursor, (x, y))

            pygame.display.update()
            self.clock.tick(27)
