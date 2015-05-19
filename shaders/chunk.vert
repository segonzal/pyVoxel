attribute vec4 position;
attribute vec3 normal;

uniform vec3 light;

varying vec3 Normal;
varying vec3 FragPos;
varying float texcoord;

void main(){
	texcoord = position.w;

    gl_Position = gl_ModelViewProjectionMatrix * vec4(position.xyz, 1.0);
    vec4 fp = gl_ModelViewMatrix * vec4(position.xyz,1.0);//vec3(gl_ModelView * vec4(position.xyz, 1.0));
    FragPos = fp.xyz;
    Normal = normal;//mat3(transpose(inverse(gl_ModelView))) * normal;  
} 