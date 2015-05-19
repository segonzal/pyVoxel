from View import *
from Controller import *
from Chunk import *

from Shader import *
import random
def main():
	controller = Controller()
	view = View()

	chunk_shader = shaderFromFile("shaders/chunk.vert","shaders/chunk.frag")
	chunk_shader.compile()
	view.shader = chunk_shader

	chunk = Chunk()
	for x in range(16):
		for y in range(16):
			for z in range(16):
				chunk.set(x,y,z,random.randint(1,16))

	controller.model = view.model = chunk

	while controller.running:
		controller.update()
		view.update()

	controller.close()

if __name__ == '__main__':
	main()