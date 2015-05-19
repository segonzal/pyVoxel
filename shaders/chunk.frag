#version 330

uniform vec3 lightPos;

in vec3 myPosition;
in vec3 myNormal;
in vec4 myColor;

void main(){
	vec3 lightDirection = normalize(lightPos-myPosition.xyz);
	
	float dProd = max(0.0, dot(myNormal.xyz, lightDirection));

    gl_FragColor = vec4(myColor.rgb * dProd, myColor.a);
}