from OpenGL.GL import *
import numpy as np

class Shader:
	def __init__(self,vertex,fragment):
		self.code = (vertex,fragment)
		self.program = None

	def compile(self):
		vertex,fragment = self.code
		# request program and shader slots from GPU
		self.program = glCreateProgram()
		vertexShader = glCreateShader(GL_VERTEX_SHADER)
		fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)

		#set shaders source
		glShaderSource(vertexShader,vertex)
		glShaderSource(fragmentShader,fragment)

		#compile shaders
		glCompileShader(vertexShader)
		glCompileShader(fragmentShader)

		#attach shader objects to the program
		glAttachShader(self.program,vertexShader)
		glAttachShader(self.program,fragmentShader)

		#build program
		glLinkProgram(self.program)

		#get rid of shaders (needed no more)
		glDetachShader(self.program,vertexShader)
		glDetachShader(self.program,fragmentShader)

	def use(self):
		#make the program the default
		glUseProgram(self.program)

	def bindAttribute(self,att_name,data,buffer,(size,type,normalized,stride,offset)):
		#http://wiki.lwjgl.org/index.php?title=GLSL_Tutorial:_Communicating_with_Shaders	

		loc = glGetAttribLocation(self.program, att_name)
		
		glEnableVertexAttribArray(loc)
		
		glBindBuffer(GL_ARRAY_BUFFER, buffer)
		glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)

		glVertexAttribPointer(loc, size, type, normalized, stride, offset)
		
		glDisableVertexAttribArray(loc)

		return loc

	def bindUniforms(self,uni_name,type,*value):
		# http://pyopengl.sourceforge.net/documentation/manual-3.0/glUniform.html
		loc = glGetUniformLocation(self.program, uni_name)
		if type == '1f':
			glUniform1f(loc, value[0])
		elif type == '2f':
			glUniform2f(loc, value[0], value[1])
		elif type == '3f':
			glUniform3f(loc, value[0], value[1], value[2])
		elif type == '4f':
			glUniform4f(loc, value[0], value[1], value[2], value[3])
		elif type == '1i':
			glUniform1i(loc, value[0])
		elif type == '2i':
			glUniform2i(loc, value[0], value[1])
		elif type == '3i':
			glUniform2i(loc, value[0], value[1], value[2])
		elif type == '4i':
			glUniform2i(loc, value[0], value[1], value[2], value[3])
		else:
			raise ValueError("Unknown type %s" % type)

def shaderFromFile(vertex,fragment):
	v = open(vertex,'r')
	v_shader = ""
	for line in v:
		v_shader += line
	v.close()

	f = open(fragment,'r')
	f_shader = ""
	for line in f:
		f_shader += line
	f.close()
	return Shader(v_shader,f_shader)
