from settings import *
from game_time_manager import game_time_manager


class ExplodeEffect(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self._layer = 4
        self.frame = 0
        self.frames = []
        for i in range(1, 6):
            scale = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2}[i]
            frame = pygame.image.load(os.path.join(IMAGE_PATH, f"explode/explode{i}.png")).convert_alpha()
            frame = pygame.transform.scale(frame, (scale * 1.5 * GRID_SIZE, scale * 1.5 * GRID_SIZE))
            self.frames.append(frame)
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(center=(center[0], center[1]))
        self.start_time = game_time_manager.get_game_time()

    def update(self):
        now = game_time_manager.get_game_time()
        if now - self.start_time > 100:
            self.frame += 1
            self.start_time = now
            if self.frame < len(self.frames):
                self.image = self.frames[self.frame]
                self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
            else:
                self.kill()


class fire_Effect(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self._layer = 4
        self.image_origin = pygame.image.load(os.path.join(IMAGE_PATH, "explode/explode2.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image_origin, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect(center=(center[0], center[1]))
        self.start_time = game_time_manager.get_game_time()

    def update(self):
        now = game_time_manager.get_game_time()
        if now - self.start_time > 100:
            self.kill()


class score_Effect(pygame.sprite.Sprite):
    def __init__(self, center, score, duration=300):
        super().__init__()
        self._layer = 3
        self.font = pygame.font.Font(os.path.join(FONT_PATH, "ARCADECLASSIC-1.ttf"), 50)
        self.image_orign = self.font.render(str(score), True, COLORS["WHITE"])
        self.rect = self.image_orign.get_rect()
        self.scaled_width = GRID_SIZE * 2
        self.scaled_height = (self.rect.height / self.rect.width) * self.scaled_width
        self.image = pygame.transform.scale(self.image_orign, (self.scaled_width, self.scaled_height))
        self.rect = self.image.get_rect(center=(center[0], center[1]))
        self.start_time = game_time_manager.get_game_time()
        self.duration = duration

    def update(self):
        now = game_time_manager.get_game_time()
        if now - self.start_time > self.duration:
            self.kill()


class game_over_Effect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._layer = 10
        self.font = pygame.font.Font(os.path.join(FONT_PATH, "ARCADECLASSIC-1.ttf"), 50)
        self.text1 = "GAME"
        self.text2 = "OVER"
        self.text1_render = self.font.render(self.text1, True, COLORS["RED"])
        self.text2_render = self.font.render(self.text2, True, COLORS["RED"])
        self.text1_rect = self.text1_render.get_rect()
        self.text2_rect = self.text2_render.get_rect()
        self.image = pygame.Surface((self.text1_rect.width, self.text1_rect.height + self.text2_rect.height),
                                    pygame.SRCALPHA)
        self.image.blit(self.text1_render, (0, 0))
        self.image.blit(self.text2_render, (0, self.text1_rect.height))
        self.rect = self.image.get_rect(center=(GAME_WIDTH / 2, GAME_HEIGHT + self.text1_rect.height))
        self.start_time = game_time_manager.get_game_time()

    def update(self):
        now = game_time_manager.get_game_time()
        elapsed_time = now - self.start_time

        if elapsed_time < 2000:
            # 平滑动画：从屏幕底部移动到屏幕中央
            start_y = GAME_HEIGHT + self.text1_rect.height
            target_y = GAME_HEIGHT / 2
            progress = elapsed_time / 2000  # 0到1的进度

            self.rect.centery = start_y + (target_y - start_y) * progress
        else:
            self.rect.centery = GAME_HEIGHT / 2

        if elapsed_time > 5000:
            self.kill()
