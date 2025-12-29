from settings import *
from game_time_manager import game_time_manager


class Award(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self._layer = 6
        self.type = type
        self.image_origin = pygame.image.load(os.path.join(IMAGE_PATH, f"awards/award{self.type}.png"))
        scaled_width = GRID_SIZE * 2  # 缩放后的宽度
        scaled_height = self.image_origin.get_height() * (scaled_width / self.image_origin.get_width())  # 保持宽高比
        self.image = pygame.transform.scale(self.image_origin, (scaled_width, scaled_height))
        self.rect = self.image.get_rect(center=(x, y))
        self.last_toggle = game_time_manager.get_game_time()
        self.alpha = 255

    def update(self):
        # 闪烁效果
        current_time = game_time_manager.get_game_time()
        # 根据时间间隔切换透明度
        if current_time - self.last_toggle > 500:
            self.last_toggle = current_time
            self.alpha = 0 if self.alpha == 255 else 255
            self.image.set_alpha(self.alpha)  # 应用透明度
