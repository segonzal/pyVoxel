import pygame
from pygame.locals import *

class Input:
	def __init__(self):
		self.keydown = []
		self.keyup = []
		self.keyhold = {}

		self.buttondown = []
		self.buttonup = []
		self.buttonhold = {}

		self.isCloseRequested = False
		self.mouseEntersScreen = lambda: None
		self.mousefocus = False

	def update(self):
		self.keydown = []
		self.keyup = []
		self.buttondown = []
		self.buttonup = []
		
		for event in pygame.event.get():
			if event.type == QUIT:
				self.isCloseRequested = True
			if event.type == KEYDOWN:
				self.keydown.append(event.key)
				self.keyhold[event.key] = True
			if event.type == KEYUP:
				self.keyup.append(event.key)
				self.keyhold[event.key] = False
			if event.type == MOUSEBUTTONDOWN:
				self.buttondown.append(event.button)
				self.buttonhold[event.button] = True
			if event.type == MOUSEBUTTONUP:
				self.buttonup.append(event.button)
				self.buttonhold[event.button] = False
			
		if not self.mousefocus and pygame.mouse.get_focused():
			self.mouseEntersScreen()
		self.mousefocus = pygame.mouse.get_focused()

	def keyPress(self,code):
		return code in self.keydown

	def keyHold(self,code):
		if code in self.keyhold:
			return self.keyhold[code]
		return False

	def keyRelease(self,code):
		return code in self.keyup

	def buttonPress(self,code):
		return code in self.buttondown

	def buttonHold(self,code):
		if code in self.buttonhold:
			return self.buttonhold[code]
		return False

	def buttonRelease(self,code):
		return code in self.buttonup
