import pygame
from constantes import *


class Draw():
    def __init__(self, screen, fase):
        self.screen = screen
        self.cenario = fase.cenario
        self.player = fase.player
        self.fase = fase

    def move(self):
        before = [self.player.coord[0], self.player.coord[1],
                  self.cenario.pos[0], self.cenario.pos[1]]

        self.cenario.moveCenario()
        self.player.movePlayer(self.cenario.limites)
        self.detectaColisao(before)
        self.draw()

    def draw(self):
        self.screen.fill(0)
        self.screen.blit(pygame.image.load(self.cenario.img),
                         (self.cenario.pos[0], self.cenario.pos[1]))
        self.screen.blit(self.player.spriteSheet(),
                         (self.player.coord[0], self.player.coord[1]))
        for npc in self.fase.npc_atual:
            self.screen.blit(npc.spriteSheet(), npc.rect.move(
                self.cenario.pos[0], self.cenario.pos[1]))

    def detectaColisao(self, before):
        p_antx, p_anty = before[0], before[1]
        c_antx, c_anty = before[2], before[3]

        for cen in self.cenario.collision:
            if self.player.rect.colliderect(cen.move(self.cenario.pos[0],
                                                     self.cenario.pos[1])):
                self.player.mov = [0, 0]
                self.cenario.mov = [0, 0]
                self.player.coord = [p_antx, p_anty]
                self.cenario.pos = [c_antx, c_anty]

        for door in self.fase.door_atual:
            if door.rect.move(self.cenario.pos[0], self.cenario.pos[1]).colliderect(self.player.rect):
                self.player.mov = [0, 0]
                self.cenario.mov = [0, 0]
                self.player.coord[0], self.player.coord[1] = p_antx, p_anty
                self.cenario.pos[0], self.cenario.pos[1] = c_antx, c_anty

        for npc in self.fase.npc_atual:
            colide = False
            for i in range(len(npc.area_interacao)):
                direction = npc.area_interacao[i].move(self.cenario.pos[0],
                                                       self.cenario.pos[1])
                if self.player.rect.colliderect(direction):
                    if i == 0:
                        npc.sprite[1] = -96
                    elif i == 1:
                        npc.sprite[1] = 0
                    elif i == 2:
                        npc.sprite[1] = -32
                    elif i == 3:
                        npc.sprite[1] = -64
                    colide = True

            if not colide:
                npc.sprite[1] = 0

            area_colisao = npc.rect.move(self.cenario.pos[0],
                                         self.cenario.pos[1])
            if self.player.rect.colliderect(area_colisao):
                self.player.mov = [0, 0]
                self.cenario.mov = [0, 0]
                self.player.coord = [p_antx, p_anty]
                self.cenario.pos = [c_antx, c_anty]

    def movimentaPersonagem(self, move):
        speed = self.player.speed
        cen = self.cenario

        center_height = Screen.height / 2 - \
            speed < self.player.coord[1] < Screen.height / 2 + speed
        center_width = Screen.height / 2 - \
            speed < self.player.coord[1] < Screen.height / 2 + speed
        if move == 1:
            if center_height and cen.pos[1] + cen.mov[1] + speed < 0:
                cen.mov[1] += speed
            else:
                self.player.mov[1] -= speed

            self.player.sprite[1] = -96
            self.player.sprite[0] -= 32
            if self.player.sprite[0] < -64:
                self.player.sprite[0] = 0
        if move == 2:
            if center_height and Screen.height - cen.size[1] < cen.pos[1] + cen.mov[1] - speed:
                cen.mov[1] -= speed
            else:
                self.player.mov[1] += speed

            self.player.sprite[1] = 0
            self.player.sprite[0] -= 32
            if self.player.sprite[0] < -64:
                self.player.sprite[0] = 0
        if move == 3:
            if center_width and cen.pos[0] + cen.mov[0] + speed < 0:
                cen.mov[0] += speed
            else:
                self.player.mov[0] -= speed

            self.player.sprite[1] = -32
            self.player.sprite[0] -= 32
            if self.player.sprite[0] < -64:
                self.player.sprite[0] = 0
        if move == 4:
            if center_width and Screen.width - cen.size[0] < cen.pos[0] + cen.mov[0] - speed:
                cen.mov[0] -= speed
            else:
                self.player.mov[0] += speed

            self.player.sprite[1] = -64
            self.player.sprite[0] -= 32
            if self.player.sprite[0] < -64:
                self.player.sprite[0] = 0
        if move == 5:
            if center_width and cen.pos[0] + cen.mov[0] + speed < 0:
                cen.mov[0] += speed
            else:
                self.player.mov[0] -= speed
            if center_height and cen.pos[1] + cen.mov[1] + speed < 0:
                cen.mov[1] += speed
            else:
                self.player.mov[1] -= speed

            self.player.sprite[1] = -32
            self.player.sprite[0] -= 32
            if self.player.sprite[0] < -64:
                self.player.sprite[0] = 0
        if move == 6:
            if center_width and cen.pos[0] + cen.mov[0] + speed < 0:
                cen.mov[0] += speed
            else:
                self.player.mov[0] -= speed
            if center_height and Screen.height - cen.size[1] < cen.pos[1] + cen.mov[1] - speed:
                cen.mov[1] -= speed
            else:
                self.player.mov[1] += speed

            self.player.sprite[1] = -32
            self.player.sprite[0] -= 32
            if self.player.sprite[0] < -64:
                self.player.sprite[0] = 0
        if move == 7:
            if center_width and Screen.width - cen.size[0] < cen.pos[0] + cen.mov[0] - speed:
                cen.mov[0] -= speed
            else:
                self.player.mov[0] += speed
            if center_height and Screen.height - cen.size[1] < cen.pos[1] + cen.mov[1] - speed:
                cen.mov[1] -= speed
            else:
                self.player.mov[1] += speed

            self.player.sprite[1] = -64
            self.player.sprite[0] -= 32
            if self.player.sprite[0] < -64:
                self.player.sprite[0] = 0
        if move == 8:
            if center_width and Screen.width - cen.size[0] < cen.pos[0] + cen.mov[0] - speed:
                cen.mov[0] -= speed
            else:
                self.player.mov[0] += speed
            if center_height and cen.pos[1] + cen.mov[1] + speed < 0:
                cen.mov[1] += speed
            else:
                self.player.mov[1] -= speed

            self.player.sprite[1] = -64
            self.player.sprite[0] -= 32
            if self.player.sprite[0] < -64:
                self.player.sprite[0] = 0