import pygame
from constantes import *


class Desenvolvedor():
    def __init__(self, screen, clock, fase):
        self.screen = screen
        self.clock = clock
        self.cenario = fase.cenario
        self.player = fase.player
        self.fase = fase

    def visualizaColisao(self):
        for i in self.cenario.collision:
            pygame.draw.rect(self.screen, (0, 255, 0),
                             i.move(self.cenario.pos[0],
                                    self.cenario.pos[1]), 1)
        for door in self.fase.door_atual:
            pygame.draw.rect(self.screen, (0, 0, 255),
                             door.rect.move(self.cenario.pos[0],
                                            self.cenario.pos[1]), 1)
            pygame.draw.rect(self.screen, (255, 255, 0),
                             door.area_interacao.move(self.cenario.pos[0],
                                                      self.cenario.pos[1]), 1)
        for npc in self.fase.npc_atual:
            pygame.draw.rect(self.screen, (255, 0, 0), npc.rect.move(
                self.cenario.pos[0], self.cenario.pos[1]), 1)
            for i in npc.area_interacao:
                pygame.draw.rect(self.screen, (255, 255, 0), i.move(
                    self.cenario.pos[0], self.cenario.pos[1]), 1)
        pygame.draw.rect(self.screen, (0), self.player.rect, 1)

    def dados(self):
        text = Fontes.dados.render('FPS: %.2f' %
                                   self.clock.get_fps(), True, (22, 255, 0))
        self.screen.blit(text, (0, 0))

    def playerDados(self, fase):
        print 'quests: ',
        for i in fase.player.quest:
            print str(i) + '[' + str(i.etapa_atual) + '] - ' + i.etapas[i.etapa_atual] + ' | ',
        print ''
        print 'inventario: ',
        for i in fase.player.inventario:
            print i.nome, '| ',
        print ''