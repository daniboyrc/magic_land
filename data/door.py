import pygame


class Door():
    def __init__(self, coord, direcao, cenario, player, aberta=True, size=32):
        self.coord = coord
        self.cenario = cenario
        self.player = player
        self.aberta = aberta
        self.size = size
        self.rect = pygame.Rect(self.coord[0], self.coord[1], self.size, 16)
        if direcao == 'down':
            self.area_interacao = pygame.Rect(
                self.coord[0], self.coord[1] + 16, self.size, 12)
        elif direcao == 'up':
            self.area_interacao = pygame.Rect(
                self.coord[0], self.coord[1] - 12, self.size, 12)

        def setCenario(self, cenario):
            self.cenario = cenario

        def setAberta(self):
            self.aberta = not self.aberta