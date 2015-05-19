import pygame
import math
from pygame.locals import *
from OpenGL.GL import *

def perspectiveGL(fovy,aspect,near,far):
	fH = math.tan(fovy/360.0)*math.pi * near
	fW = fH * aspect
	glFrustum(-fW,fW,-fH,fH,near,far)

class View:
	def __init__(self):
		self.model = None
		self.shader = None

		(WIDTH,HEIGHT) = 640, 480
		pygame.init()
		pygame.display.set_mode((WIDTH,HEIGHT), OPENGL | DOUBLEBUF)

		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		perspectiveGL(90.0,WIDTH/float(HEIGHT),1.0,100.0)
		glMatrixMode(GL_MODELVIEW)
		glEnable(GL_DEPTH_TEST)
		self.t = 0

	def update(self):
		self.shader.use()
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		glTranslatef(30*math.cos(self.t),30*math.sin(self.t),0.0)
		self.model.render(self.shader)
		self.t += 1

		pygame.display.flip()