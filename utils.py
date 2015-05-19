import numpy
import math
from OpenGL.GL import *

def perspectiveGL(fovy, aspect, near, far):
	fH = math.tan(fovy/360.0) * math.pi * near
	fW = fH * aspect
	glFrustum(-fW,fW,-fH,fH,near,far)

def createCube((xi,yi,zi),(xf,yf,zf),color=(1.0,1.0,1.0,1.0)):
	vertices = numpy.zeros(36, [("position", numpy.float32, 3),
								("color"   , numpy.float32, 4),
								("normal"  , numpy.float32, 3)])
	vertices["position"] = [
		(xi, yi, zi),
		(xi, yi, zf),
		(xi, yf, zf),
		(xi, yf, zf),
		(xi, yf, zi),
		(xi, yi, zi),

		(xf, yi, zi),
		(xf, yf, zf),
		(xf, yi, zf),
		(xf, yf, zf),
		(xf, yi, zi),
		(xf, yf, zi),

		(xf, yi, zi),
		(xf, yi, zf),
		(xi, yi, zf),
		(xi, yi, zf),
		(xi, yi, zi),
		(xf, yi, zi),

		(xf, yf, zi),
		(xi, yf, zf),
		(xf, yf, zf),
		(xi, yf, zf),
		(xf, yf, zi),
		(xi, yf, zi),

		(xi, yi, zi),
		(xi, yf, zi),
		(xf, yf, zi),
		(xf, yf, zi),
		(xf, yi, zi),
		(xi, yi, zi),

		(xi, yi, zf),
		(xf, yf, zf),
		(xi, yf, zf),
		(xf, yf, zf),
		(xi, yi, zf),
		(xf, yi, zf)]
	vertices["color"][:] = color
	vertices["normal"][ 0: 6] = (+1.0,  0.0,  0.0)
	vertices["normal"][ 6:12] = (-1.0,  0.0,  0.0)
	vertices["normal"][12:18] = ( 0.0, +1.0,  0.0)
	vertices["normal"][18:24] = ( 0.0, -1.0,  0.0)
	vertices["normal"][24:30] = ( 0.0,  0.0, +1.0)
	vertices["normal"][30:36] = ( 0.0,  0.0, -1.0)

	return vertices
def normalize(x,y,z):
	d = math.sqrt(x*x+y*y+z*z)
	x/=d
	y/=d
	z/=d
	return (x,y,z)

def translate(x,y,z):
	m = numpy.eye(4,dtype=numpy.float32)
	m[3,0] = x
	m[3,1] = y
	m[3,2] = z
	return m

def scale(x,y,z):
	m = numpy.eye(4,dtype=numpy.float32)
	m[0,0] = x
	m[1,1] = y
	m[2,2] = z
	return m

def identity():
	return numpy.eye(4,dtype=numpy.float32)

def rotate(angle,x,y,z):
	(x,y,z) = normalize(x,y,z)
	angle = math.radians(angle)

	c = math.cos(angle)
	s = math.sin(angle)
	C = 1-c

	m = numpy.eye(4,dtype=numpy.float32)
	m[0,0] = x*x*C + c
	m[1,0] = x*y*C - z*s
	m[2,0] = x*z*C + y*s

	m[0,1] = x*y*C+z*s
	m[1,1] = y*y*C+c
	m[2,1] = y*z*C-x*s

	m[0,2] = x*z*C-y*s
	m[1,2] = y*z*C+x*s
	m[2,2] = z*z*C+c
	return m