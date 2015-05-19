from View import *
from Controller import *
from SuperChunk import *
from Chunk import *
from Shader import *
import random

import cv2
def loadHGT(chunk):
	S = 16*8
	H = 16

	hmap = cv2.imread("hmap.png",cv2.CV_LOAD_IMAGE_GRAYSCALE)
	hmap = cv2.resize( hmap, (S,S) )
	(h,w) = hmap.shape
	for x in xrange(h):
		for z in xrange(w):
			y = hmap[x,z]*H/255
			for i in range(y):
				chunk.set(x,i,z,3)
			chunk.set(x,y,z,3)

def main():
	view = View()
	controller = Controller()
	controller.view = view

	chunk_shader = shaderFromFile("shaders/chunk.vert","shaders/chunk.frag")
	chunk_shader.compile()
	chunk_shader.use()
	chunk_shader.setAttribLocation(0,"position")
	chunk_shader.setAttribLocation(1,"color")
	chunk_shader.setAttribLocation(2,"normal")

	view.shader = chunk_shader

	view.reshape()

	chunk = SuperChunk()
	loadHGT(chunk)
	# for x in range(0,16):
	# 	for y in range(0,16):
	# 		for z in range(0,16):
	# 			if random.randint(0,10) != 0: continue
				
	# 			chunk.set(16+x,y,z,random.randint(1,4))

	# 			chunk.set(x,16+y,z,random.randint(1,4))

	# 			chunk.set(x,y,16+z,random.randint(1,4))

	# 			chunk.set(x,y,z,random.randint(1,4))

	controller.model = view.model = chunk
	view.camera = Camera()

	while controller.running:
		controller.update()
		view.update()

	controller.close()

if __name__ == '__main__':
	main()