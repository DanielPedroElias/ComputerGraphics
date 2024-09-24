import pygame
import cv2
import sys

# Inicializa o Pygame
pygame.init()

# Cria uma janela Pygame com as dimensões do vídeo
video_path = 'conquista.mp4'  # Caminho para o vídeo
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Erro ao abrir o arquivo de vídeo")
    sys.exit()

# Obtém as dimensões do vídeo
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Cria uma tela Pygame com as mesmas dimensões do vídeo
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Reprodução de Vídeo')

# Loop principal para reproduzir o vídeo
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ret, frame = cap.read()
    if not ret:
        break

    # Converte o frame do vídeo de BGR (OpenCV) para RGB (Pygame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Transforma o frame em uma Surface do Pygame
    frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

    # Exibe o frame na tela
    screen.blit(frame_surface, (0, 0))
    pygame.display.update()

    # Controla o FPS
    clock.tick(fps)

# Libera os recursos ao final da execução
cap.release()
pygame.quit()
