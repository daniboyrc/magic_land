# coding: utf-8

import pygame
from var_global import *
from utils import *

pygame.init()

screen = pygame.display.set_mode((Tela.width, Tela.height))
pygame.display.set_caption('RPG game')
clock = pygame.time.Clock()
		
prot = Protagonista('personagem.png', (400, 300))
cen = Cenario('back.png', prot)
cen.setPosicao('right')
limites = cen.getLimites()

def desenhaCenario():
	cen.moveCenario()
	prot.moveProtagonista(limites)
	screen.blit(cen.carregaCenario(), (cen.pos_x, cen.pos_y))
	screen.blit(prot.spriteSheet(), (prot.pos_x, prot.pos_y))

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
			move = 0
	
	movimentaPersonagem(move)
	
	pygame.display.flip()
	clock.tick(25)


