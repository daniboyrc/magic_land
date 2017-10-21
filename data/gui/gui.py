# coding: utf-8

import pygame

TRANSPARENCY_COLOR = [0, 255, 228]


class GUI():
    def __init__(self, screen, clock, font, main_coordinate, main_size):
        self.screen = screen
        self.clock = clock
        self.font = font
        self.main_coordinate = main_coordinate
        self.main_surface = pygame.Surface(main_size)
        self.surfaces = {}
        self._transparency(self.main_surface)

    def _transparency(self, surf):
        surf.fill(TRANSPARENCY_COLOR)
        surf.set_colorkey(TRANSPARENCY_COLOR, pygame.RLEACCEL)

    def _generate_img_surface(self, img_path):
        img_surf = pygame.image.load(img_path)
        surface = pygame.Surface(img_surf.get_size())
        surface.set_colorkey([0, 255, 228], pygame.RLEACCEL)
        surface.blit(img_surf, (0, 0))

        return surface

    def draw_screen(self):
        self.screen.blit(self.main_surface, self.main_coordinate)

    def draw_main(self, surfaces):
        for name in surfaces:
            self.main_surface.blit(self.surfaces[name][0], self.surfaces[name][1])

    def draw_surface(self, name, surf, coordinate):
        self.surfaces[name][0].blit(surf, coordinate)

    def generate_surface(self, name, coordinate, size, img=[], coord_img=[]):
        self.surfaces[name] = [pygame.Surface(size), coordinate]
        self._transparency(self.surfaces[name][0])
        if img:
            for i in range(len(img)):
                self.surfaces[name][0].blit(
                    pygame.image.load(img[i]), coord_img[i])

    def load_image(self, name, img, coord_img):
        for i in range(len(img)):
            self.surfaces[name][0].blit(self._generate_img_surface(img[i]), coord_img[i])

    def text_menu_vert(self, name, text, coord_text):
        x, y = coord_text[0], coord_text[1]
        for i in text:
            frase = self.font.render(i, True, (0, 0, 0))
            self.surfaces[name][0].blit(frase, (x, y))
            y += self.font.size(i)[1] - 2

    def text_menu_horiz(self, name, text, coord_text):
        x, y = coord_text[0], coord_text[1]
        for i in text:
            frase = self.font.render(i, True, (0, 0, 0))
            self.surfaces[name][0].blit(frase, (x, y))
            x += self.font.size(i)[0]

    def select_menu_horiz(self, name, tabs, select, coordinate, space, back):
        x, y = coordinate
        self.load_image(name, [back], [(0, 0)])
        separator = ' ' * (space // 2) + '/' + ' ' * (space // 2)

        for i in range(len(tabs)):
            if i == select:
                self.font.set_italic(1)
                self.font.set_underline(1)

            text = self.font.render(tabs[i], True, (0, 0, 0))
            self.surfaces[name][0].blit(text, (x, y))
            self.font.set_italic(0)
            self.font.set_underline(0)
            x += self.font.size(tabs[i])[0]

            if i != len(tabs) - 1:
                text = self.font.render(separator, True, (0, 0, 0))
                self.surfaces[name][0].blit(text, (x, y))
                x += self.font.size(separator)[0]

    def select_menu_vert(self, name, select, back, cursor, coordinate, space):
        x, y = coordinate
        y = y + select * space
        self.image_load(name, [back, cursor], [(0, 0), (x, y)])
