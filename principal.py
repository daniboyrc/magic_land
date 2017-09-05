# coding: utf-8

import pygame
from classes import *
from utils import *

pygame.init()

screen = pygame.display.set_mode((Tela.width, Tela.height))
pygame.display.set_caption('Magic Land')
clock = pygame.time.Clock()
		
prot = Protagonista('fases/fase1/personagens/prot.png', (480, 450))
cen = Cenario('fases/fase1/cenarios/mapa2.jpg')
cen.setPosicao('center')
cen.setLimites()
colid = Colide('fases/fase1/cenarios/mapa.txt')

# ------------- instanciando npcs ---------------
mago = Npc([64, 256], 'fases/fase1/personagens/mago.png', 'mago')
cavaleiro = Npc([500, 222], 'fases/fase1/personagens/cavaleiro.png', 'cavaleiro')
porto = Npc([380, 616], 'fases/fase1/personagens/porto.png', 'homem do porto')
vendedor = Npc([736, 48], 'fases/fase1/personagens/vendedor.png', 'vendedor') 	

npc = [mago, cavaleiro, porto, vendedor]

def detectaColisao(p_antx, p_anty, c_antx, c_anty):	
	
	for i in colid.porta:
		if i.move(cen.pos[0], cen.pos[1]).colliderect(prot.rect):
			prot.mov[0] = prot.mov[1] = cen.mov[0] = cen.mov[1] = 0
			prot.pos[0], prot.pos[1] = p_antx, p_anty
			cen.pos[0], cen.pos[1] = c_antx, c_anty
			continue
	
	for i in colid.colisao:
		if prot.rect.colliderect(i.move(cen.pos[0], cen.pos[1])):
			prot.mov[0] = prot.mov[1] = cen.mov[0] = cen.mov[1] = 0
			prot.pos[0], prot.pos[1] = p_antx, p_anty
			cen.pos[0], cen.pos[1] = c_antx, c_anty		
			
	for i in npc:
		if not prot.rect.colliderect(i.area_interacao.move(cen.pos[0], cen.pos[1])):
			i.sprite = 0
				
		if prot.rect.colliderect(i.rect.move(cen.pos[0] - 4, cen.pos[1] - 4)):
			prot.mov[0] = prot.mov[1] = cen.mov[0] = cen.mov[1] = 0
			prot.pos[0], prot.pos[1] = p_antx, p_anty
			cen.pos[0], cen.pos[1] = c_antx, c_anty
			if prot.direcao == 1:
				i.sprite = 0
			if prot.direcao == 2:
				i.sprite = -96
			if prot.direcao == 3:
				i.sprite = -64
			if prot.direcao == 4:
				i.sprite = -32

def acao():
	for i in npc:
		if prot.rect.colliderect(i.area_interacao.move(cen.pos[0], cen.pos[1])):
			print 'oi, eu sou um ' + i.nome
			
		
def desenhaCenario():
	p_antx, p_anty = prot.pos[0], prot.pos[1]
	c_antx, c_anty = cen.pos[0], cen.pos[1]
	
	cen.moveCenario()
	prot.moveProtagonista(cen.limites)
	
	detectaColisao(p_antx, p_anty, c_antx, c_anty)
	
	screen.blit(pygame.image.load(cen.local), (cen.pos[0], cen.pos[1]))
	screen.blit(prot.spriteSheet(), (prot.pos[0], prot.pos[1]))
	for i in npc:
		screen.blit(i.spriteSheet(), i.rect.move(cen.pos[0], cen.pos[1]))
	
	# ------------- visualização da colisão ---------------
	for i in colid.colisao:
		pygame.draw.rect(screen, (0, 255, 0), i.move(cen.pos[0], cen.pos[1]), 1)
	for i in colid.porta:
		pygame.draw.rect(screen, (0, 0, 255), i.move(cen.pos[0], cen.pos[1]), 1)
	for i in npc:
		pygame.draw.rect(screen, (255, 0, 0), i.rect.move(cen.pos[0] - 4, cen.pos[1] - 4), 1)
	pygame.draw.rect(screen, (0), prot.rect, 1)
	for i in npc:
		pygame.draw.rect(screen, (255, 255, 0), i.area_interacao.move(cen.pos[0] - 4, cen.pos[1] - 4), 1)
	
def movimentaPersonagem(move):
	if move == 1:
		if Tela.height / 2 - prot.velocidade < prot.pos[1] < Tela.height / 2 + prot.velocidade and cen.pos[1] + cen.mov[1] + prot.velocidade < 0:
			cen.mov[1] += prot.velocidade
		else:
			prot.mov[1] -= prot.velocidade
			
		prot.sprite[1] = -96
		prot.sprite[0] -= 32
		if prot.sprite[0] < -96: prot.sprite[0] = 0
		
	elif move == 2:
		if Tela.height / 2 - prot.velocidade < prot.pos[1] < Tela.height / 2 + prot.velocidade and Tela.height - cen.size[1] < cen.pos[1] + cen.mov[1] - prot.velocidade :
			cen.mov[1] -= prot.velocidade
		else:
			prot.mov[1] += prot.velocidade
			
		prot.sprite[1] = 0
		prot.sprite[0] -= 32
		if prot.sprite[0] < -96: prot.sprite[0] = 0
		
	elif move == 3:
		if Tela.width / 2 - prot.velocidade < prot.pos[0] < Tela.width / 2 + prot.velocidade and cen.pos[0] + cen.mov[0] + prot.velocidade < 0:
			cen.mov[0] += prot.velocidade
		else:
			prot.mov[0] -= prot.velocidade
			
		prot.sprite[1] = -32
		prot.sprite[0] -= 32
		if prot.sprite[0] < -96: prot.sprite[0] = 0
		
	elif move == 4:
		if Tela.width / 2 - prot.velocidade < prot.pos[0] < Tela.width / 2 + prot.velocidade and Tela.width - cen.size[0] < cen.pos[0] + cen.mov[0] - prot.velocidade:
			cen.mov[0] -= prot.velocidade
		else:
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
				prot.direcao = 1
			if event.key == pygame.K_s:
				move = 2
				prot.direcao = 2
			if event.key == pygame.K_a:
				move = 3
				prot.direcao = 3
			if event.key == pygame.K_d:
				move = 4
				prot.direcao = 4
			if event.key == pygame.K_SPACE:
				acao()
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


