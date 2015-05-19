import pygame
from pygame.locals import *
from Input import *
from OpenGL.GL import *

class Controller:
	mouseSensitivity = 0.15
	movementSpeed = 0.005

	def __init__(self):
		self.model = None
		self.view = None
		self.running = True

		self.t = pygame.time.get_ticks()
		self.input = Input()
		self.wireframe = False
		#self.input.mouseEntersScreen = lambda: pygame.mouse.set_pos(640/2, 480/2)

	def update(self):
		tiempoActual = pygame.time.get_ticks()
		dt = tiempoActual - self.t
		self.t = tiempoActual

		(mouseX,mouseY) = pygame.mouse.get_pos()
		(dx,dy) = pygame.mouse.get_rel()

		self.input.update()

		if self.input.isCloseRequested:
			self.running = False
		if self.input.keyPress(pygame.K_ESCAPE):
			self.running = False
		
		#if self.input.buttonHold(1):
		self.view.camera.yaw(dx * Controller.mouseSensitivity)
		self.view.camera.pitch(dy * Controller.mouseSensitivity)

		if self.input.keyRelease(pygame.K_f):
			pygame.display.toggle_fullscreen()
			self.view.reshape()

		if self.input.keyHold(pygame.K_w):
			self.view.camera.walkForward(Controller.movementSpeed*dt)
		if self.input.keyHold(pygame.K_s):
			self.view.camera.walkBackwards(Controller.movementSpeed*dt)
		if self.input.keyHold(pygame.K_a):
			self.view.camera.strafeLeft(Controller.movementSpeed*dt)
		if self.input.keyHold(pygame.K_d):
			self.view.camera.strafeRight(Controller.movementSpeed*dt)
		if self.input.keyHold(pygame.K_SPACE):
			self.view.camera.moveUp(Controller.movementSpeed*dt)
		if self.input.keyHold(pygame.K_LSHIFT):
			self.view.camera.moveDown(Controller.movementSpeed*dt)

		if (not self.wireframe) and self.input.keyPress(pygame.K_p):
			glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
			self.wireframe = True

		elif self.wireframe and self.input.keyPress(pygame.K_p):
			glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
			self.wireframe = False

	def close(self):
		pygame.quit()