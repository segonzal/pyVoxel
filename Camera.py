from OpenGL.GL import *
import math
import utils

# # # # # # # # # # # # #
#   Y                   #
#   |                   #
#   |                   #
#   | pitch             #
#   |.   /Z             #
#   | . /               #
#   | :/.. yaw          #
#   | /   `.            #
#   |/______:_________X #
#                       #
# # # # # # # # # # # # #

class Camera:
	def __init__(self,x=0.0,y=0.0,z=0.0):#-25.0,y=-2.5,z=25.0
		self.x = y
		self.y = x
		self.z = z
		self._yaw = -180
		self._pitch = 0
		self.vbo = glGenBuffers(1)

	def yaw(self,dyaw):
		self._yaw += dyaw

	def pitch(self,dpitch):
		self._pitch += dpitch

	def walkForward(self,distance):
		self.x += distance * math.sin(math.radians(self._yaw))
		self.z -= distance * math.cos(math.radians(self._yaw))

	def walkBackwards(self,distance):
		self.x -= distance * math.sin(math.radians(self._yaw))
		self.z += distance * math.cos(math.radians(self._yaw))

	def strafeLeft(self,distance):
		self.x += distance * math.sin(math.radians(self._yaw-90))
		self.z -= distance * math.cos(math.radians(self._yaw-90))

	def strafeRight(self,distance):
		self.x -= distance * math.sin(math.radians(self._yaw-90))
		self.z += distance * math.cos(math.radians(self._yaw-90))

	def moveUp(self,distance):
		self.y += distance

	def moveDown(self,distance):
		self.y -= distance

	def lookThrough(self,shader):
		glRotate(self._pitch,1.0,0.0,0.0)
		glRotate(self._yaw,0.0,1.0,0.0)
		glTranslate(-self.x,-self.y,-self.z)

	def getPosition(self):
		return (self.x,self.y,self.z)

	def getFocus(self):
		y = math.radians(180-self._yaw)
		p = math.radians(-270+self._pitch)
		cosP = math.cos(p)
		sinP = math.sin(p)
		cosA = math.cos(y)
		sinA = math.sin(y)
		R = 5.0
		x = self.x + R*sinA*sinP
		y = self.y + R*cosP
		z = self.z + R*cosA*sinP
		return (x,y,z)

	def drawFocus(self,shader):
		fx,fy,fz = self.getFocus()
		fx,fy,fz = int(fx),int(fy),int(fz)
		shader.uniform("translate",'3f',fx,fy,fz)

		shader.uniform("flag",'1f',1)
		vertices = utils.createCube((0,0,0),(1,1,1),color=(0.0,0.0,1.0,0.25))
		elements = 36

		stride = 4*10
		shader.bufferData(vertices,self.vbo)

		offset = 4*0
		shader.attribute("position",4,GL_FLOAT,False,stride,offset)
		offset += 4*3
		shader.attribute("color"   ,4,GL_FLOAT,False,stride,offset)
		offset += 4*4
		shader.attribute("normal"  ,4,GL_FLOAT,True ,stride,offset)

		p_loc = shader.getAttribLocation("position")
		c_loc = shader.getAttribLocation("color")
		n_loc = shader.getAttribLocation("normal")
		
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		
		stride = 4*10
		offset = 4*0
		glVertexAttribPointer(p_loc, 4, GL_FLOAT, False, stride, ctypes.c_void_p(offset))
		offset += 4*3
		glVertexAttribPointer(c_loc, 4, GL_FLOAT, False, stride, ctypes.c_void_p(offset))
		offset += 4*4
		glVertexAttribPointer(n_loc, 4, GL_FLOAT, True, stride, ctypes.c_void_p(offset))

		glEnableVertexAttribArray(p_loc)
		glEnableVertexAttribArray(c_loc)
		glEnableVertexAttribArray(n_loc)
		
		glDrawArrays(GL_TRIANGLES,0,elements)

		glDisableVertexAttribArray(p_loc)
		glDisableVertexAttribArray(c_loc)
		glDisableVertexAttribArray(n_loc)