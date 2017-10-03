import pygame


class Personagem(object):
    def __init__(self, nome, local, coord):
        self.nome = nome
        self.local = local
        self.face = self.localFace(local)
        self.sprite = [0, 0]
        self.coord = coord

    def localFace(self, local):
        word = local.split('/')[-1][0:-4] + '_f.png'
        caminho = local.split('/')
        caminho.pop()
        caminho.append(word)
        return '/'.join(caminho)

    def spriteSheet(self):
        sprite_sheet = pygame.image.load(self.local)
        image = pygame.Surface([32, 32])
        image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        image.blit(sprite_sheet, (self.sprite[0], self.sprite[1]))

        return image
