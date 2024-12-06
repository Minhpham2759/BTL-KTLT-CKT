import pygame

class AudioManager:
    def __init__(self, music_path, sound_icon_path):
        # Khởi tạo các tham số cho âm thanh
        self.music_path = music_path
        self.sound_icon_path = sound_icon_path
        self.sound_on = True
        pygame.mixer.init()  # Khởi tạo pygame mixer
        self.background_music = pygame.mixer.Sound(self.music_path)
        self.background_music.play(loops=-1, maxtime=0, fade_ms=0)  # Phát nhạc nền khi bật âm thanh
        self.sound_icon = pygame.image.load(self.sound_icon_path)  # Tải biểu tượng âm thanh
        self.sound_icon = pygame.transform.scale(self.sound_icon, (50, 50))  # Kích thước icon

    def toggle_sound(self):
        """Chuyển trạng thái âm thanh (bật/tắt)."""
        if self.sound_on:
            self.sound_on = False
            self.background_music.stop()  # Dừng nhạc nền khi tắt âm thanh
        else:
            self.sound_on = True
            self.background_music.play(loops=-1, maxtime=0, fade_ms=0)  # Tiếp tục phát nhạc nền khi bật âm thanh

    def draw_sound_icon(self, screen, position):
        """Vẽ biểu tượng âm thanh trên màn hình."""
        screen.blit(self.sound_icon, position)

    def get_sound_status(self):
        """Trả về trạng thái của âm thanh."""
        return self.sound_on
