import pygame
from moviepy.editor import VideoFileClip

# Inicializa o pygame
pygame.init()

# Função para tocar música de fundo
def play_background_music(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)  # Reproduz a música em loop

# Função que reproduz o vídeo e fecha a janela ao final
def play_video(video_path):
    # Carrega o vídeo
    video = VideoFileClip(video_path)

    # Exibe o vídeo em uma nova janela
    video.preview()

    # Fecha o vídeo automaticamente após a reprodução
    video.close()

# Caminho para o arquivo de música e vídeo
music_path = "Super Mario Bros. Soundtrack.mp3"
video_path = "conquista.mp4"

# Tocar música de fundo
play_background_music(music_path)

# Reproduzir o vídeo sem parar a música de fundo
play_video(video_path)

# Após o vídeo, a música continua tocando até que o programa seja encerrado
input("Pressione Enter para sair...")
pygame.quit()

#  bark
# def play_video(video_path):
#     # Inicializa o Pygame
#     pygame.init()

#     # Configura a janela do Pygame
#     screen = pygame.display.set_mode((720, 720))

#     # Carrega o vídeo com OpenCV
#     cap = cv2.VideoCapture(video_path)

#     # Carrega o vídeo com MoviePy para tocar o áudio
#     video_clip = VideoFileClip(video_path)

#     # Toca o vídeo e o áudio
#     video_clip.preview()  # Isso deve tocar o áudio junto com o vídeo

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

#         # Converte de BGR para RGB
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         # Converte a imagem para superfície do Pygame
#         frame = pygame.surfarray.make_surface(frame)

#         # Exibe o frame na janela do Pygame
#         screen.blit(frame, (0, 0))
#         pygame.display.flip()

#         # Atraso para controlar a taxa de quadros
#         pygame.time.delay(30)

#     cap.release()
#     video_clip.close()  # Fecha o vídeo do MoviePy
#     pygame.quit()  # Fecha o Pygame