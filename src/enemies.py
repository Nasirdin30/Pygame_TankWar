from settings import *
from effects import *
import random
from player import Bullet


class Enemy(pygame.sprite.Sprite):
    def __init__(self, all_sprites, type, x, y, health, award=False, bullets=None, game_objects=None, freezed=False):
        super().__init__()
        self.image = None
        self.original_image = None
        self._layer = 2
        self.all_sprites = all_sprites
        self.bullets = bullets
        self.bullet = pygame.sprite.Group()
        self.bricks_group = game_objects["bricks"]
        self.stone_group = game_objects["stone"]
        self.forest_group = game_objects["forest"]
        self.water_group = game_objects["water"]
        self.enemies_group = game_objects["enemies"]
        self.freezed = freezed
        self.type = type
        self.x = x
        self.y = y
        self.award = award
        self.speed = {1: 2, 2: 4, 3: 2, 4: 2}[self.type]
        self.health = health
        self.bonus = {1: 100, 2: 200, 3: 300, 4: 400}[self.type]
        self.animation_frames = []
        self.direction = "down"
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.init_image()
        self.rect.center = (x, y)
        self.animation_index = 0
        self.last_animation_update = 0
        self.moving = False
        self.bullet_speed = {1: 5, 2: 5, 3: 10, 4: 5}[self.type]
        self.magazine_size = 1
        self.last_move_time = 0
        self.move_interval = random.randint(1000, 3000)
        self.current_direction = random.choice(["up", "down", "left", "right"])
        self.last_shoot_time = 0
        self.shoot_interval = random.randint(0, 1000)
        self.last_move_axis = None

    def init_image(self):
        self.animation_frames = []
        if self.award:
            frame1 = pygame.image.load(os.path.join(IMAGE_PATH, f"enemy/enemy{self.type}_3_1.png"))
            frame2 = pygame.image.load(os.path.join(IMAGE_PATH, f"enemy/enemy{self.type}_3_2.png"))
            scaled_width = (SCREEN_WIDTH / GRID * 2) * 0.7
        elif self.health > 1:
            frame1 = pygame.image.load(os.path.join(IMAGE_PATH, f"enemy/enemy{self.type}_2_1.png"))
            frame2 = pygame.image.load(os.path.join(IMAGE_PATH, f"enemy/enemy{self.type}_2_2.png"))
            scaled_width = (SCREEN_WIDTH / GRID * 2) * 0.7
        else:
            frame1 = pygame.image.load(os.path.join(IMAGE_PATH, f"enemy/enemy{self.type}_1_1.png"))
            frame2 = pygame.image.load(os.path.join(IMAGE_PATH, f"enemy/enemy{self.type}_1_2.png"))
            scaled_width = (SCREEN_WIDTH / GRID * 2) * 0.7
        for frame in [frame1, frame2]:
            scaled_height = (frame.get_height() / frame.get_width()) * scaled_width
            scaled_frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
            self.animation_frames.append(scaled_frame)
        self.original_image = self.animation_frames[0]
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rotate()

    def rotate(self):
        angle = {"up": 0, "down": 180, "left": 90, "right": 270}[self.direction]
        self.image = pygame.transform.rotate(self.original_image, angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

    def snap_to_grid(self, axis):
        if axis == "x":
            old_x = self.rect.centerx
            nearest = round(self.rect.centerx / GRID_SIZE) * GRID_SIZE
            self.rect.centerx = nearest
            if pygame.sprite.spritecollideany(self, self.bricks_group):
                if old_x < nearest:
                    self.rect.centerx = self.rect.centerx - GRID_SIZE
                else:
                    self.rect.centerx = self.rect.centerx + GRID_SIZE
        if axis == "y":
            old_y = self.rect.centery
            nearest = round(self.rect.centery / GRID_SIZE) * GRID_SIZE
            self.rect.centery = nearest
            if pygame.sprite.spritecollideany(self, self.bricks_group):
                if old_y < nearest:
                    self.rect.centery = self.rect.centery - GRID_SIZE
                else:
                    self.rect.centery = self.rect.centery + GRID_SIZE

    def update(self):
        current_time = pygame.time.get_ticks()
        self.rect.clamp_ip((0, 0, GAME_WIDTH, GAME_HEIGHT))
        collided_enemies = []
        for enemy in self.enemies_group:
            if enemy != self and pygame.sprite.collide_rect(self, enemy):
                collided_enemies.append(enemy)

        old_x = self.rect.x
        old_y = self.rect.y

        if not self.freezed:
            if current_time - self.last_move_time > self.move_interval:
                self.current_direction = random.choice(["up", "down", "left", "right"])
                self.last_move_time = current_time
                self.move_interval = random.randint(1000, 3000)
            if self.current_direction == "up":
                self.move_up()
            elif self.current_direction == "down":
                self.move_down()
            elif self.current_direction == "left":
                self.move_left()
            elif self.current_direction == "right":
                self.move_right()

            collided = pygame.sprite.spritecollideany(self, self.bricks_group) or \
                       pygame.sprite.spritecollideany(self, self.water_group) or \
                       pygame.sprite.spritecollideany(self, self.stone_group)
            enemy_collision = False
            for enemy in self.enemies_group:
                if enemy != self and pygame.sprite.collide_rect(self, enemy) and enemy not in collided_enemies:
                    enemy_collision = True
            if collided or enemy_collision:
                self.rect.x = old_x
                self.rect.y = old_y
                self.current_direction = random.choice(["up", "down", "left", "right"])
                self.last_move_time = current_time
            if self.direction == "up" and self.rect.y - self.speed < 0:
                self.current_direction = random.choice(["down", "left", "right"])
                self.last_move_time = current_time
            elif self.direction == "down" and self.rect.bottom + self.speed > GAME_HEIGHT:
                self.current_direction = random.choice(["up", "left", "right"])
                self.last_move_time = current_time
            elif self.direction == "left" and self.rect.x - self.speed < 0:
                self.current_direction = random.choice(["up", "down", "right"])
                self.last_move_time = current_time
            elif self.direction == "right" and self.rect.right + self.speed > GAME_WIDTH:
                self.current_direction = random.choice(["up", "down", "left"])
                self.last_move_time = current_time

            if current_time - self.last_shoot_time > self.shoot_interval:
                self.shoot()
                self.last_shoot_time = current_time
                self.shoot_interval = random.randint(0, 1000)

        if self.moving:
            if current_time - self.last_animation_update > 100:
                self.animation_index = (self.animation_index + 1) % len(self.animation_frames)
                self.original_image = self.animation_frames[self.animation_index]
                self.last_animation_update = current_time
                self.rotate()

        self.moving = False

    def move_up(self):
        if self.last_move_axis != "y":
            self.snap_to_grid("x")
            self.last_move_axis = "y"
        self.direction = "up"
        self.rotate()
        self.rect.y -= self.speed
        self.moving = True

    def move_down(self):
        if self.last_move_axis != "y":
            self.snap_to_grid("x")
            self.last_move_axis = "y"
        self.direction = "down"
        self.rotate()
        self.rect.y += self.speed
        self.moving = True

    def move_left(self):
        if self.last_move_axis != "x":
            self.snap_to_grid("y")
            self.last_move_axis = "x"
        self.direction = "left"
        self.rotate()
        self.rect.x -= self.speed
        self.moving = True

    def move_right(self):
        if self.last_move_axis != "x":
            self.snap_to_grid("y")
            self.last_move_axis = "x"
        self.direction = "right"
        self.rotate()
        self.rect.x += self.speed
        self.moving = True

    def shoot(self):
        if len(self.bullet) >= self.magazine_size:
            return
        bullet = Bullet(self.rect, self.direction, speed=self.bullet_speed, is_player=False,
                        all_sprites=self.all_sprites)
        self.bullet.add(bullet)
        self.all_sprites.add(self.bullet)
        self.bullets.add(self.bullet)

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            self.all_sprites.add(ExplodeEffect(self.rect.center))
            return True
        else:
            self.init_image()
            return False
