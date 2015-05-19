from OpenGL.GL import *
import math
import utils

class Camera:
	def __init__(self):
		self.x = -25.0
		self.y = -2.5
		self.z = 25.0
		self._yaw = -180
		self._pitch = 0

	def yaw(self,dyaw):
		self._yaw += dyaw

	def pitch(self,dpitch):
		self._pitch += dpitch

	def walkForward(self,distance):
		self.x -= distance * math.sin(math.radians(self._yaw))
		self.z += distance * math.cos(math.radians(self._yaw))

	def walkBackwards(self,distance):
		self.x += distance * math.sin(math.radians(self._yaw))
		self.z -= distance * math.cos(math.radians(self._yaw))

	def strafeLeft(self,distance):
		self.x -= distance * math.sin(math.radians(self._yaw-90))
		self.z += distance * math.cos(math.radians(self._yaw-90))

	def strafeRight(self,distance):
		self.x += distance * math.sin(math.radians(self._yaw-90))
		self.z -= distance * math.cos(math.radians(self._yaw-90))

	def moveUp(self,distance):
		self.y -= distance

	def moveDown(self,distance):
		self.y += distance

	def lookThrough(self,shader):
		glRotate(self._pitch,1.0,0.0,0.0)
		glRotate(self._yaw,0.0,1.0,0.0)
		glTranslate(self.x,self.y,self.z)