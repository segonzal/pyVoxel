from OpenGL.GL import *
from ctypes import *
import numpy

class Chunk:
	SIZE = (16,16,16)

	def __init__(self):
		(x,y,z) = Chunk.SIZE
		self.voxels = [None]*x*y*z
		self.changed = True
		self.vbo = glGenBuffers(1)
		self.elements = 0

	def delete(self):
		while len(self.voxels)!=0:
			del self.voxels[0]
		glDeleteBuffers(1,self.vbo)

	def get(self,x,y,z):
		(CX,CY,CZ) = Chunk.SIZE
		n = CX*CY*z + CX*y + x
		return self.voxels[n]

	def set(self,x,y,z,aType):
		(CX,CY,CZ) = Chunk.SIZE
		n = CX*CY*z + CX*y + x
		self.voxels[n] = aType
		self.changed = True

	def update(self):
		self.changed = False

		(CX,CY,CZ) = Chunk.SIZE

		vertices = numpy.zeros((CX*CY*CZ*6*6,4))
		i = 0

		for x in xrange(CX):
			for y in xrange(CY):
				for z in xrange(CZ):
					aType = self.get(x,y,z)

					# Empty block?
					if aType in (0,None):
						continue
					
					# view from negative x
					vertices[i] = ( x  , y  , z  , aType ); i+=1
					vertices[i] = ( x  , y  , z+1, aType ); i+=1
					vertices[i] = ( x  , y+1, z  , aType ); i+=1
					vertices[i] = ( x  , y+1, z  , aType ); i+=1
					vertices[i] = ( x  , y  , z+1, aType ); i+=1
					vertices[i] = ( x  , y+1, z+1, aType ); i+=1

					# view from positive x
					vertices[i] = ( x+1, y  , z  , aType ); i+=1
					vertices[i] = ( x+1, y  , z+1, aType ); i+=1
					vertices[i] = ( x+1, y+1, z  , aType ); i+=1
					vertices[i] = ( x+1, y+1, z  , aType ); i+=1
					vertices[i] = ( x+1, y  , z+1, aType ); i+=1
					vertices[i] = ( x+1, y+1, z+1, aType ); i+=1

					# view from negative y
					vertices[i] = ( x  , y  , z  , aType ); i+=1
					vertices[i] = ( x  , y  , z+1, aType ); i+=1
					vertices[i] = ( x+1, y  , z  , aType ); i+=1
					vertices[i] = ( x+1, y  , z  , aType ); i+=1
					vertices[i] = ( x  , y  , z+1, aType ); i+=1
					vertices[i] = ( x+1, y  , z+1, aType ); i+=1

					# view from positive y
					vertices[i] = ( x  , y+1, z  , aType ); i+=1
					vertices[i] = ( x  , y+1, z+1, aType ); i+=1
					vertices[i] = ( x+1, y+1, z  , aType ); i+=1
					vertices[i] = ( x+1, y+1, z  , aType ); i+=1
					vertices[i] = ( x  , y+1, z+1, aType ); i+=1
					vertices[i] = ( x+1, y+1, z+1, aType ); i+=1

					# view from negative z
					vertices[i] = ( x  , y  , z  , aType ); i+=1
					vertices[i] = ( x  , y+1, z  , aType ); i+=1
					vertices[i] = ( x+1, y  , z  , aType ); i+=1
					vertices[i] = ( x+1, y  , z  , aType ); i+=1
					vertices[i] = ( x  , y+1, z  , aType ); i+=1
					vertices[i] = ( x+1, y+1, z  , aType ); i+=1

					# view from positive z
					vertices[i] = ( x  , y  , z+1, aType ); i+=1
					vertices[i] = ( x  , y+1, z+1, aType ); i+=1
					vertices[i] = ( x+1, y  , z+1, aType ); i+=1
					vertices[i] = ( x+1, y  , z+1, aType ); i+=1
					vertices[i] = ( x  , y+1, z+1, aType ); i+=1
					vertices[i] = ( x+1, y+1, z+1, aType ); i+=1

		self.elements = i
		self.vert = vertices
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		glBufferData(GL_ARRAY_BUFFER, vertices[:i], GL_STATIC_DRAW)

	def render(self,shader):
		if self.changed:
			self.update()
		
		#if this chunk is empty, we don't need to draw it
		if self.elements == 0:
			return

		glEnable(GL_CULL_FACE)
		glEnable(GL_DEPTH_TEST)
		
		shader.bindAttributes("position",self.vbo,(4,GL_FLOAT,GL_FALSE,0,0))
#		glVertexPointer(4, GL_FLOAT, 0, self.vert)

		glDrawArrays(GL_TRIANGLES,0,self.elements)
		
		glDisableClientState( GL_VERTEX_ARRAY )
