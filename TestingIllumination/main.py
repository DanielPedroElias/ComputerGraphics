from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pywavefront
from pywavefront import visualization
import numpy as np
import pygame
from OpenGL.arrays import vbo
from OpenGL.GL import shaders

# Variáveis de movimentação e posição
T, T2, T3 = 1, 1, 1  # Movimentação nos eixos X, Y e Z
L, L2, L3 = 0.0, 20.0, 0.0  # Posição da luz

pulo = False

posChaoX = -5

posCubeX, posCubeY = -5, 7

posCubeX2 = 36
posCubeY2 = 0.9

posChaoX2 = 80

posCastlex = 85

posBandeira = 70

camx, camy, camz = 5.0, 10.0, 30.0  # Posição da câmera

# Função para desenhar o objeto utilizando o shader
def obj_draw_shader(objeto):
    objs = list(objeto.materials.keys())
    vertices = objeto.materials[objs[0]].vertices
    vertices = np.array(vertices, dtype=np.float32).reshape(-1, 6)
    vbo_objeto = vbo.VBO(vertices)

    vbo_objeto.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glVertexPointer(3, GL_FLOAT, 24, vbo_objeto + 12)
    glNormalPointer(GL_FLOAT, 24, vbo_objeto)
    glDrawArrays(GL_TRIANGLES, 0, vertices.shape[0])
    vbo_objeto.unbind()
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)

# Função display para renderização
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Movimenta a câmera
    global camx, camy, camz
    
    if T > camx + 12:
        if camx < 70.0:
            camx += 1
    elif T < camx - 12:
        if camx > 5.0:
            camx -= 1

    gluLookAt(camx, camy, camz, camx, camy, 0.0, 0.0, 1.0, 0.0)


    # Desenha o personagem principal (Mario)
    glPushMatrix()
    glTranslatef(T, T2, T3)
    glScalef(0.5, 0.5, 0.5)
    glUseProgram(main_shader)

    corObj = (0.5, 0.0, 0.0, 1)  # Cor do objeto
    corLuz = (1.0, 1.0, 1.0, 1.0)  # Cor da luz
    configurar_material(corObj)
    configurar_luz(L, L2, L3,corLuz)

    obj_draw_shader(mario)
    glPopMatrix()

    # Desenha o cubo
    desenhar_cubo(posCubeX, posCubeY, caixa)
    desenhar_cubo(posCubeX + 14, posCubeY + 7, cube)
    desenhaCubes(posCubeX + 10, posCubeY, 5)

    # Desenha o cubo
    global posCubeX2, posCubeY2
    
    desenhar_cubo(posCubeX2, posCubeY2, cube)
    desenhar_cubo(posCubeX2 + 2, posCubeY2, cube)
    desenhar_cubo(posCubeX2 + 4, posCubeY2, cube)
    desenhar_cubo(posCubeX2 + 6, posCubeY2, cube)
    desenhar_cubo(posCubeX2 + 8, posCubeY2, cube)
    desenhar_cubo(posCubeX2 + 2, posCubeY2 +2 , cube)
    desenhar_cubo(posCubeX2 + 4, posCubeY2 +2 , cube)
    desenhar_cubo(posCubeX2 + 6, posCubeY2 +2 , cube)
    desenhar_cubo(posCubeX2 + 8, posCubeY2 +2 , cube)
    desenhar_cubo(posCubeX2 + 4, posCubeY2 +4 , cube)
    desenhar_cubo(posCubeX2 + 6, posCubeY2 +4 , cube)
    desenhar_cubo(posCubeX2 + 8, posCubeY2 +4 , cube)
    desenhar_cubo(posCubeX2 + 6, posCubeY2 +6 , cube)
    desenhar_cubo(posCubeX2 + 8, posCubeY2 +6 , cube)
    desenhar_cubo(posCubeX2 + 8, posCubeY2 +8 , cube)

    # Desenha o chão

    desenhar_chao(posChaoX, chao)
 
    desenhar_chao(posChaoX + 35, chao )

    desenhar_chao(posChaoX2, chaoCastelo)

    # Desenha o castelo
    glPushMatrix()
    glTranslatef(posCastlex, -0.1, -9)
    glScalef(.3, .3, .3)
    glUseProgram(main_shader)
    corCastelo = (1.0, 0.5, 0.0, 1.0)  # Laranja (RGB: 255, 127, 0)    
    configurar_material(corCastelo)
    obj_draw_shader(castelo)
    glPopMatrix()

    # Desenha a bandeira
    glPushMatrix()
    glTranslatef(posBandeira, 0, 0)
    glUseProgram(main_shader)
    corBandeira = (1.0, 1.0, 1.0, 1.0)
    configurar_material(corBandeira)
    obj_draw_shader(bandeira)
    glPopMatrix()

    # Desenha a esfera de luz
    desenhar_esfera(L, L2, L3, corLuz)

    glUseProgram(0)

    # Desenha os eixos de coordenadas
   # desenhar_eixos()

    glutSwapBuffers()



