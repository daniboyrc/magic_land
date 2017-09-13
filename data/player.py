import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, local, pos):
        pygame.sprite.Sprite.__init__(self)
        self.local = local
        self.speed = 8
        self.pos = [pos[0], pos[1]]
        self.mov = [0, 0]
        self.sprite = [0, 0]
        self.rect = pygame.Rect(self.pos[0] + 9, self.pos[1] + 5, 16, 25)
        self.quest = []

    def newQuest(self, quest):
        self.quest.append(quest)

    def spriteSheet(self):
        sprite_sheet = pygame.image.load(self.local)
        image = pygame.Surface([32, 32])
        image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        image.blit(sprite_sheet, (self.sprite[0], self.sprite[1]))
        return image

    def movePlayer(self, limites):
        left = self.pos[0] + self.mov[0]
        right = self.pos[0] + self.mov[0] + 32
        up = self.pos[1] + self.mov[1]
        down = self.pos[1] + self.mov[1] + 32

        if left > limites[3] and right < limites[1]:
            self.pos[0] += self.mov[0]
        if up > limites[0] and down < limites[2]:
            self.pos[1] += self.mov[1]

        self.rect = pygame.Rect(self.pos[0] + 9, self.pos[1] + 5, 16, 25)
        self.mov[0] = 0
        self.mov[1] = 0
