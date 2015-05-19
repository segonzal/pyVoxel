from Chunk import *

class SuperChunk:
	SIZE = (16,16,16)
	def __init__(self):
		# guardo los chunks
		(SCX,SCY,SCZ) = SuperChunk.SIZE
		self.chunks = [None]*SCX*SCY*SCZ

	def delete(self):
		(SCX,SCY,SCZ) = SuperChunk.SIZE
		for x in xrange(SCX):
			for y in xrange(SCY):
				for z in xrange(SCZ):
					n = SCX*SCY*z + SCX*y + x
					self.chunks[n].delete()
					self.chunks[n] = None

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

		n = SCX*SCY*z + SCX*y + x
		if self.chunks[n] is None:
			self.chunks[n] = Chunk()

		self.chunks[n].set(x,y,z,type)

	def render(self,attribute_coord):
		(SCX,SCY,SCZ) = SuperChunk.SIZE
		for x in xrange(SCX):
			for y in xrange(SCY):
				for z in xrange(SCZ):
					n = SCX*SCY*z + SCX*y + x
					if self.chunks[n] is None:
						continue
					#glm::mat4 model = glm::translate(glm::mat4(1), glm::vec3(x * CX, y * CY, z * CZ));
            		# calculate the full MVP matrix here and pass it to the vertex shader
					self.chunks[n].render(attribute_coord)