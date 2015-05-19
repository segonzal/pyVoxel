from OpenGL.GL import *
from ctypes import *
import numpy
from OpenGL.arrays import vbo

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

va = None
no = None

def normalize_v3(arr):
    ''' Normalize a numpy array of 3 component vectors shape=(n,3) '''
    lens = numpy.sqrt( arr[:,0]**2 + arr[:,1]**2 + arr[:,2]**2 )
    arr[:,0] /= lens
    arr[:,1] /= lens
    arr[:,2] /= lens                
    return arr

def myExtend(l,*args):
	for e in args:
		l.append(e)

def genVertices(size):
	(CX,CY,CZ) = size
	d = 1.0
	vertices = []
	for x in xrange(CX+1):
		for y in xrange(CY+1):
			for z in xrange(CZ+1):
				myExtend( vertices, x  , y  , z   ) # 000 - 0
				#myExtend( vertices, x  , y  , z+d ) # 001 - 1
				#myExtend( vertices, x  , y+d, z   ) # 010 - 2
				#myExtend( vertices, x  , y+d, z+d ) # 011 - 3
				#myExtend( vertices, x+d, y  , z   ) # 100 - 4
				#myExtend( vertices, x+d, y  , z+d ) # 101 - 5
				#myExtend( vertices, x+d, y+d, z   ) # 110 - 6
				#myExtend( vertices, x+d, y+d, z+d ) # 111 - 7
	return numpy.array(vertices,numpy.float32)

