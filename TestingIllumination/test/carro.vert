#version 330 compatibility

uniform vec3 Light_location;

out vec3 vN;	//Vetor normal
out vec3 vL;	//Vetor do ponto para a luz
out vec3 vE; 	//Vetor do ponto para o olho da camera
out vec2 vST;



void main() {
	vST = gl_MultiTexCoord0.st;
	
	vec4 ECPosition = gl_ModelViewMatrix * gl_Vertex;   //Posicao do olho
	
	vN = normalize(gl_NormalMatrix * gl_Normal);		// atualiza a normal
	
	vL = vec3(gl_ModelViewMatrix  * vec4(Light_location, 0.0)) - ECPosition.xyz;
	
	vE = vec3(0.,0.,0.) - ECPosition.xyz;
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}