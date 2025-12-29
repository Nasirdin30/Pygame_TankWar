from settings import *


def draw_player_life(screen, player_mode, player1_life, player2_life=None):
    font = pygame.font.Font(os.path.join(FONT_PATH, "ARCADECLASSIC-1.ttf"), 36)
    player1_text1 = font.render("P 1", True, COLORS["BLACK"])
    player1_text2 = font.render(f"{player1_life}", True, COLORS["BLACK"])
    player1_text1_rect = player1_text1.get_rect(topright=(SCREEN_WIDTH, 500))
    player1_text2_rect = player1_text2.get_rect(topright=(SCREEN_WIDTH, 550))
    screen.blit(player1_text1, player1_text1_rect)
    screen.blit(player1_text2, player1_text2_rect)
    if player_mode == "2P":
        player2_text1 = font.render("P 2", True, COLORS["BLACK"])
        player2_text2 = font.render(f"{player2_life}", True, COLORS["BLACK"])
        player2_text1_rect = player2_text1.get_rect(topright=(SCREEN_WIDTH, 600))
        player2_text2_rect = player2_text2.get_rect(topright=(SCREEN_WIDTH, 650))
        screen.blit(player2_text1, player2_text1_rect)
        screen.blit(player2_text2, player2_text2_rect)


def draw_enemy_count(screen, enemy_count):
    thumbnail = pygame.image.load(os.path.join(IMAGE_PATH, "enemy/thumbnail.png"))
    scaled_width = 20
    space = 5
    scaled_height = thumbnail.get_height() * scaled_width / thumbnail.get_width()
    thumbnail = pygame.transform.scale(thumbnail, (scaled_width, scaled_height))
    for i in range(enemy_count // 3 + 1):
        for j in range(3):
            if i * 3 + j >= enemy_count:
                break
            thumbnail_rect = thumbnail.get_rect(topleft=(GAME_WIDTH + 30 + j * (scaled_width + space),
                                                         10 + i * (scaled_height + space)))
            screen.blit(thumbnail, thumbnail_rect)


def draw_time(screen, time):
    font = pygame.font.Font(os.path.join(FONT_PATH, "ARCADECLASSIC-1.ttf"), 36)
    text = time // 1000
    render_text = font.render(str(text), True, COLORS["BLACK"])
    render_text_rect = render_text.get_rect(topright=(SCREEN_WIDTH, 300))
    screen.blit(render_text, render_text_rect)