class Chunk:
	SIZE = (16,16,16)
	#VERTICES = genVertices(SIZE)

	def __init__(self):
		(x,y,z) = Chunk.SIZE
		self.voxels = [None]*x*y*z
		self.changed = True
		self.vbo = glGenBuffers(1)
		self.elements = 0

	def get(self,x,y,z):
		(CX,CY,CZ) = Chunk.SIZE
		n = CX*CY*z + CX*y + x
		return self.voxels[n]

	def set(self,x,y,z,aType):
		(CX,CY,CZ) = Chunk.SIZE
		n = CX*CY*z + CX*y + x
		self.voxels[n] = aType
		self.changed = True

	def update(self,shader):
		self.changed = False

		(CX,CY,CZ) = Chunk.SIZE

		vertices = []
		d = 1
		for x in xrange(CX):
			for y in xrange(CY):
				for z in xrange(CZ):
					# the python way is always mysterious and unknown
					aType = self.get(x,y,z)

					# Empty block?
					if aType in (0,None):
						continue
					
					# view from negative x
					myExtend( vertices, x  , y  , z  , aType,    +1.0,  0.0,  0.0 )
					myExtend( vertices, x  , y  , z+d, aType,    +1.0,  0.0,  0.0 )
					myExtend( vertices, x  , y+d, z+d, aType,    +1.0,  0.0,  0.0 )
					myExtend( vertices, x  , y+d, z+d, aType,    +1.0,  0.0,  0.0 )
					myExtend( vertices, x  , y+d, z  , aType,    +1.0,  0.0,  0.0 )
					myExtend( vertices, x  , y  , z  , aType,    +1.0,  0.0,  0.0 )

					# view from positive x
					myExtend( vertices, x+d, y  , z  , aType,    -1.0,  0.0,  0.0 )
					myExtend( vertices, x+d, y+d, z+d, aType,    -1.0,  0.0,  0.0 )
					myExtend( vertices, x+d, y  , z+d, aType,    -1.0,  0.0,  0.0 )
					myExtend( vertices, x+d, y+d, z+d, aType,    -1.0,  0.0,  0.0 )
					myExtend( vertices, x+d, y  , z  , aType,    -1.0,  0.0,  0.0 )
					myExtend( vertices, x+d, y+d, z  , aType,    -1.0,  0.0,  0.0 )

					# view from negative y
					myExtend( vertices, x+d, y  , z  , aType,     0.0, +1.0,  0.0 )
					myExtend( vertices, x+d, y  , z+d, aType,     0.0, +1.0,  0.0 )
					myExtend( vertices, x  , y  , z+d, aType,     0.0, +1.0,  0.0 )
					myExtend( vertices, x  , y  , z+d, aType,     0.0, +1.0,  0.0 )
					myExtend( vertices, x  , y  , z  , aType,     0.0, +1.0,  0.0 )
					myExtend( vertices, x+d, y  , z  , aType,     0.0, +1.0,  0.0 )

					# view from positive y
					myExtend( vertices, x+d, y+d, z  , aType,     0.0, -1.0,  0.0 )
					myExtend( vertices, x  , y+d, z+d, aType,     0.0, -1.0,  0.0 )
					myExtend( vertices, x+d, y+d, z+d, aType,     0.0, -1.0,  0.0 )
					myExtend( vertices, x  , y+d, z+d, aType,     0.0, -1.0,  0.0 )
					myExtend( vertices, x+d, y+d, z  , aType,     0.0, -1.0,  0.0 )
					myExtend( vertices, x  , y+d, z  , aType,     0.0, -1.0,  0.0 )

					# view from negative z
					myExtend( vertices, x  , y  , z  , aType,     0.0,  0.0, +1.0 )
					myExtend( vertices, x  , y+d, z  , aType,     0.0,  0.0, +1.0 )
					myExtend( vertices, x+d, y+d, z  , aType,     0.0,  0.0, +1.0 )
					myExtend( vertices, x+d, y+d, z  , aType,     0.0,  0.0, +1.0 )
					myExtend( vertices, x+d, y  , z  , aType,     0.0,  0.0, +1.0 )
					myExtend( vertices, x  , y  , z  , aType,     0.0,  0.0, +1.0 )

					# view from positive z
					myExtend( vertices, x  , y  , z+d, aType,     0.0,  0.0, -1.0 )
					myExtend( vertices, x+d, y+d, z+d, aType,     0.0,  0.0, -1.0 )
					myExtend( vertices, x  , y+d, z+d, aType,     0.0,  0.0, -1.0 )
					myExtend( vertices, x+d, y+d, z+d, aType,     0.0,  0.0, -1.0 )
					myExtend( vertices, x  , y  , z+d, aType,     0.0,  0.0, -1.0 )
					myExtend( vertices, x+d, y  , z+d, aType,     0.0,  0.0, -1.0 )

		# #-----------------------------------------------------------------------

		# vertices = [
		# 			0.0, 0.0, 0.0, 1.0,    +1.0,  0.0,  0.0,
		# 			0.0, 0.0, 9.0, 1.0,    +1.0,  0.0,  0.0,
		# 			0.0, 9.0, 9.0, 1.0,    +1.0,  0.0,  0.0,
		# 			0.0, 9.0, 9.0, 1.0,    +1.0,  0.0,  0.0,
		# 			0.0, 9.0, 0.0, 1.0,    +1.0,  0.0,  0.0,
		# 			0.0, 0.0, 0.0, 1.0,    +1.0,  0.0,  0.0,


		# 			9.0, 0.0, 0.0, 1.0,    -1.0,  0.0,  0.0,
		# 			9.0, 9.0, 9.0, 1.0,    -1.0,  0.0,  0.0,
		# 			9.0, 0.0, 9.0, 1.0,    -1.0,  0.0,  0.0,
		# 			9.0, 9.0, 9.0, 1.0,    -1.0,  0.0,  0.0,
		# 			9.0, 0.0, 0.0, 1.0,    -1.0,  0.0,  0.0,
		# 			9.0, 9.0, 0.0, 1.0,    -1.0,  0.0,  0.0,


		# 			9.0, 0.0, 0.0, 1.0,     0.0, +1.0,  0.0,
		# 			9.0, 0.0, 9.0, 1.0,     0.0, +1.0,  0.0,
		# 			0.0, 0.0, 9.0, 1.0,     0.0, +1.0,  0.0,
		# 			0.0, 0.0, 9.0, 1.0,     0.0, +1.0,  0.0,
		# 			0.0, 0.0, 0.0, 1.0,     0.0, +1.0,  0.0,
		# 			9.0, 0.0, 0.0, 1.0,     0.0, +1.0,  0.0,


		# 			9.0, 9.0, 0.0, 1.0,     0.0, -1.0,  0.0,
		# 			0.0, 9.0, 9.0, 1.0,     0.0, -1.0,  0.0,
		# 			9.0, 9.0, 9.0, 1.0,     0.0, -1.0,  0.0,
		# 			0.0, 9.0, 9.0, 1.0,     0.0, -1.0,  0.0,
		# 			9.0, 9.0, 0.0, 1.0,     0.0, -1.0,  0.0,
		# 			0.0, 9.0, 0.0, 1.0,     0.0, -1.0,  0.0,


		# 			0.0, 0.0, 0.0, 1.0,     0.0,  0.0, +1.0,
		# 			0.0, 9.0, 0.0, 1.0,     0.0,  0.0, +1.0,
		# 			9.0, 9.0, 0.0, 1.0,     0.0,  0.0, +1.0,
		# 			9.0, 9.0, 0.0, 1.0,     0.0,  0.0, +1.0,
		# 			9.0, 0.0, 0.0, 1.0,     0.0,  0.0, +1.0,
		# 			0.0, 0.0, 0.0, 1.0,     0.0,  0.0, +1.0,


		# 			0.0, 0.0, 9.0, 1.0,     0.0,  0.0, -1.0,
		# 			9.0, 9.0, 9.0, 1.0,     0.0,  0.0, -1.0,
		# 			0.0, 9.0, 9.0, 1.0,     0.0,  0.0, -1.0,
		# 			9.0, 9.0, 9.0, 1.0,     0.0,  0.0, -1.0,
		# 			0.0, 0.0, 9.0, 1.0,     0.0,  0.0, -1.0,
		# 			9.0, 0.0, 9.0, 1.0,     0.0,  0.0, -1.0]

		#-----------------------------------------------------------------------

		self.elements = len(vertices)
		vert = numpy.array(vertices,numpy.float32)

		self.loc = shader.bindAttribute("position",vert,self.vbo,(4,GL_FLOAT,False,7*4,ctypes.c_void_p(0)))
		self.norm = shader.bindAttribute("normal",vert,self.vbo,(3,GL_FLOAT,False,7*4,ctypes.c_void_p(4)))

	def render(self,shader):
		if self.changed:
			self.update(shader)
		
		#if this chunk is empty, we don't need to draw it
		if self.elements == 0:
			return
		
		glEnableVertexAttribArray(self.loc)
		glEnableVertexAttribArray(self.norm)
		glDrawArrays(GL_TRIANGLES,0,self.elements/7)
		glDisableVertexAttribArray(self.loc)
		glDisableVertexAttribArray(self.norm)