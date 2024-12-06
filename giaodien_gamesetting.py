import pygame

class SettingsButton:
    def __init__(self, screen, image_path, position, size=(100, 100)):
        self.screen = screen
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)  # Resize image
        self.rect = self.image.get_rect(topright=position)  # Position the button

    def draw(self): #Vẽ nút Settings lên màn hình.
        self.screen.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):    #Kiểm tra nếu nút Settings được nhấn.
        return self.rect.collidepoint(mouse_pos)
