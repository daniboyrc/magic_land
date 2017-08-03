# coding: utf-8:

import pygame
from var_global import *
from utils import *

pygame.init()

pygame.display.set_caption('RPG game')
clock = pygame.time.Clock()

prot = Protagonista('img/personagens/principal/person.png', (70, 200))
cen = Cenario('img/cenarios/fase1/mapa.png', prot, (10, 10))
cen.setPosicao((0,0))
limites = cen.getLimites()

screen = pygame.display.set_mode((cen.width, cen.height))

def getCor(tipo):
	if tipo == 'c':
		cor = (0, 255, 0)
	elif tipo == 'e':
		cor = (0, 0, 255)
	elif tipo == 'f':
		cor = (255, 0, 0)
	return cor
	
def desenhaCenario():
	cen.moveCenario()
	prot.moveProtagonista(limites)
	screen.blit(cen.carregaCenario(), (cen.pos_x, cen.pos_y))
	screen.blit(prot.spriteSheet(), (prot.pos_x, prot.pos_y))
	for i in coordenadas:
		pygame.draw.rect(screen, getCor(i[2]), [i[0] * 16 + cen.mov_x, i[1] * 16 + cen.mov_y, 16, 16])
	
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
		
tipo = 'c'
move = 0
coordenadas = []

arq = open('mapa.txt', 'r')
for i in arq:
	i = i.split()
	coordenadas.append([int(i[0]) / 16, int(i[1]) / 16, i[2]])
arq.close()

while True:	
	desenhaCenario()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			confirm = raw_input('Deseja salvar? ')
			if confirm == 's':
				arq = open('mapa.txt', 'w')
				for i in coordenadas:
					arq.write(str(i[0] * 16) + ' ' + str(i[1] * 16) + ' ' + i[2] + '\n')
				arq.close()
				pygame.quit()
			if confirm == 'n':
				pygame.quit()
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			pos_x, pos_y = pygame.mouse.get_pos()
			pos_x = (pos_x - cen.pos_x) / 16
			pos_y = (pos_y - cen.pos_y) / 16
			
			var = True
			for i in 'cef':
				if [pos_x, pos_y, i] in coordenadas:
					coordenadas.remove([pos_x, pos_y, i])
					var = False
			if var:
				coordenadas.append([pos_x, pos_y, tipo])
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				move = 1
			if event.key == pygame.K_s:
				move = 2
			if event.key == pygame.K_a:
				move = 3
			if event.key == pygame.K_d:
				move = 4
			if event.key == pygame.K_j:
				tipo = 'c' # colidir
			if event.key == pygame.K_k:
				tipo = 'e' # entrar
			if event.key == pygame.K_l:
				tipo = 'f' # falar
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
