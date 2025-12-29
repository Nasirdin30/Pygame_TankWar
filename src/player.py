from settings import *
from effects import *
from game_time_manager import game_time_manager


class BasePlayer(pygame.sprite.Sprite):
    def __init__(self, player_type, all_sprites=None, lv=1, bullets=None, game_objects=None, life=3):
        super().__init__()
        self._layer = 2
        self.player_type = player_type
        self.animation_frames = []
        self.lv = lv
        self.init_image()
        self.rect.center = self.get_initial_position()
        self.all_sprites = all_sprites
        self.bullets = bullets
        self.bricks_group = game_objects["bricks"]
        self.stone_group = game_objects["stone"]
        self.forest_group = game_objects["forest"]
        self.water_group = game_objects["water"]
        self.enemies_group = game_objects["enemies"]
        self.live = life
        self.speed = 3
        self.direction = "up"
        self.last_move_axis = None
        self.animation_index = 0
        self.last_animation_update = 0
        self.is_moving = False
        self.init_bullets()
        self.invincible = False
        self.invincible_action = None
        self.invincible_end_time = 0
        self.can_control = True
        self.set_invincible(3000)

    def get_initial_position(self):
        """子类需要重写此方法以提供不同的初始位置"""
        raise NotImplementedError("子类必须实现get_initial_position方法")

    def get_controls(self):
        """子类需要重写此方法以提供不同的控制键位"""
        raise NotImplementedError("子类必须实现get_controls方法")

    def get_image_config(self):
        """子类需要重写此方法以提供不同的图像配置"""
        raise NotImplementedError("子类必须实现get_image_config方法")

    def init_image(self):
        self.animation_frames = []
        image_config = self.get_image_config()
        config = image_config[self.lv]
        frame1 = pygame.image.load(os.path.join(IMAGE_PATH, f"player/{config['frame1']}")).convert_alpha()
        frame2 = pygame.image.load(os.path.join(IMAGE_PATH, f"player/{config['frame2']}")).convert_alpha()
        scaled_width = (GRID_SIZE * 2) * config["scale"]
        for frame in [frame1, frame2]:
            scaled_height = frame.get_height() / frame.get_width() * scaled_width
            scaled_frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
            self.animation_frames.append(scaled_frame)
        self.original_image = self.animation_frames[0]
        self.image = self.original_image
        self.rect = self.image.get_rect()

    def init_bullets(self):
        self.bullet_speed = {1: 5, 2: 10, 3: 10, 4: 10}[self.lv]
        self.magazine_size = {1: 1, 2: 1, 3: 2, 4: 2}[self.lv]

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

    def collided(self):
        enemy_collision = False
        for enemy in self.enemies_group:
            if pygame.sprite.collide_rect(self, enemy):
                enemy_collision = True
        collided = pygame.sprite.spritecollideany(self, self.bricks_group) or \
                   pygame.sprite.spritecollideany(self, self.water_group) or \
                   pygame.sprite.spritecollideany(self, self.stone_group)
        return collided or enemy_collision

    def move_up(self):
        old_x = self.rect.x
        old_y = self.rect.y
        if self.last_move_axis != "y":
            self.snap_to_grid("x")
            self.last_move_axis = "y"
        self.direction = "up"
        self.rect.y -= self.speed
        self.rotate()
        self.is_moving = True
        if self.collided():
            self.rect.x = old_x
            self.rect.y = old_y

    def move_down(self):
        old_x = self.rect.x
        old_y = self.rect.y
        if self.last_move_axis != "y":
            self.snap_to_grid("x")
            self.last_move_axis = "y"
        self.direction = "down"
        self.rect.y += self.speed
        self.rotate()
        self.is_moving = True
        if self.collided():
            self.rect.x = old_x
            self.rect.y = old_y

    def move_left(self):
        old_x = self.rect.x
        old_y = self.rect.y
        if self.last_move_axis != "x":
            self.snap_to_grid("y")
            self.last_move_axis = "x"
        self.direction = "left"
        self.rect.x -= self.speed
        self.rotate()
        self.is_moving = True
        if self.collided():
            self.rect.x = old_x
            self.rect.y = old_y

    def move_right(self):
        old_x = self.rect.x
        old_y = self.rect.y
        if self.last_move_axis != "x":
            self.snap_to_grid("y")
            self.last_move_axis = "x"
        self.direction = "right"
        self.rect.x += self.speed
        self.rotate()
        self.is_moving = True
        if self.collided():
            self.rect.x = old_x
            self.rect.y = old_y

    def update(self):
        if self.can_control:
            self.keyboard_input()
        current_time = game_time_manager.get_game_time()
        if self.is_moving:
            if current_time - self.last_animation_update > 100:
                self.last_animation_update = current_time
                self.animation_index = (self.animation_index + 1) % len(self.animation_frames)
                self.original_image = self.animation_frames[self.animation_index]
                self.rotate()
        self.is_moving = False
        if self.invincible:
            self.invincible_action.rect.center = self.rect.center
            if current_time >= self.invincible_end_time:
                self.invincible = False
                self.invincible_action.kill()

    def keyboard_input(self):
        keys = pygame.key.get_pressed()
        controls = self.get_controls()
        if keys[controls["up"]]:
            self.move_up()
        elif keys[controls["down"]]:
            self.move_down()
        elif keys[controls["left"]]:
            self.move_left()
        elif keys[controls["right"]]:
            self.move_right()

        self.rect.clamp_ip((0, 0, GAME_WIDTH, GAME_HEIGHT))
        if keys[controls["A"]]:
            self.shoot()

    def rotate(self):
        angle = {"up": 0, "down": 180, "left": 90, "right": 270}[self.direction]
        rotated_image = pygame.transform.rotate(self.original_image, angle)
        old_center = self.rect.center
        self.image = rotated_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def shoot(self):
        if not self.can_control:
            return
        if len(self.bullets) >= self.magazine_size:
            return
        bullet = Bullet(self.rect, self.direction, self.bullet_speed, all_sprites=self.all_sprites)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)
        pygame.mixer.Sound(SOUNDS["shoot"]).play()

    def hit(self):
        if self.invincible:
            return
        if self.lv == 4:
            center = self.rect.center
            direction = self.direction
            self.lv = 3
            self.init_image()
            self.init_bullets()
            self.rect.center = center
            self.direction = direction
            self.rotate()
            pygame.mixer.Sound(SOUNDS["bullet_hit_armor"]).play()
            return
        self.dead()

    def dead(self):
        self.all_sprites.add(ExplodeEffect(self.rect.center))
        pygame.mixer.Sound(SOUNDS["player_explode"]).play()
        if self.live == 0:
            self.kill()
        else:
            self.live -= 1
            self.lv = 1
            self.init_image()
            self.direction = "up"
            self.rect.center = self.get_initial_position()
            self.init_bullets()
            self.set_invincible(3000)

    def level_up(self):
        if self.lv < 4:
            old_center = self.rect.center
            self.lv += 1
            self.init_image()
            self.rect.center = old_center
            self.init_bullets()

    def set_invincible(self, duration=3000):
        self.invincible_end_time = game_time_manager.get_game_time() + duration
        if self.invincible:
            return
        self.invincible = True
        self.invincible_action = Invincible(self.rect.center[0], self.rect.center[1])
        self.all_sprites.add(self.invincible_action)


