# coding: utf-8

import pygame
from classes import *
from utils import *

pygame.init()

screen = pygame.display.set_mode((Tela.width, Tela.height))
pygame.display.set_caption('RPG game')
clock = pygame.time.Clock()
		
prot = Protagonista('fases/fase1/personagens/prot.png', (70, 200))
cen = Cenario('fases/fase1/cenarios/mapa.png', prot, (10, 10))
cen.setPosicao('up')
colid = Colide('fases/fase1/cenarios/mapa.txt')

def detectaColisao(p_antx, p_anty, c_antx, c_anty):
	for i in colid.colisao:
		if prot.rect.colliderect(i.move(cen.pos[0], cen.pos[1])):
			prot.mov[0] = prot.mov[1] = cen.mov[0] = cen.mov[1] = 0
			prot.pos[0], prot.pos[1] = p_antx, p_anty
			cen.pos[0], cen.pos[1] = c_antx, c_anty
			
def desenhaCenario():
	p_antx, p_anty = prot.pos[0], prot.pos[1]
	c_antx, c_anty = cen.pos[0], cen.pos[1]
	
	cen.moveCenario()
	prot.moveProtagonista(cen.limites)
	
	detectaColisao(p_antx, p_anty, c_antx, c_anty)
	
	screen.blit(pygame.image.load(cen.local), (cen.pos[0], cen.pos[1]))
	screen.blit(prot.spriteSheet(), (prot.pos[0], prot.pos[1]))
	
	# ------------- visualização da colisão ---------------
	#for i in colid.colisao:
	#	pygame.draw.rect(screen, (0, 255, 0), i.move(cen.pos[0], cen.pos[1]), 1)
	#for i in colid.npc:
	#	pygame.draw.rect(screen, (255, 0, 0), i.move(cen.pos[0], cen.pos[1]), 1)
	#for i in colid.porta:
	#	pygame.draw.rect(screen, (0, 0, 255), i.move(cen.pos[0], cen.pos[1]), 1)

	#pygame.draw.rect(screen, (0), prot.rect, 1)

def movimentaPersonagem(move):
	if move == 1:
		cen.mov[1] += prot.velocidade
		prot.mov[1] -= prot.velocidade
		
		prot.sprite[1] = -96
		prot.sprite[0] -= 32
		if prot.sprite[0] < -96: prot.sprite[0] = 0
	elif move == 2:
		cen.mov[1] -= prot.velocidade
		prot.mov[1] += prot.velocidade
		
		prot.sprite[1] = 0
		prot.sprite[0] -= 32
		if prot.sprite[0] < -96: prot.sprite[0] = 0
	elif move == 3:
		cen.mov[0] += prot.velocidade
		prot.mov[0] -= prot.velocidade
		
		prot.sprite[1] = -32
		prot.sprite[0] -= 32
		if prot.sprite[0] < -96: prot.sprite[0] = 0
	elif move == 4:
		cen.mov[0] -= prot.velocidade
		prot.mov[0] += prot.velocidade
		
		prot.sprite[1] = -64
		prot.sprite[0] -= 32
		if prot.sprite[0] < -96: prot.sprite[0] = 0
	
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


