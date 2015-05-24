from View import *
from Controller import *
from SuperChunk import *
from Chunk import *
from Shader import *
import random
from OpenSimplexNoise import *

import cv2
def loadHGT(chunk):
	S = 16*5#S = 16*10
	H = 16#H = 16*2

	hmap = cv2.imread("hmap.png",cv2.CV_LOAD_IMAGE_GRAYSCALE)
	hmap = cv2.resize( hmap, (S,S) )
	(h,w) = hmap.shape
	for x in xrange(h):
		for z in xrange(w):
			y = (255-hmap[x,z])*H/255
			for i in range(y):
				chunk.set(x,i,z,3)
			chunk.set(x,y,z,2)

def loadWorld(chunk):
	S = 16*8
	H = 16
	noise = OpenSimplexNoise(345789876543456787654l)
	FEATURE_SIZE = 2.0
	hmap = cv2.imread("hmap.png",cv2.CV_LOAD_IMAGE_GRAYSCALE)
	hmap = cv2.resize( hmap, (S,S) )
	(h,w) = hmap.shape
	for x in xrange(h):
		for z in xrange(w):
			y = hmap[x,z]*H/255
			chunk.set(x,y,z,2)
			for i in range(y):
				value = noise.eval(x/FEATURE_SIZE,i/FEATURE_SIZE,z/FEATURE_SIZE)
				if value < 0.5:
					chunk.set(x,i,z,3)
				else:
					chunk.set(x,i,z,1)

def random(chunk):
	(h,w,l) = 16*8,16*8,16
	noise = OpenSimplexNoise(345789876543456787654l)
	FEATURE_SIZE = 2.0
	for x in xrange(h):
		for z in xrange(w):
			for y in xrange(l):
				value = noise.eval(x/FEATURE_SIZE,y/FEATURE_SIZE,z/FEATURE_SIZE)
				if value < 0.5:
					chunk.set(x,y,z,2)

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
	#loadWorld(chunk)
	#random(chunk)
	loadHGT(chunk)

	controller.model = view.model = chunk
	view.camera = Camera(25,15,25)

	while controller.running:
		controller.update()
		view.update()

	controller.close()

if __name__ == '__main__':
	main()