class Player1(BasePlayer):
    def __init__(self, all_sprites=None, lv=1, bullets=None, game_objects=None, life=3):
        super().__init__("player1", all_sprites, lv, bullets, game_objects, life)

    def get_initial_position(self):
        return 9 * GRID_SIZE, 25 * GRID_SIZE

    def get_controls(self):
        return CONTROLS["player1"]

    def get_image_config(self):
        return {
            1: {"frame1": "player1_1_1.png", "frame2": "player1_1_2.png", "scale": 0.7},
            2: {"frame1": "player1_2_1.png", "frame2": "player1_2_2.png", "scale": 0.7},
            3: {"frame1": "player1_3_1.png", "frame2": "player1_3_2.png", "scale": 0.7},
            4: {"frame1": "player1_4_1.png", "frame2": "player1_4_2.png", "scale": 0.8}
        }


class Player2(BasePlayer):
    def __init__(self, all_sprites=None, lv=1, bullets=None, game_objects=None, life=3):
        super().__init__("player2", all_sprites, lv, bullets, game_objects, life)

    def get_initial_position(self):
        return 17 * GRID_SIZE, 25 * GRID_SIZE

    def get_controls(self):
        return CONTROLS["player2"]

    def get_image_config(self):
        return {
            1: {"frame1": "player2_1_1.png", "frame2": "player2_1_2.png", "scale": 0.7},
            2: {"frame1": "player2_2_1.png", "frame2": "player2_2_2.png", "scale": 0.7},
            3: {"frame1": "player2_3_1.png", "frame2": "player2_3_2.png", "scale": 0.7},
            4: {"frame1": "player2_4_1.png", "frame2": "player2_4_2.png", "scale": 0.8}
        }


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_rect, direction, speed, is_player=True, all_sprites=None):
        super().__init__()
        self._layer = 2
        self.all_sprites = all_sprites
        self.player_rect = player_rect  # 记录发射子弹的玩家
        self.direction = direction  # 子弹方向与玩家方向相同
        self.speed = speed  # 子弹速度
        self.init_image()
        self.is_player = is_player

    def init_image(self):
        original_image = pygame.image.load(os.path.join(IMAGE_PATH, "bullet/bullet.png")).convert_alpha()
        scaled_width = (GAME_WIDTH / GRID * 2) * 0.1
        scaled_height = original_image.get_height() / original_image.get_width() * scaled_width
        image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
        self.original_image = image
        if self.direction == "up":
            self.image = pygame.transform.rotate(self.original_image, 0)
            self.rect = self.image.get_rect(midtop=(self.player_rect.centerx, self.player_rect.top))
        elif self.direction == "down":
            self.image = pygame.transform.rotate(self.original_image, 180)
            self.rect = self.image.get_rect(midbottom=(self.player_rect.centerx, self.player_rect.bottom))
        elif self.direction == "left":
            self.image = pygame.transform.rotate(self.original_image, 90)
            self.rect = self.image.get_rect(midleft=(self.player_rect.left, self.player_rect.centery))
        elif self.direction == "right":
            self.image = pygame.transform.rotate(self.original_image, 270)
            self.rect = self.image.get_rect(midright=(self.player_rect.right, self.player_rect.centery))

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        if self.rect.x < 0 or self.rect.x > GAME_WIDTH or self.rect.y < 0 or self.rect.y > GAME_HEIGHT:
            self.kill()
            self.all_sprites.add(fire_Effect(self.rect.center))
            if self.is_player:
                pygame.mixer.Sound(SOUNDS["bullet_hit_border"]).play()


class Invincible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self._layer = 2
        frame1 = pygame.image.load(os.path.join(IMAGE_PATH, "player/invinsible1.png")).convert_alpha()
        frame2 = pygame.image.load(os.path.join(IMAGE_PATH, "player/invinsible2.png")).convert_alpha()
        self.animation_frames = [pygame.transform.scale(frame1, (2 * GRID_SIZE, 2 * GRID_SIZE)),
                                 pygame.transform.scale(frame2, (2 * GRID_SIZE, 2 * GRID_SIZE))]
        self.animation_index = 0
        self.last_animation_update = pygame.time.get_ticks()
        self.image = self.animation_frames[self.animation_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_update > 100:
            self.last_animation_update = current_time
            self.animation_index = (self.animation_index + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.animation_index]
