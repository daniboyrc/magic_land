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
		self.pos = [posicao[0], posicao[1]]
		self.mov = [0, 0]
		
		img = Image.open(local)
		self.size = img.size
		self.limites = []
		
		self.protagonista = protagonista
		
		if self.pos[1] > 0:
			self.limites.append(self.pos[1])
		else:
			self.limites.append(0)
		if self.size[0] >= Tela.width:
			self.limites.append(Tela.width)
		else:
			self.limites.append(self.size[0] + self.pos[0])
		if self.size[1] >= Tela.height:
			self.limites.append(Tela.height)
		else:
			self.limites.append(self.size[1] + self.pos[1])
		if self.pos[0] > 0:
			self.limites.append(self.pos[0])
		else:
			self.limites.append(0)
	
	def setPosicao(self, local = '', pos = (0, 0)):
		if local == 'up':
			self.pos[0] = Tela.width / 2 - self.size[0] / 2
			self.pos[1] = 0
		elif local == 'left':
			self.pos[0] = 0
			self.pos[1] = Tela.height / 2 - self.size[1] / 2
		elif local == 'center':
			self.pos[0] = Tela.width / 2 - self.size[0] / 2
			self.pos[1] = Tela.height / 2 - self.size[1] / 2
		elif local == 'right':
			self.pos[0] = Tela.width - self.size[0]
			self.pos[1] = Tela.height / 2 - self.size[1] / 2 
		elif local == 'down':
			self.pos[0] = Tela.width / 2 - self.size[0] / 2 
			self.pos[1] = Tela.height - self.size[1]
		else:
			self.pos[0] = pos[0]
			self.pos[1] = pos[1]

	def moveCenario(self):
		if self.size[0] > Tela.width:
			if Tela.width - self.size[0] < self.pos[0] + self.mov[0] < 0: 
				self.pos[0] += self.mov[0]
			else:
				self.protagonista.mov[0] *= 2
		else:
			self.protagonista.mov[0] *= 2
		if self.size[1] > Tela.height:
			if Tela.height - self.size[1] < self.pos[1] + self.mov[1] < 0:
				self.pos[1] += self.mov[1]
			else:
				self.protagonista.mov[1] *= 2
		else:
				self.protagonista.mov[1] *= 2
			
		self.mov[0] = 0
		self.mov[1] = 0

class Protagonista(pygame.sprite.Sprite):
	
	def __init__(self, local, pos):
		pygame.sprite.Sprite.__init__(self)
		self.local = local
		self.velocidade = 3
		self.pos = [pos[0], pos[1]]
		self.mov = [0, 0]
		self.direcao = 0
		self.acao = False
		self.sprite = [0, 0]
		self.rect = pygame.Rect(self.pos[0], self.pos[1], 32, 32)
	
	def spriteSheet(self):
		sprite_sheet = pygame.image.load(self.local)
		image = pygame.Surface([32, 32])
		image.set_colorkey((0,0,0), pygame.RLEACCEL)
		image.blit(sprite_sheet, (self.sprite[0], self.sprite[1]))
		return image
		
	def moveProtagonista(self, limites):
		if self.pos[0] + self.mov[0] > limites[3] and self.pos[0] + self.mov[0] + 32 < limites[1]:
			self.pos[0] += self.mov[0]
		if self.pos[1] + self.mov[1] > limites[0] and self.pos[1] + self.mov[1] + 32 < limites[2]:
			self.pos[1] += self.mov[1]
		
		self.rect = pygame.Rect(self.pos[0] + 9, self.pos[1] + 5, 16, 25)

		self.mov[0] = 0
		self.mov[1] = 0

class Npc(pygame.sprite.Sprite):
	def __init__(self, coord, img, nome):
		pygame.sprite.Sprite.__init__(self)
		self.coord = coord
		self.img = img
		self.sprite = 0
		self.nome = nome
		self.rect = pygame.Rect(self.coord[0], self.coord[1], 40, 40)
		# self.falas = []
		# self.quest = []
		
	def spriteSheet(self):
		sprite_sheet = pygame.image.load(self.img)
		image = pygame.Surface([32, 32])
		image.set_colorkey((0,0,0), pygame.RLEACCEL)
		image.blit(sprite_sheet, (0, self.sprite))
		
		return image
		
class Colide():
	def __init__(self, local):
		self.local = local
		self.colisao = []
		self.npc = None
		self.porta = []
		
		arq = open(local, 'r')
		for i in arq:
			i = i.split()
			if i[2] == 'c':
				self.colisao.append(pygame.Rect(int(i[0]), int(i[1]), 16, 16))
			#if i[2] == 'f':
			#	self.npc.append(pygame.Rect(int(i[0]), int(i[1]), 16, 16))
			if i[2] == 'e':
				self.porta.append(pygame.Rect(int(i[0]), int(i[1]), 16, 16))
		arq.close()
		











