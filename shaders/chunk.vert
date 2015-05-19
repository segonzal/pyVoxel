#version 330

layout (location = 0 ) in vec3 position;
layout (location = 1 ) in vec4 color;
layout (location = 2 ) in vec3 normal;

uniform vec3 translate;

out vec3 myPosition;
out vec3 myNormal;
out vec4 myColor;

void main(){
	myPosition = translate + position;
	myNormal = normal;
	myColor = color;

	gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * vec4(myPosition,1.0);
} 