from OpenGL.GL import *
from Chunk import *

class SuperChunk:
	SIZE = (16,16,16)
	def __init__(self):
		# guardo los chunks
		(SCX,SCY,SCZ) = SuperChunk.SIZE
		self.chunks = [None]*SCX*SCY*SCZ

	def get(self,x,y,z):
		(SCX,SCY,SCZ) = SuperChunk.SIZE
		(CX,CY,CZ) = Chunk.SIZE

		cx = x / CX
		cy = y / CY
		cz = z / CZ

		x %= CX
		y %= CY
		z %= CZ

		n = SCX*SCY*z + SCX*y + x
		if self.chunks[n] is None:
			return 0
		else:
			return self.chunks[n].get(x,y,z)

	def set(self,x,y,z,type):
		(SCX,SCY,SCZ) = SuperChunk.SIZE
		(CX,CY,CZ) = Chunk.SIZE
		cx = x / CX
		cy = y / CY
		cz = z / CZ

		x %= CX
		y %= CY
		z %= CZ

		n = SCX*SCY*cz + SCX*cy + cx
		if self.chunks[n] is None:
			pos = (cx*CX,cy*CY,cz*CZ)
			self.chunks[n] = Chunk(pos)
		self.chunks[n].set(x,y,z,type)

	def render(self,shader):
		(SCX,SCY,SCZ) = SuperChunk.SIZE
		(CX,CY,CZ) = Chunk.SIZE
		for x in xrange(SCX):
			for y in xrange(SCY):
				for z in xrange(SCZ):
					n = SCX*SCY*z + SCX*y + x
					if self.chunks[n] is None:
						continue
					self.chunks[n].render(shader)