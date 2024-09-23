from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
import numpy as np


from OpenGL.arrays import vbo
from OpenGL.GL import shaders

T = 1 # mov no eixo x
T2 = 1 # mov no eixo y
T3 = 1 # mov no eixo z

L, L2, L3 = -5.0, 10.0, 0.0

camx, camy, camz = 0.0, 5.0, 20.0 # posicao da camera

# Variáveis para o shader
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


# Variáveis para o shader
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # movimenta a camera
    global camx, camy, camz
    if T > camx + 12 :
        camx += 1
    elif T < camx - 12:
        camx -= 1
    gluLookAt(camx , camy, camz, # eye posicao do olho
                camx,camy, 0.0, # center ponto para o qual a camera aponta
                0.0, 1.0, 0.0) # up vetor que indica a orientacao da camera

    glPushMatrix()

    #Ações em todo o carro
    glTranslatef(T, T2, T3)
    # Escala do carro
    glScalef(0.5, 0.5, 0.5)  #glScalef(tamanho_x, tamanho_y, tamanho_z)

    glPushMatrix()
      
    glUseProgram(carro_shader)


    corObj = (0.5, 0.0, 0.0, 1) # cor do objeto (branco)
    glUniform4f( LIGTH_LOCATIONS['Material_ambient'], .1,.1,.1, 1.0 ) # material ambiente
    glUniform4f( LIGTH_LOCATIONS['Material_diffuse'],*corObj ) # material difuso 
    glUniform4f( LIGTH_LOCATIONS['Material_specular'], 0.9,0.9,0.9, 1) # material especular
    glUniform1f( LIGTH_LOCATIONS['Material_shininess'], 0.6*128.0 ) # brilho do material
    
    glUniform4f( LIGTH_LOCATIONS['Global_ambient'], 0.1, 0.1, 0.1, 1.0 )    #  luz ambiente global 

    glUniform3f( LIGTH_LOCATIONS['Light_location'], L, L2, L3 ) # posicao da luz
    light_color = (1.0, 1.0, 0.0, 1.0) # cor da luz
    glUniform4f( LIGTH_LOCATIONS['Light_diffuse'], *light_color) # luz difusa
    glUniform4f( LIGTH_LOCATIONS['Light_specular'], *light_color) # luz especular
    # * é usado para "desempacotar" a tupla, ou seja, ele separa os elementos da tupla e os passa como argumentos individuais para a função
    
    
    obj_draw_shader(carro)
    
    glPopMatrix()

    

    glDisableClientState(GL_VERTEX_ARRAY) # desabilita o uso de arrays de vertices
    glDisableClientState(GL_NORMAL_ARRAY) # desabilita o uso de arrays de normais

    glPopMatrix()


    glUseProgram(0)
    
    glPushMatrix()
    # deseha a esfera
    glTranslatef(L, L2, L3) # translada a esfera
    glColor4f(*light_color)  # Define a cor da esfera como a cor da luz
    glutSolidSphere(0.8, 16, 8) # desenha a esfera glutSolidSphere(raio, slices, stacks)
    glPopMatrix() # finaliza a esfera

 
    #Eixos
    # eixo x cor vermelha
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(20.0, 0.0, 0.0)
    glEnd()
    # eixo y cor verde
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 20.0, 0.0)
    glEnd()
    # eixo z cor azul
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 20.0)
    glEnd()
    
    


    glutSwapBuffers()

def resize(w, h):
   
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w/h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    global camx, camy, camz

    gluLookAt(camx , camy, camz, # eye posicao do olho
                0.0, 5.0, 0.0, # center ponto para o qual a camera aponta
                0.0, 1.0, 0.0) # up vetor que indica a orientacao da camera
    


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
    
def KeysEspecial(key, x, y):
    global L
    global L2
    global L3
    
    if(key == GLUT_KEY_LEFT ): 
        L -= 1 
    elif(key == GLUT_KEY_RIGHT ): 
        L += 1 
    elif(key == GLUT_KEY_UP ): 
        L2 -= 1
    elif(key == GLUT_KEY_DOWN ): 
        L2 += 1 
    elif(key == GLUT_KEY_PAGE_UP ): 
        L3 -= 1 
    elif(key == GLUT_KEY_PAGE_DOWN ): 
        L3 += 1         
       
def animacao(value):
    glutPostRedisplay()
    glutTimerFunc(30, animacao,1)
    
    


  

def init():
    glClearColor (0.3, 0.3, 0.3, 0.0) # cor de fundo
    glShadeModel( GL_SMOOTH ) # tipo de sombreamento
    glClearColor( 0.0, 0.0, 0.0, 1.0 ) # cor de fundo
    glClearDepth( 1.0 ) # valor do z-buffer
    glEnable( GL_DEPTH_TEST ) # ativa o z-buffer
    glDepthFunc( GL_LEQUAL ) # tipo de teste do z-buffer
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST ) # correcao de perspectiva

    glDepthFunc( GL_LEQUAL )
    glEnable( GL_DEPTH_TEST )
    
    vertexShader = shaders.compileShader(open('carro.vert', 'r').read(), GL_VERTEX_SHADER)
    fragmentShader = shaders.compileShader(open('carro.frag', 'r').read(), GL_FRAGMENT_SHADER)

    global carro_shader
    carro_shader = glCreateProgram()
    glAttachShader(carro_shader, vertexShader) 
    glAttachShader(carro_shader, fragmentShader)
    glLinkProgram(carro_shader)
    
    global LIGTH_LOCATIONS
    LIGTH_LOCATIONS = {
        'Global_ambient': glGetUniformLocation( carro_shader, 'Global_ambient' ),
        'Light_ambient': glGetUniformLocation( carro_shader, 'Light_ambient' ),
        'Light_diffuse': glGetUniformLocation( carro_shader, 'Light_diffuse' ),
        'Light_location': glGetUniformLocation( carro_shader, 'Light_location' ),
        'Light_specular': glGetUniformLocation( carro_shader, 'Light_specular' ),
        'Material_ambient': glGetUniformLocation( carro_shader, 'Material_ambient' ),
        'Material_diffuse': glGetUniformLocation( carro_shader, 'Material_diffuse' ),
        'Material_shininess': glGetUniformLocation( carro_shader, 'Material_shininess' ),
        'Material_specular': glGetUniformLocation( carro_shader, 'Material_specular' ),
        'Object_color': glGetUniformLocation(carro_shader, 'Object_color')

    }   
    
    global ATTR_LOCATIONS
    ATTR_LOCATIONS = {
        'Vertex_position': glGetAttribLocation( carro_shader, 'Vertex_position' ),
        'Vertex_normal': glGetAttribLocation( carro_shader, 'Vertex_normal' )
    }

    

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1920, 1080)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Cubo")

init()
carro = pywavefront.Wavefront("disco.obj")
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
glutSpecialFunc(KeysEspecial)
glutKeyboardFunc(Keys)
glutMainLoop()