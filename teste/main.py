import sys, pygame
pygame.init()

screen = pygame.display.set_mode([800, 600])

back = pygame.image.load("bg.jpg")
black = pygame.image.load("black.png")
surf = pygame.Surface([800, 600])
surf.set_alpha(100)

font = pygame.font.SysFont('OldLondon.ttf', 50)
text = font.render('Hello, World!', True, (255, 255, 0))
text.set_alpha(255)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.blit(back, (0, 0))
    screen.blit(surf, (0, 0))
    screen.blit(text, (0, 0))

    pygame.display.flip()