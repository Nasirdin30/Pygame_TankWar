from settings import *
from effects import *


class Bricks(pygame.sprite.Sprite):
    def __init__(self, x, y, sub_x, sub_y):
        super().__init__()
        self._layer = 1
        self.sub_size = GRID_SIZE / 2
        original_image = pygame.image.load(os.path.join(IMAGE_PATH, "objects/bricks.png"))
        sub_image = original_image.subsurface(
            (sub_x * (original_image.get_width() / 2), sub_y * (original_image.get_height() / 2),
             original_image.get_width() / 2, original_image.get_height() / 2))
        self.image = pygame.transform.scale(sub_image, (self.sub_size, self.sub_size))
        self.rect = self.image.get_rect(topleft=(
            x + sub_x * self.sub_size,
            y + sub_y * self.sub_size
        ))


class Bricks2(pygame.sprite.Sprite):
    def __init__(self, x, y, sub_x, sub_y):
        super().__init__()
        self._layer = 1
        self.sub_size = GRID_SIZE / 2
        original_image = pygame.image.load(os.path.join(IMAGE_PATH, "objects/bricks2.png"))
        sub_image = original_image.subsurface(
            (sub_x * (original_image.get_width() / 2), sub_y * (original_image.get_height() / 2),
             original_image.get_width() / 2, original_image.get_height() / 2))
        self.image = pygame.transform.scale(sub_image, (self.sub_size, self.sub_size))
        self.rect = self.image.get_rect(topleft=(
            x + sub_x * self.sub_size,
            y + sub_y * self.sub_size
        ))


class Stone(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self._layer = 1
        original_image = pygame.image.load(os.path.join(IMAGE_PATH, "objects/stone.png"))
        self.image = pygame.transform.scale(original_image, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))


class Forest(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self._layer = 3
        original_image = pygame.image.load(os.path.join(IMAGE_PATH, "objects/forest.png"))
        self.image = pygame.transform.scale(original_image, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

class Snowfield(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self._layer = 1
        original_image = pygame.image.load(os.path.join(IMAGE_PATH, "objects/snowfield.png"))
        self.image = pygame.transform.scale(original_image, (GRID_SIZE, GRID_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self._layer = 1
        frame1 = pygame.image.load(os.path.join(IMAGE_PATH, "objects/water1.png"))
        frame2 = pygame.image.load(os.path.join(IMAGE_PATH, "objects/water2.png"))
        self.scaled_frame1 = pygame.transform.scale(frame1, (GRID_SIZE, GRID_SIZE))
        self.scaled_frame2 = pygame.transform.scale(frame2, (GRID_SIZE, GRID_SIZE))
        self.images = [self.scaled_frame1, self.scaled_frame2]
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time % 2000 < 1000:
            self.image = self.scaled_frame1
        else:
            self.image = self.scaled_frame2


class Protect(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites):
        super().__init__()
        self._layer = 1
        self.all_sprites = all_sprites
        self.is_destroyed = False
        original_image = pygame.image.load(os.path.join(IMAGE_PATH, "objects/protected_object.png"))
        self.image = pygame.transform.scale(original_image, (GRID_SIZE * 2, GRID_SIZE * 2))
        self.rect = self.image.get_rect(center=(x, y))

    def destroyed(self):
        self.is_destroyed = True
        original_image = pygame.image.load(os.path.join(IMAGE_PATH, "objects/protected_object_destroyed.png"))
        self.image = pygame.transform.scale(original_image, (GRID_SIZE * 2, GRID_SIZE * 2))
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
        self.all_sprites.add(ExplodeEffect(self.rect.center))
