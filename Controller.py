import pygame
from pygame.locals import *

class Controller:
	def __init__(self):
		self.model = None
		self.running = True

	def update(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.running = False

	def close(self):
		pygame.quit()