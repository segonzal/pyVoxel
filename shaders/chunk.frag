#version 330

uniform vec3 lightPos;
uniform float flag;

in vec3 myPosition;
in vec3 myNormal;
in vec4 myColor;

void main(){
	if (flag){
		gl_FragColor = myColor;
	}
	else {
		vec3 lightDirection = normalize(myPosition.xyz-lightPos);
		
		float dProd = max(0.0, dot(myNormal.xyz, lightDirection));

		gl_FragColor = vec4(myColor.rgb * dProd, myColor.a);
	}
}