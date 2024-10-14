#version 330 compatibility


uniform vec4 Global_ambient;
uniform vec4 Light_ambient;
uniform vec4 Light_diffuse;
uniform vec4 Light_specular;
uniform float Material_shininess;
uniform vec4 Material_ambient;
uniform vec4 Material_diffuse;
uniform vec4 Material_specular;

uniform sampler2D tex;

in vec3 vN;
in vec3 vL;
in vec3 vE;
in vec2 vST;


void main() {
	vec3 Normal = normalize(vN);
	vec3 Light = normalize(vL);
	vec3 Eye = normalize(vE);
	
	vec4 ambient = Light_ambient * Material_ambient;
	
	float d = max(dot(Normal, Light), 0);
	vec4 diffuse = Light_diffuse * d * Material_diffuse;
	
	float s = 0;
	vec3 ref = normalize( reflect( -Light, Normal ) );
	s = pow( max( dot(Eye,ref),0. ), Material_shininess );	
	vec4 specular = Light_specular * s * Material_specular;
	
	//gl_FragColor = ambient + diffuse + specular;
	
	
	float attenuation = 1.0 / (1.0 + 0.00001 * pow(length(vL), 2));
	
	gl_FragColor = ambient + attenuation*(diffuse + specular) + 0.6*texture2D(tex, vST);;
	
}