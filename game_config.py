import os

IMAGE_SIZE = 128

NUM_TILES_SIDE = 7
NUM_TILES_TOTAL = 56
MARGIN = 8

# Cập nhật kích thước màn hình
SCREEN_SIZE = 1920  # Width của cửa sổ
SCREEN_HEIGHT = 1080  # Height của cửa sổ

ASSET_DIR = 'ani'
ASSET_FILES = [x for x in os.listdir(ASSET_DIR) if x[-3:].lower() == 'png']
assert len(ASSET_FILES) == 34
