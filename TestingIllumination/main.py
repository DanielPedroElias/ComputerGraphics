
# Importações necessárias
import pywavefront # Importa a biblioteca PyWavefront pra carregar objetos 3D
import numpy as np # Importa a biblioteca NumPy pra trabalhar com arrays
import cv2  # Usando OpenCV para carregar e ler o vídeo
import pygame # Importa a biblioteca Pygame pra reproduzir música de fundo

from OpenGL.GL import * # Importa todas as funções do OpenGL
from OpenGL.GLU import * # Importa todas as funções do OpenGL Utility Library pra criar a câmera
from OpenGL.GLUT import * # Importa todas as funções do OpenGL Utility Toolkit pra criar a janela
from pywavefront import visualization  # Importa a função visualization da biblioteca PyWavefront pra visualizar os objetos 3D
from OpenGL.arrays import vbo # Importa a classe vbo pra trabalhar com Vertex Buffer Objects
from OpenGL.GL import shaders # Importa a classe shaders pra trabalhar com shaders
from moviepy.editor import VideoFileClip # Importa a classe VideoFileClip da biblioteca MoviePy pra reproduzir vídeos
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18 # Importa a constante GLUT_BITMAP_HELVETICA_18
from PIL import Image # Importa a classe Image da biblioteca PIL pra trabalhar com imagens



# Variáveis de movimentação e posição
T, T2, T3 = 1, 1, 0  # Movimentação nos eixos X, Y e Z
L, L2, L3 = 0.0, 20.0, 0.0  # Posição da luz
Fx, Fy, Fz = 18, 0, 0  # Posição do foco da luz
Teclaw = False
pulo = False

# Variáveis de posição dos objetos
# posição do chão
posChaoX = -5

# posição do cubo
posCubeX, posCubeY = -5, 7

# posição do cubo 2 (para fazer a escada)
posCubeX2, posCubeY2 = 36, 0.9

# posição do chao do castelo
posChaoX2 = 80

# posição do castelo
posCastlex = 85

# posição da bandeira
posBandeira = 70

camx, camy, camz = 5.0, 10.0, 30.0  # Posição da câmera

# variavel pra controlar a reprodução do video
controle = 0

fds = True

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


# Função display para renderização
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Movimenta a câmera
    global camx, camy, camz
    global T, T2, T3
    if T > camx + 5:
        if camx < 70.0:
            if camx< camx+5:
                camx += 1
    elif T < camx - 5:
        if camx > 5.0:
            if camx > camx-5:
                camx -= 5
    gluLookAt(camx, camy, camz, 
              camx, camy, 0.0, 
              0.0, 1.0, 0.0)


    # Desenha o personagem principal (Mario)
    glPushMatrix()
    glTranslatef(T, T2, T3)
    glScalef(0.5, 0.5, 0.5)
    
    glUseProgram(main_shader)

    corObj = (0.5, 0.0, 0.0, 1)  # Cor do objeto
    corLuz = (0.9, 0.9, 0.9, 1.0)  # Cor da luz
    configurar_material(corObj)
    configurar_luz(L, L2, L3,corLuz)

    obj_draw_shaderTexture(mario, main_shader, mario_ID)
    glPopMatrix()

    # Desenha o cubo
    desenhar_cubo(posCubeX, posCubeY, caixa)
    desenhar_cubo(posCubeX + 14, posCubeY + 7, cube)
    desenhaCubes(posCubeX + 10, posCubeY, 5)

    # Desenha o cubo
    global posCubeX2, posCubeY2
    
    # desenha a primeira linha da escada
    desenhaCubes(posCubeX2, posCubeY2, 5)
    # desenha a segunda linha da escada
    desenhaCubes(posCubeX2 +2, posCubeY2 +2, 4)
    # desenha a terceira linha da escada
    desenhaCubes(posCubeX2 +4, posCubeY2 +4, 3)
    # desenha a quarta linha da escada
    desenhaCubes(posCubeX2 +6, posCubeY2 +6, 2)
    # desenha o ultimo cubo da escada
    desenhar_cubo(posCubeX2 + 8, posCubeY2 +8 , cube)

    # Desenha o chão

    desenhar_chao(posChaoX, chao)
 
    desenhar_chao(posChaoX + 35, chao )

    desenhar_chao(posChaoX2, chaoCastelo)

    # Desenha o castelo
    desenhaCastelo()

    # Desenha a bandeira
    desenhaBandera()

    # Desenha a esfera de luz
    desenhar_esfera(L, L2, L3, corLuz)

    global fds 
    if fds == True:
        # desenha o inimigo
        desenhaInimigo()

    glUseProgram(0) # Desativa o shader

    
    # colisao do inimigo
    if T >= Fx - 1 and T <= Fx + 1 and fds == True and T2 <= 2:
        fds = False
        play_music("media/Freddy.mp3", 1, 1)    
        DesenhaVideo("media/explosion.mp4", Fx-4, 0, 6, 4)

    # Desenha os eixos de coordenadas
    #desenhar_eixos()

    # colisão com o castelo
    global controle
    # Dentro da função display (onde ocorre a colisão com o castelo)
    if (T > posCastlex - 5 and T < posCastlex + 5) and controle == 0:
        controle = 1
        T = T
        play_music("media/conquista.mp3", 1, 1)  # Toca a música de conquista
        # Rotaciona a matriz para ajustar o vídeo (180 graus)
        glPushMatrix()  # Salva o estado atual da matriz
        glTranslatef(posCastlex, 4 + 4, 0)  # Centraliza a rotação no meio do vídeo
        glRotatef(180, 0, 0, 1)  # Rotaciona 180 graus
        glTranslatef(-posCastlex, -(4 + 4), 0)  # Restaura a posição original

        # Executa o vídeo de conquista
        DesenhaVideo("media/conquista.mp4", posCastlex-4, 4, 8, 8)

        glPopMatrix()  # Restaura o estado da matriz

    

    glutSwapBuffers()

