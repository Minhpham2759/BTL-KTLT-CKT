import pygame
import game_config as gc
from pygame import display, event
from time import sleep
from animal import Animal
import ctypes
import subprocess
import sys
from giaodien_gamesetting import SettingsButton
from music_ingame import AudioManager  # Import AudioManager

ctypes.windll.shcore.SetProcessDpiAwareness(1)
BACKGROUND_IMAGE_PATH = 'source\\play_background.png'
SETTINGS_ICON_PATH = 'source\\setting_icon.png'  # Đường dẫn đến ảnh settings
RESUME_ICON_PATH = 'source\\resume_icon.png'  # Đường dẫn đến ảnh resume
RESTART_ICON_PATH = 'source\\restart_icon.jpg'  # Đường dẫn đến ảnh restart
HOME_ICON_PATH = 'source\\home_icon.png'  # Đường dẫn đến ảnh home
SOUND_ICON_PATH = 'source\\mute_icon.png'  # Đường dẫn đến ảnh âm thanh

class MemoryGame:
    def __init__(self):
        pygame.init()
        display.set_caption('Memory Game')
        self.screen = display.set_mode((gc.SCREEN_SIZE, gc.SCREEN_HEIGHT))
        self.background = pygame.image.load(BACKGROUND_IMAGE_PATH)
        self.background = pygame.transform.scale(self.background, (gc.SCREEN_SIZE, gc.SCREEN_HEIGHT))
        self.running = True
        self.tiles = [Animal(i) for i in range(0, gc.NUM_TILES_TOTAL)]
        self.current_images_displayed = []

        # Tạo nút Settings và nút Âm Thanh
        self.settings_button = SettingsButton(self.screen, SETTINGS_ICON_PATH, (gc.SCREEN_SIZE - 70, 20))
        self.sound_button = SettingsButton(self.screen, SOUND_ICON_PATH, (gc.SCREEN_SIZE - 140, 20))

        # Quản lý âm thanh
        self.audio_manager = AudioManager("music\\lawnbgm(1).mp3", SOUND_ICON_PATH)

        # Biến trạng thái để quản lý màn hình pause
        self.game_paused = False

        # Tải các biểu tượng nút
        self.resume_icon = pygame.image.load(RESUME_ICON_PATH)
        self.resume_icon = pygame.transform.scale(self.resume_icon, (200, 50))

        self.restart_icon = pygame.image.load(RESTART_ICON_PATH)
        self.restart_icon = pygame.transform.scale(self.restart_icon, (200, 50))

        self.home_icon = pygame.image.load(HOME_ICON_PATH)
        self.home_icon = pygame.transform.scale(self.home_icon, (200, 50))

    def find_index_from_xy(self, x, y):
        adjusted_x = x - gc.SCREEN_SIZE // 2 + (gc.NUM_TILES_SIDE * gc.IMAGE_SIZE) // 2
        adjusted_y = y - gc.SCREEN_HEIGHT // 2 + (gc.NUM_TILES_SIDE * gc.IMAGE_SIZE) // 2
        row = adjusted_y // gc.IMAGE_SIZE
        col = adjusted_x // gc.IMAGE_SIZE
        if row < 0 or col < 0 or row >= gc.NUM_TILES_SIDE or col >= gc.NUM_TILES_SIDE:
            return -1, -1, -1
        index = row * gc.NUM_TILES_SIDE + col
        return row, col, index

    def draw_pause_screen(self):
        """Vẽ màn hình pause với các nút điều khiển."""
        resume_button = pygame.Rect((gc.SCREEN_SIZE // 2 - 100, gc.SCREEN_HEIGHT // 2 - 100), (200, 50))
        home_button = pygame.Rect((gc.SCREEN_SIZE // 2 - 100, gc.SCREEN_HEIGHT // 2), (200, 50))
        restart_button = pygame.Rect((gc.SCREEN_SIZE // 2 - 100, gc.SCREEN_HEIGHT // 2 + 100), (200, 50))

        # Vẽ các biểu tượng nút
        self.screen.blit(self.resume_icon, resume_button.topleft)
        self.screen.blit(self.home_icon, home_button.topleft)
        self.screen.blit(self.restart_icon, restart_button.topleft)

    def open_settings(self):
        """Tạm dừng trò chơi và hiển thị giao diện Settings."""
        self.game_paused = True

    def resume_game(self):
        """Tiếp tục trò chơi."""
        self.game_paused = False

    def go_home(self):
        """Trở về màn hình chính."""
        pygame.quit()
        subprocess.run([sys.executable, 'giaodien_open.py'])
        sys.exit()

    def restart_game(self):
        """Khởi động lại trò chơi."""
        pygame.quit()
        subprocess.run([sys.executable, sys.argv[0]])
        sys.exit()

    def run_game(self):
        while self.running:
            current_events = event.get()
            for e in current_events:
                if e.type == pygame.QUIT:
                    self.running = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.open_settings()  # Mở màn hình Settings khi nhấn ESC
                if e.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Kiểm tra nhấn nút Settings
                    if self.settings_button.is_clicked((mouse_x, mouse_y)):
                        self.open_settings()

                    # Kiểm tra nhấn nút âm thanh
                    if self.sound_button.is_clicked((mouse_x, mouse_y)):
                        self.audio_manager.toggle_sound()

                    if self.game_paused:
                        resume_button = pygame.Rect((gc.SCREEN_SIZE // 2 - 100, gc.SCREEN_HEIGHT // 2 - 100), (200, 50))
                        home_button = pygame.Rect((gc.SCREEN_SIZE // 2 - 100, gc.SCREEN_HEIGHT // 2), (200, 50))
                        restart_button = pygame.Rect((gc.SCREEN_SIZE // 2 - 100, gc.SCREEN_HEIGHT // 2 + 100), (200, 50))

                        # Kiểm tra nhấn nút Resume
                        if resume_button.collidepoint(mouse_x, mouse_y):
                            self.resume_game()

                        # Kiểm tra nhấn nút Home
                        if home_button.collidepoint(mouse_x, mouse_y):
                            self.go_home()

                        # Kiểm tra nhấn nút Restart
                        if restart_button.collidepoint(mouse_x, mouse_y):
                            self.restart_game()

                    # Kiểm tra nhấn ô game
                    row, col, index = self.find_index_from_xy(mouse_x, mouse_y)
                    if index >= 0 and index < len(self.tiles) and not self.tiles[index].skip:
                        if index not in self.current_images_displayed and len(self.current_images_displayed) < 2:
                            self.current_images_displayed.append(index)

            if not self.game_paused:
                self.screen.blit(self.background, (0, 0))
                total_skipped = 0
                total_width = gc.NUM_TILES_SIDE * gc.IMAGE_SIZE
                total_height = gc.NUM_TILES_SIDE * gc.IMAGE_SIZE
                center_x = (gc.SCREEN_SIZE - total_width) // 2
                center_y = (gc.SCREEN_HEIGHT - total_height) // 2

                for i, tile in enumerate(self.tiles):
                    current_image = tile.image if i in self.current_images_displayed else tile.box
                    if not tile.skip:
                        self.screen.blit(
                            current_image,
                            (center_x + tile.col * gc.IMAGE_SIZE + gc.MARGIN,
                             center_y + tile.row * gc.IMAGE_SIZE + gc.MARGIN)
                        )
                    else:
                        total_skipped += 1

                self.audio_manager.draw_sound_icon(self.screen, (gc.SCREEN_SIZE - 140, 20))

            # Nếu trò chơi tạm dừng, vẽ màn hình tạm dừng
            if self.game_paused:
                self.draw_pause_screen()

            display.flip()

            if total_skipped == len(self.tiles):
                self.running = False

        pygame.quit()
        subprocess.run([sys.executable, 'giaodien_end.py'])
        sys.exit()
