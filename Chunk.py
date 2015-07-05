from OpenGL.GL import *
from ctypes import *
import numpy
from OpenGL.arrays import vbo
import utils

# # # # # # # # # # # # # # # # # # # # # # # # # #
#       _____________   #           +1   -1       #
#      /|010     110/|  #        (Y) |   /        #
#     / |          / |  #            |  /         #
#    /  |         /  |  #            | /          #
#   /___|________/   |  #            |/           #
#  |011 |     111|   |  #  -1________|_________+1 #
#  |    |________|___|  #           /|        (X) #
#  |   /000      |100/  #          / |            #
#  |  /          |  /   #         /  | OpenGL     #
#  | /           | /    #        /   | Coordinate #
#  |/____________|/     #    (Z)/    | System     #
#  001        101       #     +1    -1            #
# # # # # # # # # # # # # # # # # # # # # # # # # #

def myExtend(l,*args):
	for e in args:
		l.append(e)

class Chunk:
	SIZE = (16,16,16)
	color = [
		(0.0,0.0,1.0,1.0),
		(0.0,1.0,0.0,1.0),
		(1.0,0.0,0.0,1.0),
		(0.5,0.5,0.0,1.0),
		(0.0,0.5,0.5,1.0),
		(0.5,0.0,0.5,1.0)]

	def __init__(self,parent,position):
		self.parent = parent
		self.position = position
		(x,y,z) = Chunk.SIZE
		self.voxels = [None]*x*y*z
		self.changed = True
		self.vbo = glGenBuffers(1)
		self.elements = 0
		self.n = 0

	def get(self,x,y,z):
		(CX,CY,CZ) = Chunk.SIZE
		if (x<0 or x>=CX) or (y<0 or y>=CY) or (z<0 or z>=CZ):
			(px,py,pz) = self.position
			return self.parent.get(px+x,py+y,pz+z)

		n = CX*CY*z + CX*y + x
		return self.voxels[n]

	def set(self,x,y,z,aType):
		(CX,CY,CZ) = Chunk.SIZE
		n = CX*CY*z + CX*y + x
		self.voxels[n] = aType
		self.changed = True
		if aType==0:
			self.n-=1
		else:
			self.n+=1

	def isFull(self):
		(CX,CY,CZ) = Chunk.SIZE
		return self.n == CX*CY*CZ

	def update(self,shader):
		self.changed = False

		(CX,CY,CZ) = Chunk.SIZE

		vertices = numpy.zeros(CX*CY*CZ*36, [
								("position", numpy.float32, 3),
								("color"   , numpy.float32, 4),
								("normal"  , numpy.float32, 3)])
		l = 0
		for x in xrange(CX):
			for y in xrange(CY):
				for z in xrange(CZ):
					# the python way is always mysterious and unknown
					aType = self.get(x,y,z)

					top    = self.get(x,y+1,z)
					bottom = self.get(x,y-1,z)
					front  = self.get(x,y,z-1)
					back   = self.get(x,y,z+1)
					right  = self.get(x+1,y,z)
					left   = self.get(x-1,y,z)

					# Empty block?
					if aType in (0,None):
						continue

					(xi,yi,zi) = (x,y,z)
					(xf,yf,zf) = (xi+1,yi+1,zi+1)
					#vertices[l:l+36] = utils.createCube((i,j,k),(i+1,j+1,k+1),Chunk.color[aType-1])

					color = Chunk.color[aType-1]

					if left in (0,None):
						vertices["position"][l:l+6] = [
							(xi, yi, zi),
							(xi, yi, zf),
							(xi, yf, zf),
							(xi, yf, zf),
							(xi, yf, zi),
							(xi, yi, zi)]
						vertices["color"][l:l+6] = color
						vertices["normal"][l:l+6] = (+1.0,  0.0,  0.0)
						l += 6

					if right in (0,None):
						vertices["position"][l:l+6] = [
							(xf, yi, zi),
							(xf, yf, zf),
							(xf, yi, zf),
							(xf, yf, zf),
							(xf, yi, zi),
							(xf, yf, zi)]
						vertices["color"][l:l+6] = color
						vertices["normal"][l:l+6] = (-1.0,  0.0,  0.0)
						l += 6

					if bottom in (0,None):
						vertices["position"][l:l+6] = [
							(xf, yi, zi),
							(xf, yi, zf),
							(xi, yi, zf),
							(xi, yi, zf),
							(xi, yi, zi),
							(xf, yi, zi)]
						vertices["color"][l:l+6] = color
						vertices["normal"][l:l+6] = ( 0.0, +1.0,  0.0)
						l += 6

					if top in (0,None):
						vertices["position"][l:l+6] = [
							(xf, yf, zi),
							(xi, yf, zf),
							(xf, yf, zf),
							(xi, yf, zf),
							(xf, yf, zi),
							(xi, yf, zi)]
						vertices["color"][l:l+6] = color
						vertices["normal"][l:l+6] = ( 0.0, -1.0,  0.0)
						l += 6

					if front in (0,None):
						vertices["position"][l:l+6] = [
							(xi, yi, zi),
							(xi, yf, zi),
							(xf, yf, zi),
							(xf, yf, zi),
							(xf, yi, zi),
							(xi, yi, zi)]
						vertices["color"][l:l+6] = color
						vertices["normal"][l:l+6] = ( 0.0,  0.0, +1.0)
						l += 6

					if back in (0,None):
						vertices["position"][l:l+6] = [
							(xi, yi, zf),
						(xf, yf, zf),
						(xi, yf, zf),
						(xf, yf, zf),
						(xi, yi, zf),
						(xf, yi, zf)]
						vertices["color"][l:l+6] = color
						vertices["normal"][l:l+6] = ( 0.0,  0.0, -1.0)
						l += 6

		self.vertices = vertices[:l]
		self.elements = l

		stride = 4*10
		shader.bufferData(vertices,self.vbo)

		offset = 4*0
		shader.attribute("position",3,GL_FLOAT,False,stride,offset)
		offset += 4*3
		shader.attribute("color"   ,4,GL_FLOAT,False,stride,offset)
		offset += 4*4
		shader.attribute("normal"  ,3,GL_FLOAT,True ,stride,offset)
		print "finished updating chunk", self.position

	def render(self,shader):
		if self.changed:
			self.update(shader)

		#if this chunk is empty, we don't need to draw it
		if self.elements == 0:
			return

		p_loc = shader.getAttribLocation("position")
		c_loc = shader.getAttribLocation("color")
		n_loc = shader.getAttribLocation("normal")
		
		glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
		
		stride = 4*10
		offset = 4*0
		glVertexAttribPointer(p_loc, 3, GL_FLOAT, False, stride, ctypes.c_void_p(offset))
		offset += 4*3
		glVertexAttribPointer(c_loc, 4, GL_FLOAT, False, stride, ctypes.c_void_p(offset))
		offset += 4*4
		glVertexAttribPointer(n_loc, 3, GL_FLOAT, True, stride, ctypes.c_void_p(offset))

		glEnableVertexAttribArray(p_loc)
		glEnableVertexAttribArray(c_loc)
		glEnableVertexAttribArray(n_loc)
		
		glDrawArrays(GL_TRIANGLES,0,self.elements)

		glDisableVertexAttribArray(p_loc)
		glDisableVertexAttribArray(c_loc)
		glDisableVertexAttribArray(n_loc)