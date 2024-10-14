from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
import numpy as np
from PIL import Image

from OpenGL.arrays import vbo
from OpenGL.GL import shaders

T = 1
T2 = 1
T3 = 1

L = -5
L2 = 5
L3 = 0

# controles da camera
C = 0
C2 = 5
C3 = 40

CRota = 0
CRota2 = 5
CRota3 = 0
  



def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(C, C2, C3, CRota, CRota2, CRota3, 0.0, 1.0, 0.0)

    glPushMatrix()

    # Desenha carro
    glTranslatef(T, T2, T3)
    glColor3f(0.1, 0.0, 1.1)

    glUseProgram(carro_shader)

    # Atualiza a posição da luz
    configuraLuz()

    confiuraMaterial()

    obj_draw_shader(carro)

    glPopMatrix()

    glUseProgram(0)

    # Desenha esfera de luz
    glPushMatrix()
    glTranslatef(L, L2, L3)
    glutSolidSphere(0.8, 8, 8)
    glPopMatrix()
    
    desenhaEixos()

    glutSwapBuffers()

def obj_draw_shader(objeto):
    objs = list(objeto.materials.keys())    #Pega primeiro objeto do .obj
    vertices = objeto.materials[objs[0]].vertices
    vertices = np.array(vertices, dtype=np.float32).reshape(-1,6)
    vbo_objeto = vbo.VBO(vertices)
    
    vbo_objeto.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glVertexPointer(3, GL_FLOAT, 24, vbo_objeto+12)   #glVertexPointer(size, type, stride, pointer)
    glNormalPointer(GL_FLOAT, 24, vbo_objeto)         #glNormalPointer(type, stride, pointer)
    glDrawArrays(GL_TRIANGLES, 0, vertices.shape[0])
    vbo_objeto.unbind()
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)

   
# Função para desenhar um objeto com shader e textura (se fornecida)
def obj_draw_shaderTexture(objeto, shader_program, texture_ID=None):
    objs = list(objeto.materials.keys())    # Pega o primeiro material do objeto
    vertices = objeto.materials[objs[0]].vertices
    vertices = np.array(vertices, dtype=np.float32).reshape(-1, 8)  # Assumindo que temos tex_2, vn_3, v_3
    vbo_objeto = vbo.VBO(vertices)

    # Liga o VBO
    vbo_objeto.bind()

    # Ativa os estados necessários para usar os dados de vértices, normais e coordenadas de textura
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    # Define os ponteiros para os dados de vértices, normais e coordenadas de textura
    glVertexPointer(3, GL_FLOAT, 32, vbo_objeto + 20)  # 3 floats para os vértices (posição)
    glNormalPointer(GL_FLOAT, 32, vbo_objeto + 8)      # 3 floats para as normais
    glTexCoordPointer(2, GL_FLOAT, 32, vbo_objeto)     # 2 floats para coordenadas de textura

    # Se houver uma textura, ativa e aplica
    if texture_ID is not None:
        glActiveTexture(GL_TEXTURE0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_ID)
        glUniform1i(glGetUniformLocation(shader_program, 'tex'), 0)

    # Ativa o shader
    glUseProgram(shader_program)

    # Desenha o objeto
    glDrawArrays(GL_TRIANGLES, 0, vertices.shape[0])

    # Desativa o shader e estados
    glUseProgram(0)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)

    # Desvincula o VBO
    vbo_objeto.unbind()

def configuraLuz():
    glUniform4f( LIGTH_LOCATIONS['Global_ambient'], 0.01, 0.01, 0.01, 1.0 )
    glUniform3f( LIGTH_LOCATIONS['Light_location'], L,L2,L3 )
    glUniform4f( LIGTH_LOCATIONS['Light_ambient'], 0.2, 0.2, 0.2, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Light_diffuse'], 0.9, 0.9, 0.9, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Light_specular'], 0.9,0.9,0.9, 1.0 )
    
def confiuraMaterial():
    glUniform4f( LIGTH_LOCATIONS['Material_ambient'], .1,.1,.1, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Material_diffuse'], 0.1,0.1,0.9, 1 )
    glUniform4f( LIGTH_LOCATIONS['Material_specular'], 0.9,0.9,0.9, 1 )
    glUniform1f( LIGTH_LOCATIONS['Material_shininess'], 0.6*128.0 )

def desenhaEixos():

    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(10.0, 0.0, 0.0)
    glEnd()
    
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 10.0, 0.0)
    glEnd()
    
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 10.0)
    glEnd()
    
    
