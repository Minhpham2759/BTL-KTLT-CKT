import pygame
import game_config as gc
from pygame import display, event
from time import sleep
from animal import Animal
import ctypes
import subprocess
import sys

ctypes.windll.shcore.SetProcessDpiAwareness(1)
BACKGROUND_IMAGE_PATH = 'source\play_background.png'

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

    def find_index_from_xy(self, x, y):
        adjusted_x = x - gc.SCREEN_SIZE // 2 + (gc.NUM_TILES_SIDE * gc.IMAGE_SIZE) // 2
        adjusted_y = y - gc.SCREEN_HEIGHT // 2 + (gc.NUM_TILES_SIDE * gc.IMAGE_SIZE) // 2
        row = adjusted_y // gc.IMAGE_SIZE
        col = adjusted_x // gc.IMAGE_SIZE
        if row < 0 or col < 0 or row >= gc.NUM_TILES_SIDE or col >= gc.NUM_TILES_SIDE:
            return -1, -1, -1
        index = row * gc.NUM_TILES_SIDE + col
        return row, col, index

    def run_game(self):
        while self.running:
            current_events = event.get()
            for e in current_events:
                if e.type == pygame.QUIT:
                    self.running = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.running = False # Thoát vòng lặp
                        pygame.quit()         # Đóng Pygame
                        subprocess.run([sys.executable, 'giaodien_open.py']) 
                        sys.exit()            # Thoát hoàn toàn chương trình Python
                        subprocess.run([sys.executable, 'giaodien_open.py'])  # Mở lại giaodien_open.py

                if e.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    row, col, index = self.find_index_from_xy(mouse_x, mouse_y)
                    if index >= 0 and index < len(self.tiles) and not self.tiles[index].skip:
                        if index not in self.current_images_displayed and len(self.current_images_displayed) < 2:
                            self.current_images_displayed.append(index)

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

            display.flip()

            if len(self.current_images_displayed) == 2:
                idx1, idx2 = self.current_images_displayed
                sleep(0.5)
                if self.tiles[idx1].name == self.tiles[idx2].name:
                    self.tiles[idx1].skip = True
                    self.tiles[idx2].skip = True
                else:
                    self.current_images_displayed = []
                sleep(0.5)
                self.current_images_displayed = []

            if total_skipped == len(self.tiles):
                self.running = False

        # Sau khi trò chơi kết thúc, mở giaodien_end.py
        pygame.quit()         # Đóng Pygame
        subprocess.run([sys.executable, 'giaodien_end.py']) 
        sys.exit()            # Thoát hoàn toàn chương trình Python
        subprocess.run([sys.executable, 'giaodien_end.py'])  # Mở lại .py



if __name__ == "__main__":
    game = MemoryGame()
    game.run_game()
