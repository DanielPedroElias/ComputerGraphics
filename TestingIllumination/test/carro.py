from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
import numpy as np


from OpenGL.arrays import vbo
from OpenGL.GL import shaders

T = 1
T2 = 1
T3 = 1

L = 3
L2 = 1
L3 = 1


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



def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    
      
    vertices = roda.materials['Default_OBJ'].vertices
    vertices = np.array(vertices, dtype=np.float32).reshape(-1,6)
    vbo_roda = vbo.VBO(vertices)

    

    glPushMatrix()
    #Ações em todo o carro
    #glRotatef(T, 0.0, 1.0, 0.0)
    #glScalef(T, T2, T3)
    
    glPushMatrix()
    #Corpo do carro
    glTranslatef(T, T2, T3)
    glColor3f(0.1, 0.0, 1.1)
    #visualization.draw(carro)
    
    #glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, vertices)
    #glEnableVertexAttribArray(0)
    
    glUseProgram(carro_shader)
    
    
    glUniform4f( LIGTH_LOCATIONS['Global_ambient'], 0.1, 0.1, 0.1, 1.0 )
    glUniform3f( LIGTH_LOCATIONS['Light_location'], -5.0, 5.0, 0.0 )
    glUniform4f( LIGTH_LOCATIONS['Light_ambient'], 0.2, 0.2, 0.2, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Light_diffuse'], 0.9, 0.9, 0.9, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Light_specular'], 0.9,0.9,0.9, 1.0 )
    
    glUniform4f( LIGTH_LOCATIONS['Material_ambient'], .1,.1,.1, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Material_diffuse'], 0.1,0.1,0.9, 1 )
    glUniform4f( LIGTH_LOCATIONS['Material_specular'], 0.9,0.9,0.9, 1 )
    glUniform1f( LIGTH_LOCATIONS['Material_shininess'], 0.6*128.0 )
    
        
    obj_draw_shader(carro)
    
    glPopMatrix()

    glPushMatrix()

    #Mario 
    glTranslatef(L, L2, L3)
    glColor3f(0.1, 0.0, 1.1)
    #visualization.draw(mario)

    glUseProgram(carro_shader)

    glUniform4f( LIGTH_LOCATIONS['Global_ambient'], 0.1, 0.1, 0.1, 1.0 )
    glUniform3f( LIGTH_LOCATIONS['Light_location'], -5.0, 5.0, 0.0 )
    glUniform4f( LIGTH_LOCATIONS['Light_ambient'], 0.2, 0.2, 0.2, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Light_diffuse'], 0.9, 0.9, 0.9, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Light_specular'], 0.9,0.9,0.9, 1.0 )
    
    glUniform4f( LIGTH_LOCATIONS['Material_ambient'], .1,.1,.1, 1.0 )
    glUniform4f( LIGTH_LOCATIONS['Material_diffuse'], 0.9,0.1,0.1, 1 )
    glUniform4f( LIGTH_LOCATIONS['Material_specular'], 0.9,0.9,0.9, 1 )
    glUniform1f( LIGTH_LOCATIONS['Material_shininess'], 0.6*128.0 )

    obj_draw_shader(mario)

    glPopMatrix()


    

    vbo_roda.bind() # Vincula o VBO
    glVertexPointer(3, GL_FLOAT, 24, vbo_roda+12)  #glVertexPointer(size, type, stride, pointer)
    glNormalPointer(GL_FLOAT, 24, vbo_roda)     
    
    glUniform4f( LIGTH_LOCATIONS['Material_diffuse'], 0.4,0.4,0.4, 1 )            
                
    glPushMatrix()
    #glColor3f(1.0, 0.1, 0.1)
    glTranslatef(1.2, 1.0, 3.0)
    #glRotatef(T2, 1.0, 0.0, 0.0)
    #visualization.draw(roda)
    glDrawArrays(GL_TRIANGLES, 0, vertices.shape[0]) # glDrawArrays(mode, first, count)
    glPopMatrix()

    glPushMatrix()
    #glColor3f(1.0, 0.1, 0.1)
    glTranslatef(-1.2, 1.0, 3.0)
    #glRotatef(T2, 1.0, 0.0, 0.0)
    #visualization.draw(roda)
    glDrawArrays(GL_TRIANGLES, 0, vertices.shape[0])
    glPopMatrix()

    glPushMatrix()
    #glColor3f(1.0, 0.1, 0.1)
    glTranslatef(1.2, 1.0, -3.0)
    glRotatef(T, 0.0, 1.0, 0.0)
    #glRotatef(T2, 1.0, 0.0, 0.0)
    #visualization.draw(roda)
    glDrawArrays(GL_TRIANGLES, 0, vertices.shape[0])
    glPopMatrix()

    glPushMatrix()
    #glColor3f(1.0, 0.1, 0.1)
    glTranslatef(-1.2, 1.0, -3.0)
    glRotatef(T, 0.0, 1.0, 0.0)
    #glRotatef(T2, 1.0, 0.0, 0.0)
    #visualization.draw(roda)
    glDrawArrays(GL_TRIANGLES, 0, vertices.shape[0])
    glPopMatrix()
    
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)

    glPopMatrix()
    
    vbo_roda.unbind()
    
    glUseProgram(0)
    
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
    
    glPushMatrix()
    glTranslatef(-5.0, 5.0, 0.0)
    glutSolidSphere(0.8, 8, 8)
    glPopMatrix()
  


    glutSwapBuffers()
    

def resize(w, h):
   
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w/h, 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    
    gluLookAt(0.0, 5.0, 100.0, # eye posicao do olho
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
    glClearColor (0.3, 0.3, 0.3, 0.0)
    glShadeModel( GL_SMOOTH )
    glClearColor( 0.0, 0.0, 0.0, 1.0 )
    glClearDepth( 1.0 )
    glEnable( GL_DEPTH_TEST )
    glDepthFunc( GL_LEQUAL )
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )

    glDepthFunc( GL_LEQUAL )
    glEnable( GL_DEPTH_TEST )
    
    vertexShader = shaders.compileShader(open('main.vert', 'r').read(), GL_VERTEX_SHADER)
    fragmentShader = shaders.compileShader(open('main.frag', 'r').read(), GL_FRAGMENT_SHADER)

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
roda = pywavefront.Wavefront("roda2.obj")
carro = pywavefront.Wavefront("carro.obj")
mario = pywavefront.Wavefront("disco.obj")
glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
glutSpecialFunc(KeysEspecial)
glutKeyboardFunc(Keys)
glutMainLoop()