def desenhaInimigo():
        glPushMatrix()
        glTranslatef(Fx, Fy, Fz)
        glUseProgram(main_shader)
        corInimigo = (1.0, 1.0, 0.0, 1.0)
        configurar_material(corInimigo)
        obj_draw_shader(Freddy)
        glPopMatrix()

def desenhaBandera():
    glPushMatrix()
    glTranslatef(posBandeira, 0, 0)
    glUseProgram(main_shader)
    corBandeira = (1.0, 1.0, 1.0, 1.0)
    configurar_material(corBandeira)
    obj_draw_shader(bandeira)
    glPopMatrix()

def desenhaCastelo():
    glPushMatrix()
    glTranslatef(posCastlex, -0.1, -9)
    glScalef(.3, .3, .3)
    glUseProgram(main_shader)
    corCastelo = (1.0, 0.5, 0.0, 1.0)  # Laranja (RGB: 255, 127, 0)    
    configurar_material(corCastelo)
    obj_draw_shaderTexture(castelo, main_shader, castelo_ID)
    glPopMatrix()

def CarregaTexturaDoFrame(frame):
    # Converte o frame para uma textura OpenGL
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    altura, largura, _ = frame_rgb.shape

    # Gera uma nova textura
    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)

    # Definir parâmetros de textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # Transferir os dados do frame para a textura
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, largura, altura, 0, GL_RGB, GL_UNSIGNED_BYTE, frame_rgb)

    return textura_id

def DesenhaVideo(arquivo_video, x, y, largura, altura):
    # Carrega o vídeo usando OpenCV
    video = cv2.VideoCapture(arquivo_video)

    # Verifica se o vídeo foi carregado corretamente
    if not video.isOpened():
        print("Erro ao abrir o vídeo.")
        return

    while True:
        ret, frame = video.read()  # Lê um frame do vídeo
        if not ret:
            break  # Sai do loop se o vídeo terminar

        textura_id = CarregaTexturaDoFrame(frame)

        # Desenhar um quadrilátero com a textura do frame
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textura_id)

        glPushMatrix()  # Salva a matriz de transformação atual

        # Define a posição do quadrilátero na tela
        glTranslatef(x, y, 1)

        # Desenha o quadrilátero com a textura do frame do vídeo
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex2f(0, 0)  # Inferior esquerdo
        glTexCoord2f(1.0, 0.0); glVertex2f(largura, 0)  # Inferior direito
        glTexCoord2f(1.0, 1.0); glVertex2f(largura, altura)  # Superior direito
        glTexCoord2f(0.0, 1.0); glVertex2f(0, altura)  # Superior esquerdo
        glEnd()

        glPopMatrix()  # Restaura a matriz de transformação anterior

        # Exibe o frame na janela
        glutSwapBuffers()

        # Libera a textura para o próximo frame
        glDeleteTextures([textura_id])

        # Controle de velocidade do vídeo (depende do framerate)
        cv2.waitKey(30)

    video.release()  # Libera o vídeo após terminar

