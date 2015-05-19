from View import *
from Controller import *
from SuperChunk import *
from Chunk import *
from Shader import *
import random

def main():
	view = View()
	controller = Controller()

	chunk_shader = shaderFromFile("shaders/chunk.vert","shaders/chunk.frag")
	chunk_shader.compile()
	chunk_shader.use()

	chunk_shader.bindUniforms("lightPos",'3f',100.0,100.0,100.0)
	chunk_shader.bindUniforms("lightColor",'3f',1.0,1.0,1.0)

	view.shader = chunk_shader

	chunk = SuperChunk()
	# for x in range(16):
	# 	for y in range(16):
	# 		for z in range(16):
	# 			if random.randint(0,10) != 0: continue
	# 			chunk.set(x,y,z,random.randint(1,4))
	chunk.set(0,0,0,1)
	chunk.set(22,5,0,1)

	controller.model = view.model = chunk
	controller.camera = view.camera = Camera()

	while controller.running:
		controller.update()
		view.update()

	controller.close()

if __name__ == '__main__':
	main()