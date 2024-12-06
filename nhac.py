import pygame

def play_music(file_path, loop=True):

    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    if loop:
        pygame.mixer.music.play(-1)  # Lặp vô hạn
    else:
        pygame.mixer.music.play()  # Phát 1 lần

def stop_music():   #Hàm dừng nhạc nền.
    pygame.mixer.music.stop()

