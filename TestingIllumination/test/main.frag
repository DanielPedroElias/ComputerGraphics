#version 330 compatibility // Define a versão do OpenGL que estamos utilizando

// Função para gerar números aleatórios usando um vetor 2D como semente
float rand(vec2 co) {
    return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453); // Gera um valor entre 0 e 1
}

// Definição de variáveis de luz
uniform vec4 Global_ambient;    // Cor do ambiente global
uniform vec4 Light_ambient;     // Cor da luz ambiente
uniform vec4 Light_diffuse;     // Cor da luz difusa
uniform vec4 Light_specular;    // Cor da luz especular

// Definição de variáveis de material
uniform float Material_shininess;  // Brilho do material
uniform vec4 Material_specular;     // Cor especular do material
uniform vec4 Material_ambient;      // Cor ambiente do material
uniform vec4 Material_diffuse;      // Cor difusa do material

// Variáveis de entrada do shader
in vec2 vST;  // Coordenadas de textura
in vec3 vN;   // Vetor normal da superfície
in vec3 vL;   // Vetor direção da luz
in vec3 vE;   // Vetor direção do olho/câmera


void main() {
    vec3 Normal = normalize(vN); // Normaliza o vetor normal
    vec3 Light = normalize(vL);  // Normaliza o vetor de luz
    vec3 Eye = normalize(vE);    // Normaliza o vetor do olho

	// Cálculo da luz ambiente
    vec4 ambient = Light_ambient * Material_ambient;
	
    // Cálculo da luz difusa com base no ângulo entre a normal e a direção da luz
	float d = max(dot(Normal, Light), 0); 
    vec4 diffuse = Light_diffuse * d * Material_diffuse;

	// Cálculo da reflexão da luz
    vec3 ref = normalize(reflect(-Light, Normal));

    // Cálculo da luz especular com base na direção do olho e na reflexão
    float s = pow(max(dot(Eye, ref), 0.0), Material_shininess);
    vec4 specular = Light_specular * s * Material_specular;

    float attenuation = 1.0 / (1.0 + 0.0001 * pow(length(vL), 2));

    // Combina iluminação com a cor escolhida
   // gl_FragColor = (ambient + attenuation * (diffuse + specular));
    gl_FragColor = ambient + diffuse + specular;

}