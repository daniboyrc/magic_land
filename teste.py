# coding: utf-8

import pygame
from var_global import *
from utils import *

pygame.init()

screen = pygame.display.set_mode((Tela.width, Tela.height))
pygame.display.set_caption('RPG game')
clock = pygame.time.Clock()
		
prot = Protagonista('img/personagens/principal/person.png', (70, 200))
cen = Cenario('img/cenarios/fase1/mapa.png', prot, (10, 10))
cen.setPosicao('up')
limites = cen.getLimites()

def desenhaCenario():
	cen.moveCenario()
	prot.moveProtagonista(limites)
	screen.blit(cen.carregaCenario(), (cen.pos_x, cen.pos_y))
	screen.blit(prot.spriteSheet(), (prot.pos_x, prot.pos_y))
	#for i in range(0, cen.height, 16):
	#	for j in range(0, cen.width, 16):
	#		pygame.draw.rect(screen, (0), [j, i, 16, 16], 1)

def movimentaPersonagem(move):
	if move == 1:
		cen.mov_y += Glob.veloc_person
		prot.mov_y -= Glob.veloc_person
		
		prot.sprite_y = -96
		prot.sprite_x -= 32
		if prot.sprite_x < -96: prot.sprite_x = 0
	elif move == 2:
		cen.mov_y -= Glob.veloc_person
		prot.mov_y += Glob.veloc_person
		
		prot.sprite_y = 0
		prot.sprite_x -= 32
		if prot.sprite_x < -96: prot.sprite_x = 0
	elif move == 3:
		cen.mov_x += Glob.veloc_person
		prot.mov_x -= Glob.veloc_person
		
		prot.sprite_y = -32
		prot.sprite_x -= 32
		if prot.sprite_x < -96: prot.sprite_x = 0
	elif move == 4:
		cen.mov_x -= Glob.veloc_person
		prot.mov_x += Glob.veloc_person
		
		prot.sprite_y = -64
		prot.sprite_x -= 32
		if prot.sprite_x < -96: prot.sprite_x = 0
	
move = 0
while True:	
	desenhaCenario()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				move = 1
			if event.key == pygame.K_s:
				move = 2
			if event.key == pygame.K_a:
				move = 3
			if event.key == pygame.K_d:
				move = 4
			if event.key == pygame.K_F10:
				pygame.display.toggle_fullscreen()
			
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_w and move == 1:
				move = 0
			if event.key == pygame.K_s and move == 2:
				move = 0
			if event.key == pygame.K_a and move == 3:
				move = 0
			if event.key == pygame.K_d and move == 4:
				move = 0
	
	movimentaPersonagem(move)
	
	pygame.display.flip()
	clock.tick(27)