# Função para desenhar os cubos
def desenhar_cubo(posx, posy, objeto):
    glPushMatrix()
    glTranslatef(posx, posy, 0)
    glUseProgram(main_shader)
    corCube = (1, 1, 0, 1)
    configurar_material(corCube)
    obj_draw_shader(objeto)
    glPopMatrix()

# Função para desenhar o chão
def desenhar_chao(posx, objeto):
    glPushMatrix()
    glTranslatef(posx, -1, 2)
    glUseProgram(main_shader)
    corChao = (0.5, .3, 0.1, 1)
    configurar_material(corChao)
    obj_draw_shader(objeto)
    glPopMatrix()

# Função para desenhar a esfera representando a luz
def desenhar_esfera(L, L2, L3, light_color):
    glPushMatrix()
    glTranslatef(L, L2, L3)
    glUseProgram(main_shader)  # Use o shader para a esfera
    corEsfera = light_color # Mudar a cor da esfera para vermelho
    configurar_material(corEsfera)  # Configurar material da esfera
    glutSolidSphere(0.8, 16, 8)
    glPopMatrix()


# Função para desenhar os eixos de coordenadas
def desenhar_eixos():
    # Eixo X (vermelho)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(20.0, 0.0, 0.0)
    glEnd()

    # Eixo Y (verde)
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 20.0, 0.0)
    glEnd()

    # Eixo Z (azul)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 20.0)
    glEnd()

# Função para configurar os materiais (cor, brilho, etc.)
def configurar_material(cor):
    glUniform4f(LIGTH_LOCATIONS['Material_ambient'], .1, .1, .1, 1.0)
    glUniform4f(LIGTH_LOCATIONS['Material_diffuse'], *cor)
    glUniform4f(LIGTH_LOCATIONS['Material_specular'], 0.9, 0.9, 0.9, 1)
    glUniform1f(LIGTH_LOCATIONS['Material_shininess'], 0.6 * 128.0)

# Função para configurar as luzes
def configurar_luz(L, L2, L3, light_color):
    glUniform4f(LIGTH_LOCATIONS['Global_ambient'], 0.1, 0.1, 0.1, 1.0)
    glUniform3f(LIGTH_LOCATIONS['Light_location'], L, L2, L3)
    glUniform4f(LIGTH_LOCATIONS['Light_diffuse'], *light_color)
    glUniform4f(LIGTH_LOCATIONS['Light_specular'], *light_color)

# Desenha múltiplos cubos em linha
def desenhaCubes(posx, posy, quantidade):
    for i in range(quantidade):
        desenhar_cubo(posx + (i + i), posy, cube)

# Função para redimensionar a tela
def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    


def Keys(key, x, y):

    global T
    global T2
    global T3, pulo
    
    if(key == b'a'): 
        T -= 1
    elif(key == b'd'): 
        T += 1
    elif((key == b'w') and T2 <= 1) or (pulo == True and key == b'w'): 
        T2 += 8
        if pulo == True:
            pulo = False
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
    elif(key == GLUT_KEY_DOWN ): 
        L2 -= 1
    elif(key == GLUT_KEY_UP ): 
        L2 += 1 
    elif(key == GLUT_KEY_PAGE_UP ): 
        L3 -= 1 
    elif(key == GLUT_KEY_PAGE_DOWN ): 
        L3 += 1         
       
