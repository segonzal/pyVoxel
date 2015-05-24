import numpy as np

def lerp(a,b,x):
	return (1-x)*a + b*x

def groundGradient(mat,size):
	(x,y,z) = size

	for i in xrange(y):
		a[:,i,:] = i*1.0/(y-1)

def threshold(mat,threshold,low=0,high=1):
	idx = mat[:,:,:] > threshold
	mat[:,:,:] = low
	mat[idx] = high

if __name__ == '__main__':
	(x,y,z) = (5,5,5)
	a = np.zeros((x,y,z))

	groundGradient(a,(x,y,z))
	threshold(a,0.5)

	print a