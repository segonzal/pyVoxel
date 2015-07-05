from OpenGL.GL import *
import numpy as np
import utils

class Shader:
	def __init__(self,vertex,fragment):
		self.code = (vertex,fragment)
		self.program = None
		self.locations = {}

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

	def getAttribLocation(self,att_name):
		if self.locations.has_key(att_name):
			return self.locations[att_name]
		loc = glGetAttribLocation(self.program, att_name)

		if loc < 0:
			raise ValueError("getAttribLocation error for attribute "+att_name+": attribute not found")

		self.locations[att_name] = loc
		return loc

	def setAttribLocation(self,index,att_name):
		if self.locations.has_key(att_name):
			raise ValueError("setAttribLocation error for attribute "+att_name+": attribute already exists")
		glBindAttribLocation(self.program,index,att_name)
		self.locations[att_name] = index

	def bufferData(self, data, buffer):
		glBindBuffer(GL_ARRAY_BUFFER, buffer)
		glBufferData(GL_ARRAY_BUFFER, data, GL_DYNAMIC_DRAW)

	def attribute(self,att_name,size,type,normalized,stride,offset):
		"""
		attribute(name,size,type,normalized,stride,offset)

		name: name of the attribute
		size: Specifies the number of components per generic vertex attribute.
			  Must be 1, 2, 3, 4.
		type: Specifies the data type of each component in the array.
			  GL_BYTE, GL_UNSIGNED_BYTE, GL_SHORT, GL_UNSIGNED_SHORT, GL_INT,
			  GL_UNSIGNED_INT, GL_FLOAT and GL_DOUBLE.
		normalized: Specifies whether fixed-point data values should be normalized (True) or
			  converted directly as fixed-point values (False)
		stride: Specifies the byte offset between consecutive generic vertex attributes.
		offset: Specifies a offset of the first component of the first generic vertex attribute in the
				array in the data store of the buffer currently bound to the GL_ARRAY_BUFFER target.
		"""
		# https://www.opengl.org/sdk/docs/man/html/glVertexAttribPointer.xhtml
		loc = self.getAttribLocation(att_name)
		
		glEnableVertexAttribArray(loc)

		glVertexAttribPointer(loc, size, type, normalized, stride, ctypes.c_void_p(offset))
		
		glDisableVertexAttribArray(loc)

	def uniform(self,uni_name,type,*value):
		"""
		uniform(name,type, value ... )

		name: name of the uniform
		type: 1f, 2f, 3f, 4f, 1i, 2i, 3i, 4i, 22f, 23f, 24f, 33f, 32f, 34f, 44f, 42f, 43f
		*value:
		For the scalar commands:
			[0][1][2][3] Specifies the new values to be used for the specified uniform variable.
						 ( v0, v1, v2, v3 )
		For the matrix array commands:
			[0] Specifies the number of elements that are to be modified.
				This should be 1 if the targeted uniform variable is not an array, and 1 or more if it is an array.
				( count )
			[1] Specifies whether to transpose the matrix as the values are loaded into the uniform variable.
				( transpose )
			[2] Specifies a pointer to an array of count values that will be used to update the specified uniform variable.
				( value )
		"""
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

		# for matrices:  location , count , transpose , value
		elif type == '22f':
			glUniformMatrix2fv(loc,value[0],value[1],value[2])
		elif type == '23f':
			glUniformMatrix2x3fv(loc,value[0],value[1],value[2])
		elif type == '24f':
			glUniformMatrix2x4fv(loc,value[0],value[1],value[2])
		elif type == '33f':
			glUniformMatrix3fv(loc,value[0],value[1],value[2])
		elif type == '32f':
			glUniformMatrix3x2fv(loc,value[0],value[1],value[2])
		elif type == '34f':
			glUniformMatrix3x4fv(loc,value[0],value[1],value[2])
		elif type == '44f':
			glUniformMatrix4fv(loc,value[0],value[1],value[2])
		elif type == '42f':
			glUniformMatrix4x2fv(loc,value[0],value[1],value[2])
		elif type == '43f':
			glUniformMatrix4x3fv(loc,value[0],value[1],value[2])
		
		else:
			raise ValueError("Unknown type " + type)

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