def animacao(value):
    glutPostRedisplay()
    glutTimerFunc(30, animacao,1)
    
    #colisao do chao
    # chao tem tamanho = 30

    global T, T2, T3, pulo
    global posChaoX, posCubeY, posCubeX, posCubeX2, posCubeY2

    # limites laterais
    if T <= -17:
        T = -17
    elif T >= 92:
        T = 92
    # Colisa com o chão
    if T > posChaoX -16 and T < posChaoX + 16:
        if T2 < 0.35:
            T2 = 0.35
    elif T > posChaoX -16 + 35 and T < posChaoX +16 + 35:
        if T2 < 0.35:
            T2 = 0.35
    elif T > posChaoX2 -16 and T < posChaoX2 + 16:  
        if T2 < 0.35:
            T2 = 0.35

    # Colisao com os cubos
    if (T > posCubeX -2 and T < posCubeX + 2) and T2 >= posCubeY:
        if T2 < posCubeY+1.5:
            T2 = posCubeY+1.5
            pulo = True
        
    elif ( T > posCubeX+12 and T < posCubeX+16) and T2 >= posCubeY+7:
        if T2 < posCubeY+8.5:
            T2 = posCubeY+8.5
            pulo = True
    elif (T > posCubeX+8 and T < posCubeX+20) and T2 >= posCubeY:
        if T2 < posCubeY+1.5:
            T2 = posCubeY+1.5
            pulo = True

    # Colisao com os cubos em formato de escaad
    if (T > posCubeX2 -2 and T < posCubeX2 + 1) :
        if T2 < posCubeY2+1.5:
            T2 = posCubeY2+1.5    
            pulo = True

    elif (T > posCubeX2 -1 and T < posCubeX2 + 3) :
        if T2 < posCubeY2+3.5:
            T2 = posCubeY2+3.5
            pulo = True

    elif (T > posCubeX2 and T < posCubeX2 + 5) :
        if T2 < posCubeY2+5.5:
            T2 = posCubeY2+5.5
            pulo = True

    elif (T > posCubeX2 + 1 and T < posCubeX2 + 7) :
        if T2 < posCubeY2+7.5:
            T2 = posCubeY2+7.5
            pulo = True

    elif (T > posCubeX2 + 2 and T < posCubeX2 + 10) :
        if T2 < posCubeY2+9.5:
            T2 = posCubeY2+9.5
            pulo = True
 
 
    #implementa gravidade
    if T2 > -3:
        T2 -= 0.4

    if T2 <= -3: 
        print("you died")
    
    



  

def init():
    glClearColor (0.3, 0.3, 0.3, 0.0) # cor de fundo
    glShadeModel( GL_SMOOTH ) # tipo de sombreamento
    glClearColor( 0.13, 0.41, 0.58, 1.0 ) # cor de fundo
    
    glClearDepth( 1.0 ) # valor do z-buffer
    glEnable( GL_DEPTH_TEST ) # ativa o z-buffer
    glDepthFunc( GL_LEQUAL ) # tipo de teste do z-buffer
    glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST ) # correcao de perspectiva

    glDepthFunc( GL_LEQUAL )
    glEnable( GL_DEPTH_TEST )
    
    vertexShader = shaders.compileShader(open('main.vert', 'r').read(), GL_VERTEX_SHADER)
    fragmentShader = shaders.compileShader(open('main.frag', 'r').read(), GL_FRAGMENT_SHADER)

    global main_shader
    main_shader = glCreateProgram()
    glAttachShader(main_shader, vertexShader) 
    glAttachShader(main_shader, fragmentShader)
    glLinkProgram(main_shader)
    
    global LIGTH_LOCATIONS
    LIGTH_LOCATIONS = {
        'Global_ambient': glGetUniformLocation( main_shader, 'Global_ambient' ),
        'Light_ambient': glGetUniformLocation( main_shader, 'Light_ambient' ),
        'Light_diffuse': glGetUniformLocation( main_shader, 'Light_diffuse' ),
        'Light_location': glGetUniformLocation( main_shader, 'Light_location' ),
        'Light_specular': glGetUniformLocation( main_shader, 'Light_specular' ),
        'Material_ambient': glGetUniformLocation( main_shader, 'Material_ambient' ),
        'Material_diffuse': glGetUniformLocation( main_shader, 'Material_diffuse' ),
        'Material_shininess': glGetUniformLocation( main_shader, 'Material_shininess' ),
        'Material_specular': glGetUniformLocation( main_shader, 'Material_specular' ),
        'Object_color': glGetUniformLocation(main_shader, 'Object_color')

    }   
    
    global ATTR_LOCATIONS
    ATTR_LOCATIONS = {
        'Vertex_position': glGetAttribLocation( main_shader, 'Vertex_position' ),
        'Vertex_normal': glGetAttribLocation( main_shader, 'Vertex_normal' )
    }

    

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1920, 1080)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Cubo")

init()

mario = pywavefront.Wavefront("mario.obj")
cube = pywavefront.Wavefront("cube.obj")
chao = pywavefront.Wavefront("chao.obj")
chaoCastelo = pywavefront.Wavefront("chaoCastelo.obj")
caixa = pywavefront.Wavefront("caixaInterrogacao.obj")
castelo = pywavefront.Wavefront("castelo.obj")
bandeira = pywavefront.Wavefront("flag.obj")

# inicia a mudica de fundo
pygame.mixer.init()
pygame.mixer.music.load('Super Mario Bros. Soundtrack.mp3')
pygame.mixer.music.play(-1)

glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
glutSpecialFunc(KeysEspecial)
glutKeyboardFunc(Keys)
glutMainLoop()