def camera(w, h):
   
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w/h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
def Keys(key, x, y):

    global T
    global T2
    global T3
    
    if(key == b'a'): 
        T -= 1
    elif(key == b'd'): 
        T += 1
    elif(key == b'w'): 
        T2 += 1
    elif(key == b's'): 
        T2 -= 1
    elif(key == b'q'): 
        T3 -= 1
    elif(key == b'e'): 
        T3 += 1

    global C
    global C2
    global C3
    global CRota

    # movimento da camera
    if (key == b'i'):
        C3 -= 1
    elif (key == b'k'):
        C3 += 1
    elif (key == b'j'):
        CRota -= 1
    elif (key == b'l'):
        CRota += 1
    elif (key == b'u'):
        C2 -= 1
    elif (key == b'o'):
        C2 += 1
    
    # movimentos de rotação da camera
    global CRota2
    global CRota3
    if (key == b','):
        C -= 1
    elif (key == b'.'):
        C += 1
    
def KeysEspecial(key, x, y):
    global L
    global L2
    global L3
    
    if(key == GLUT_KEY_LEFT ): 
        L -= 1 
    elif(key == GLUT_KEY_RIGHT ): 
        L += 1 
    elif(key == GLUT_KEY_DOWN ): 
        L2 -= 1
    elif(key == GLUT_KEY_UP ): 
        L2 += 1 
    elif(key == GLUT_KEY_PAGE_UP ): 
        L3 -= 1 
        
    elif(key == GLUT_KEY_PAGE_DOWN ): 
        L3 += 1         
    print(L3)

def animacao(value):
    glutPostRedisplay()
    glutTimerFunc(30, animacao,1)
  

# Função de inicialização (setup inicial)
def init():
    glClearColor(0.3, 0.3, 0.3, 0.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)

    # Carrega e compila shaders
    vertexShader = shaders.compileShader(open('carro.vert', 'r').read(), GL_VERTEX_SHADER)
    fragmentShader = shaders.compileShader(open('carro.frag', 'r').read(), GL_FRAGMENT_SHADER)

    global carro_shader
    carro_shader = glCreateProgram()
    glAttachShader(carro_shader, vertexShader)
    glAttachShader(carro_shader, fragmentShader)
    glLinkProgram(carro_shader)

    # Define variáveis de iluminação no shader
    global LIGTH_LOCATIONS
    LIGTH_LOCATIONS = {
        'Global_ambient': glGetUniformLocation(carro_shader, 'Global_ambient'),
        'Light_ambient': glGetUniformLocation(carro_shader, 'Light_ambient'),
        'Light_diffuse': glGetUniformLocation(carro_shader, 'Light_diffuse'),
        'Light_location': glGetUniformLocation(carro_shader, 'Light_location'),
        'Light_specular': glGetUniformLocation(carro_shader, 'Light_specular'),
        'Material_ambient': glGetUniformLocation(carro_shader, 'Material_ambient'),
        'Material_diffuse': glGetUniformLocation(carro_shader, 'Material_diffuse'),
        'Material_shininess': glGetUniformLocation(carro_shader, 'Material_shininess'),
        'Material_specular': glGetUniformLocation(carro_shader, 'Material_specular'),
    }

    global TEX_LOCATIONS
    TEX_LOCATIONS = {
        'tex': glGetAttribLocation(carro_shader, 'tex')
    }

    # Carregar a textura do Mario
    global mario_ID
    mario_img = Image.open('mario.png')
    w, h, mario_img = mario_img.size[0], mario_img.size[1], mario_img.tobytes("raw", "RGB", 0, -1)
    mario_ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, mario_ID)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, w, h, GL_RGB, GL_UNSIGNED_BYTE, mario_img)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1920, 1080)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Cubo")
init()
carro = pywavefront.Wavefront("mario2.obj")
glutDisplayFunc(display)
glutReshapeFunc(camera)
glutTimerFunc(30,animacao,1)
glutSpecialFunc(KeysEspecial)
glutKeyboardFunc(Keys)
glutMainLoop()
 