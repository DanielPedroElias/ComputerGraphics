from moviepy.editor import VideoFileClip

video = VideoFileClip("conquista.mp4")

video.preview()

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