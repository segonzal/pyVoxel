#version 120 
attribute vec4 position;

void main(void) {
	gl_Position = gl_ModelViewProjectionMatrix * vec4(position.xyz, 1);
}