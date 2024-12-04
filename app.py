import pygame
import game_config as gc
from pygame import display, event
from time import sleep
from animal import Animal
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)
# Đường dẫn tới hình ảnh nền
BACKGROUND_IMAGE_PATH = 'source\play_background.png'

class MemoryGame:
    def __init__(self):
        # Khởi tạo Pygame
        pygame.init()
        display.set_caption('Memory Game')

        # Tạo cửa sổ với kích thước được định nghĩa trong game_config
        self.screen = display.set_mode((gc.SCREEN_SIZE, gc.SCREEN_HEIGHT))

        # Tải hình nền và thay đổi kích thước cho phù hợp với màn hình
        self.background = pygame.image.load(BACKGROUND_IMAGE_PATH)
        self.background = pygame.transform.scale(self.background, (gc.SCREEN_SIZE, gc.SCREEN_HEIGHT))  # Thay đổi kích thước

        # Biến để điều khiển vòng lặp trò chơi
        self.running = True
        self.tiles = [Animal(i) for i in range(0, gc.NUM_TILES_TOTAL)]  # Tạo các ô (tiles) từ lớp Animal
        self.current_images_displayed = []  # Danh sách lưu trữ các ô đang được hiển thị

    def find_index_from_xy(self, x, y):
        """
        Hàm này sẽ tính toán chỉ số ô trong một lưới dựa trên tọa độ (x, y) của chuột.
        Nếu chuột click ra ngoài khu vực ô, trả về -1.
        """
        # Tính toán tọa độ của ô
        adjusted_x = x - gc.SCREEN_SIZE // 2 + (gc.NUM_TILES_SIDE * gc.IMAGE_SIZE) // 2
        adjusted_y = y - gc.SCREEN_HEIGHT // 2 + (gc.NUM_TILES_SIDE * gc.IMAGE_SIZE) // 2

        row = adjusted_y // gc.IMAGE_SIZE
        col = adjusted_x // gc.IMAGE_SIZE

        # Kiểm tra nếu chuột nằm trong phạm vi của các ô (không vượt quá số hàng/cột)
        if row < 0 or col < 0 or row >= gc.NUM_TILES_SIDE or col >= gc.NUM_TILES_SIDE:
            return -1, -1, -1  # Trả về -1 nếu click ngoài vùng các ô

        # Tính chỉ số của ô trong mảng 1D
        index = row * gc.NUM_TILES_SIDE + col
        return row, col, index

    def run_game(self):
        while self.running:
            current_events = event.get()  # Lấy tất cả sự kiện đang diễn ra

            for e in current_events:
                if e.type == pygame.QUIT:
                    self.running = False  # Đóng trò chơi khi nhấn nút thoát cửa sổ

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.running = False  # Thoát trò chơi khi nhấn phím ESC

                if e.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()  # Lấy tọa độ của chuột
                    row, col, index = self.find_index_from_xy(mouse_x, mouse_y)  # Tính toán chỉ số của ô dựa trên tọa độ chuột

                    # Kiểm tra nếu ô này hợp lệ và chưa bị lật
                    if index >= 0 and index < len(self.tiles) and not self.tiles[index].skip:
                        if index not in self.current_images_displayed and len(self.current_images_displayed) < 2:
                            self.current_images_displayed.append(index)  # Lật ô nếu điều kiện thỏa mãn

            # Vẽ nền trước
            self.screen.blit(self.background, (0, 0))  # Vẽ hình nền vào vị trí (0, 0)

            total_skipped = 0
            # Tính toán các thông số căn giữa
            total_width = gc.NUM_TILES_SIDE * gc.IMAGE_SIZE  # Chiều rộng của khu vực vẽ các ô
            total_height = gc.NUM_TILES_SIDE * gc.IMAGE_SIZE  # Chiều cao của khu vực vẽ các ô

            # Tính toán tọa độ để căn giữa khu vực vẽ
            center_x = (gc.SCREEN_SIZE - total_width) // 2
            center_y = (gc.SCREEN_HEIGHT - total_height) // 2
            # Vẽ các ô vật phẩm lên màn hình
            for i, tile in enumerate(self.tiles):
                current_image = tile.image if i in self.current_images_displayed else tile.box  # Chọn hình ảnh hiện tại cho ô
                if not tile.skip:
                    # Vẽ ô vào vị trí căn giữa
                    self.screen.blit(
                        current_image,
                        (center_x + tile.col * gc.IMAGE_SIZE + gc.MARGIN,
                         center_y + tile.row * gc.IMAGE_SIZE + gc.MARGIN)
                    )
                else:
                    total_skipped += 1  # Tính tổng số ô đã ghép thành công

            display.flip()  # Cập nhật màn hình

            # Kiểm tra nếu người chơi đã chọn 2 ô
            if len(self.current_images_displayed) == 2:
                idx1, idx2 = self.current_images_displayed
                sleep(0.5)  # Tạm dừng để hiển thị ảnh trong 0.5 giây

                # Kiểm tra nếu 2 ô giống nhau
                if self.tiles[idx1].name == self.tiles[idx2].name:
                    # Nếu giống nhau, đánh dấu các ô này là đã ghép thành công
                    self.tiles[idx1].skip = True
                    self.tiles[idx2].skip = True
                else:
                    # Nếu không giống nhau, ẩn các ô đã chọn
                    self.current_images_displayed = []

                sleep(0.5)  # Tạm dừng để người chơi có thời gian nhìn kết quả
                self.current_images_displayed = []  # Xóa danh sách các ô đang hiển thị

            # Kết thúc trò chơi khi tất cả các ô đã được ghép
            if total_skipped == len(self.tiles):
                self.running = False

        # Hiển thị thông báo kết thúc trò chơi
        print('Goodbye!')

# Khởi tạo và chạy trò chơi
if __name__ == "__main__":
    game = MemoryGame()
    game.run_game()
