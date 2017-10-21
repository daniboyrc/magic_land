import pygame
from constantes import *


class Developer():
    def __init__(self, screen, clock, stage):
        self.screen = screen
        self.clock = clock
        self.scenario = stage.scenario
        self.player = stage.player
        self.stage = stage

    def view_collision(self):
        for i in self.scenario.collision:
            pygame.draw.rect(self.screen, (0, 255, 0),
                             i.move(self.scenario.pos[0],
                                    self.scenario.pos[1]), 1)
        for door in self.stage.door_atual:
            pygame.draw.rect(self.screen, (0, 0, 255),
                             door.rect.move(self.scenario.pos[0],
                                            self.scenario.pos[1]), 1)
            pygame.draw.rect(self.screen, (255, 255, 0),
                             door.area_interacao.move(self.scenario.pos[0],
                                                      self.scenario.pos[1]), 1)
        for npc in self.stage.npc_atual:
            pygame.draw.rect(self.screen, (255, 0, 0), npc.rect.move(
                self.scenario.pos[0], self.scenario.pos[1]), 1)
            for i in npc.area_interacao:
                pygame.draw.rect(self.screen, (255, 255, 0), i.move(
                    self.scenario.pos[0], self.scenario.pos[1]), 1)
        pygame.draw.rect(self.screen, (0), self.player.rect, 1)

    def data(self):
        text = Fontes.dados.render('FPS: %.2f' %
                                   self.clock.get_fps(), True, (22, 255, 0))
        self.screen.blit(text, (0, 0))
