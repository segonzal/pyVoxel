import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from Camera import *
import utils

class View:
	def __init__(self):
		self.model = None
		self.shader = None
		self.camera = None

		(WIDTH,HEIGHT) = 640, 480
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT), OPENGL | DOUBLEBUF, 24)
		pygame.mouse.set_visible(False)
		glClearColor (0.0, 0.5, 0.5, 1.0)

		glEnable(GL_BLEND)
		glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glHint (GL_LINE_SMOOTH_HINT, GL_NICEST)
		glEnable(GL_CULL_FACE)
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LESS)

		self.angle = 0;

	def getSize(self):
		return self.screen.get_size()

	def reshape(self):
		WIDTH,HEIGHT = self.getSize()

		glViewport(0, 0, WIDTH,HEIGHT)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		utils.perspectiveGL(90.0,WIDTH/float(HEIGHT),0.1,100.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def update(self):
		rad = math.radians(self.angle)
		self.angle += 0.05
		self.shader.uniform("lightPos",'3f',-50*math.cos(rad),-75.0,-50*math.sin(rad))

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()

		self.camera.lookThrough(self.shader)

		self.model.render(self.shader)

		pygame.display.flip()