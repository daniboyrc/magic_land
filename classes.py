# coding: utf-8

import PIL
from PIL import Image
import pygame

class Tela:
	
	width = 800
	height = 600

class Cenario():
	
	def __init__(self, local, protagonista, posicao = (0, 0)):
		self.local = local
		self.pos_x = posicao[0]
		self.pos_y = posicao[1]
		self.mov_x = 0
		self.mov_y = 0
		self.protagonista = protagonista
		img = Image.open(local)
		self.width, self.height = img.size
		self.limites = []
		
		if self.pos_y > 0:
			self.limites.append(self.pos_y)
		else:
			self.limites.append(0)
		if self.width >= Tela.width:
			self.limites.append(Tela.width)
		else:
			self.limites.append(self.width + self.pos_x)
		if self.height >= Tela.height:
			self.limites.append(Tela.height)
		else:
			self.limites.append(self.height + self.pos_y)
		if self.pos_x > 0:
			self.limites.append(self.pos_x)
		else:
			self.limites.append(0)
	
	def setPosicao(self, local = '', pos = (0, 0)):
		if local == 'up':
			self.pos_x = Tela.width / 2 - self.width / 2
			self.pos_y = 0
		elif local == 'left':
			self.pos_x = 0
			self.pos_y = Tela.height / 2 - self.height / 2
		elif local == 'center':
			self.pos_x = Tela.width / 2 - self.width / 2
			self.pos_y = Tela.height / 2 - self.height / 2
		elif local == 'right':
			self.pos_x = Tela.width - self.width
			self.pos_y = Tela.height / 2 - self.height / 2 
		elif local == 'down':
			self.pos_x = Tela.width / 2 - self.width / 2 
			self.pos_y = Tela.height - self.height
		else:
			self.pos_x = pos[0]
			self.pos_y = pos[1]

	def moveCenario(self):
		if self.width > Tela.width:
			if Tela.width - self.width < self.pos_x + self.mov_x < 0: 
				self.pos_x += self.mov_x
			else:
				self.protagonista.mov_x *= 2
		else:
			self.protagonista.mov_x *= 2
		if self.height > Tela.height:
			if Tela.height - self.height < self.pos_y + self.mov_y < 0:
				self.pos_y += self.mov_y
			else:
				self.protagonista.mov_y *= 2
		else:
				self.protagonista.mov_y *= 2
			
		self.mov_x = 0
		self.mov_y = 0

class Protagonista(pygame.sprite.Sprite):
	
	def __init__(self, local, pos):
		pygame.sprite.Sprite.__init__(self)
		self.local = local
		self.velocidade = 2
		self.pos_x = pos[0]
		self.pos_y = pos[1]
		self.mov_x = 0
		self.mov_y = 0
		self.move = 0
		self.sprite_x = 0
		self.sprite_y = 0
		
	def spriteSheet(self):
		sprite_sheet = pygame.image.load(self.local)
		image = pygame.Surface([32, 32])
		image.set_colorkey((0,0,0), pygame.RLEACCEL)
		image.blit(sprite_sheet, (self.sprite_x, self.sprite_y))
		return image
		
	def moveProtagonista(self, limites):
		if self.pos_x + self.mov_x > limites[3] and self.pos_x + self.mov_x + 32 < limites[1]:
			self.pos_x += self.mov_x
		if self.pos_y + self.mov_y > limites[0] and self.pos_y + self.mov_y + 32 < limites[2]:
			self.pos_y += self.mov_y
		
		self.mov_x = 0
		self.mov_y = 0

class Colide():
	def __init__(self):
		self.colid = {'c': [], 'f': [], 'e': []}
		self.colisao = []
		self.npc = []
		self.porta = []
		
		arq = open('mapa.txt', 'r')
		for i in arq:
			i = i.split()
			if i[2] == 'c':
				self.colisao.append(pygame.Rect(int(i[0]), int(i[1]), 16, 16))
			if i[2] == 'f':
				self.npc.append(pygame.Rect(int(i[0]), int(i[1]), 16, 16))
			if i[2] == 'e':
				self.porta.append(pygame.Rect(int(i[0]), int(i[1]), 16, 16))
		arq.close()
		