# Função para desenhar texto na tela
def DesenhaTexto(text, x, y, font=GLUT_BITMAP_HELVETICA_18):
    glPushMatrix() # Salva a matriz de transformação atual
    glRasterPos2f(x, y)  # Define a posição do texto
    # para cada caractere no texto
    for ch in text:
        glutBitmapCharacter(font, ord(ch))  # Desenha cada caractere do texto
    glPopMatrix() # Restaura a matriz de transformação anterior

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
    obj_draw_shaderTexture(objeto, main_shader, chao_ID)
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
    glUniform4f(LIGTH_LOCATIONS['Material_ambient'], 0, 0, 0, 1.0)
    glUniform4f(LIGTH_LOCATIONS['Material_diffuse'], *cor)
    glUniform4f(LIGTH_LOCATIONS['Material_specular'], 0.9, 0.9, 0.9, 1)
    glUniform1f(LIGTH_LOCATIONS['Material_shininess'], 0.6 * 128.0)

# Função para configurar as luzes
def configurar_luz(L, L2, L3, corLuz):
    glUniform4f(LIGTH_LOCATIONS['Global_ambient'], 0, 0, 0, 1.0)
    glUniform3f(LIGTH_LOCATIONS['Light_location'], L, L2, L3)
    glUniform4f(LIGTH_LOCATIONS['Light_ambient'], 0, 0, 0, 1.0 )
    glUniform4f(LIGTH_LOCATIONS['Light_diffuse'], *corLuz)
    glUniform4f(LIGTH_LOCATIONS['Light_specular'], *corLuz)

# Desenha múltiplos cubos em linha
def desenhaCubes(posx, posy, quantidade):
    for i in range(quantidade):
        desenhar_cubo(posx + (i + i), posy, cube)

# Função para tocar música de fundo 
def play_music(music_path, channel, volume):
    pygame.mixer.init()
    pygame.mixer.Channel(2)
    sound = pygame.mixer.Sound(music_path)
    sound_channel = pygame.mixer.Channel(channel)
    sound_channel.play(sound, loops=0)
    # seta o volume 
    sound_channel.set_volume(volume)
# Função para redimensionar a tela
def resize(w, h):
    glViewport(0, 0, w, h) # Define a área de visualização
    glMatrixMode(GL_PROJECTION) # Define a matriz de projeção
    glLoadIdentity() # Carrega a matriz identidade
    gluPerspective(45, w / h, 0.1, 100.0) # Define a perspectiva
    glMatrixMode(GL_MODELVIEW) # Define a matriz de visualização 
    glLoadIdentity() # Carrega a matriz identidade

def Keys(key, x, y):

    global T
    global T2
    global T3, pulo
    
    if(key == b'a'): 
        T -= .5
    elif(key == b'd'): 
        T += .5
    elif((key == b'w') and T2 <= 1) or (pulo == True and key == b'w'): 
        global Teclaw
        Teclaw = True

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

i = 0
VelocidadeX = .5

def animacao(value):
    glutPostRedisplay()
    glutTimerFunc(30, animacao,1)

    #colisao do chao
    # chao tem tamanho = 30

    global T, T2, T3, pulo
    global posChaoX, posCubeY, posCubeX, posCubeX2, posCubeY2
    global Teclaw
    global i
    # aninimação de pulo
    if Teclaw == True:
        if i <=8    :
            i += 1
            T2 += 1

        elif pulo == True:
            pulo = False

        else:
            i = 0
            Teclaw = False

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
    if (T > posCubeX -2 and T < posCubeX + 2) and T2 >= posCubeY+ 1:
        if T2 < posCubeY+1.5:
            T2 = posCubeY+1.5
            pulo = True
        
    elif ( T > posCubeX+12 and T < posCubeX+16) and T2 >= posCubeY+8:
        if T2 < posCubeY+8.5:
            T2 = posCubeY+8.5
            pulo = True
    elif (T > posCubeX+8 and T < posCubeX+20) and T2 >= posCubeY+1:
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
    

    # animando o inimigo
    global Fx, Fy, Fz, VelocidadeX
    # mantem o movimento em um intervalo 
    if Fx >32:
        VelocidadeX = -VelocidadeX
    elif Fx < 17:
        VelocidadeX = -VelocidadeX
    Fx += VelocidadeX

    #implementa gravidade
    if T2 > -3:
        if Teclaw == False:
            T2 -= 0.4

    if T2 <= -3: 
        print("you died")
    
