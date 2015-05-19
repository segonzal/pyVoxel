import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from Camera import *

def perspectiveGL(fovy, aspect, near, far):
	fH = math.tan(fovy/360.0) * math.pi * near
	fW = fH * aspect
	glFrustum(-fW,fW,-fH,fH,near,far)

class View:
	def __init__(self):
		self.model = None
		self.shader = None
		self.camera = None

		(WIDTH,HEIGHT) = 640, 480
		pygame.init()
		pygame.display.set_mode((WIDTH,HEIGHT), OPENGL | DOUBLEBUF, 24)
		pygame.mouse.set_visible(False)
		glClearColor (0.0, 0.5, 0.5, 1.0)

		glEnable(GL_BLEND)
		glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glEnable(GL_CULL_FACE)
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LESS)
		
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		perspectiveGL(90.0,WIDTH/float(HEIGHT),0.1,50.0)
		glMatrixMode(GL_MODELVIEW)

	def update(self):
		self.shader.bindUniforms("viewPos",'3f',self.camera.x,self.camera.y,self.camera.z)

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		
		self.camera.lookThrough()

		self.model.render(self.shader)

		pygame.display.flip()