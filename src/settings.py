import pygame
import os

# 获取项目根目录路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 资源路径常量
IMAGE_PATH = os.path.join(PROJECT_ROOT, "image")
SOUND_PATH = os.path.join(PROJECT_ROOT, "sound")
FONT_PATH = os.path.join(PROJECT_ROOT, "font")
LEVEL_PATH = os.path.join(PROJECT_ROOT, "level")


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800

GAME_WIDTH = 780
GAME_HEIGHT = 780

GRID = 26
GRID_SIZE = GAME_WIDTH / GRID

FPS = 60

CONTROLS = {
    "pause": pygame.K_p,
    "player1": {
        "up": pygame.K_w,
        "down": pygame.K_s,
        "left": pygame.K_a,
        "right": pygame.K_d,
        "A": pygame.K_SPACE,
        "B": pygame.K_c
    },
    "player2": {
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "A": pygame.K_KP_0,
        "B": pygame.K_KP_1
    }
}

COLORS = {
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "GREEN": (0, 255, 0),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "PURPLE": (255, 0, 255),
    "ORANGE": (255, 127, 0),
    "GRAY": (127, 127, 127),
    "CYAN": (0, 255, 255)
}

SOUNDS = {
    "enemy_explosion": os.path.join(SOUND_PATH, "enemy_explode.mp3"),
    "shoot": os.path.join(SOUND_PATH, "player_shoot.mp3"),
    "bullet_hit_border": os.path.join(SOUND_PATH, "bullet_hit_border.mp3"),
    "bullet_hit_armor": os.path.join(SOUND_PATH, "bullet_hit_armor.mp3"),
    "award_appear": os.path.join(SOUND_PATH, "award_appear.mp3"),
    "kill_bricks": os.path.join(SOUND_PATH, "kill_bricks.mp3"),
    "pickup_award": os.path.join(SOUND_PATH, "pick_up_award.mp3"),
    "health_up": os.path.join(SOUND_PATH, "health_up.mp3"),
    "player_explode": os.path.join(SOUND_PATH, "player_explode.mp3"),
    "pause": os.path.join(SOUND_PATH, "pause.mp3"),
    "protect_destroyed": os.path.join(SOUND_PATH, "protect_destroyed.mp3"),
    "game_start": os.path.join(SOUND_PATH, "game_start.mp3")
}