# Função de inicialização (setup inicial)
def init():
    glClearColor(0.3, 0.3, 0.3, 0.0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)

    # Carrega e compila shaders
    vertexShader = shaders.compileShader(open('shaders/main.vert', 'r').read(), GL_VERTEX_SHADER)
    fragmentShader = shaders.compileShader(open('shaders/main.frag', 'r').read(), GL_FRAGMENT_SHADER)

    global main_shader
    main_shader = glCreateProgram()
    glAttachShader(main_shader, vertexShader)
    glAttachShader(main_shader, fragmentShader)
    glLinkProgram(main_shader)

    # Define variáveis de iluminação no shader
    global LIGTH_LOCATIONS
    LIGTH_LOCATIONS = {
        'Global_ambient': glGetUniformLocation(main_shader, 'Global_ambient'),
        'Light_ambient': glGetUniformLocation(main_shader, 'Light_ambient'),
        'Light_diffuse': glGetUniformLocation(main_shader, 'Light_diffuse'),
        'Light_location': glGetUniformLocation(main_shader, 'Light_location'),
        'Light_specular': glGetUniformLocation(main_shader, 'Light_specular'),
        'Material_ambient': glGetUniformLocation(main_shader, 'Material_ambient'),
        'Material_diffuse': glGetUniformLocation(main_shader, 'Material_diffuse'),
        'Material_shininess': glGetUniformLocation(main_shader, 'Material_shininess'),
        'Material_specular': glGetUniformLocation(main_shader, 'Material_specular'),
    }

    global TEX_LOCATIONS
    TEX_LOCATIONS = {
        'tex': glGetAttribLocation(main_shader, 'tex')
    }

    # Carregar a textura do Mario
    global mario_ID
    mario_img = Image.open('texturas/mario.png')
    w, h, mario_img = mario_img.size[0], mario_img.size[1], mario_img.tobytes("raw", "RGB", 0, -1)
    mario_ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, mario_ID)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, w, h, GL_RGB, GL_UNSIGNED_BYTE, mario_img)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    global chao_ID
    chao_img = Image.open('texturas/chao.png')
    w, h, chao_img = chao_img.size[0], chao_img.size[1], chao_img.tobytes("raw", "RGB", 0, -1)
    chao_ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, chao_ID)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, w, h, GL_RGB, GL_UNSIGNED_BYTE, chao_img)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    global castelo_ID
    castelo_img = Image.open('texturas/castelo.png')
    w, h, castelo_img = castelo_img.size[0], castelo_img.size[1], castelo_img.tobytes("raw", "RGB", 0, -1)
    castelo_ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, castelo_ID)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, w, h, GL_RGB, GL_UNSIGNED_BYTE, castelo_img)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)




glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1920, 1080)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Super Mario 100% Original")

init()

# Carrega os objetos 3D
mario = pywavefront.Wavefront("objetos/mario.obj")
cube = pywavefront.Wavefront("objetos/cube.obj")
chao = pywavefront.Wavefront("objetos/chao.obj")
chaoCastelo = pywavefront.Wavefront("objetos/chaoCastelo.obj")
caixa = pywavefront.Wavefront("objetos/caixaInterrogacao.obj")
castelo = pywavefront.Wavefront("objetos/castelo.obj")
bandeira = pywavefront.Wavefront("objetos/flag.obj")
Freddy = pywavefront.Wavefront("objetos/Freddy.obj")

# inicia a mudica de fundo
play_music("media/Super Mario Bros. Soundtrack.mp3", 0, 1)

glutDisplayFunc(display)
glutReshapeFunc(resize)
glutTimerFunc(30,animacao,1)
glutSpecialFunc(KeysEspecial)
glutKeyboardFunc(Keys)
glutMainLoop()