from settings import *
import sys
from brick_logo import BrickLogo


class Menu:
    def __init__(self, screen):
        self.current_time = None
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.menu_selected = 1
        self.stage_selected = 1
        self.press_down_time = None
        self.press_up_time = None

        # 创建砖块LOGO
        self.brick_logo = BrickLogo(screen)
        self.brick_logo.create_brick_field()

    def draw_menu_selection(self):
        # 绘制砖块LOGO
        self.brick_logo.draw()

        # 绘制菜单选项
        font = pygame.font.Font(os.path.join(FONT_PATH, "ARCADECLASSIC-1.ttf"), 36)
        text1 = font.render("1 player", True, COLORS["WHITE"])
        text2 = font.render("2 players", True, COLORS["WHITE"])
        text3 = font.render("1player and PC", True, COLORS["WHITE"])
        text4 = font.render("Construction", True, COLORS["WHITE"])
        text5 = font.render("Exit", True, COLORS["WHITE"])
        rect1 = text1.get_rect()
        rect2 = text2.get_rect()
        rect3 = text3.get_rect()
        rect4 = text4.get_rect()
        rect5 = text5.get_rect()
        rect1.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100)
        rect2.topleft = (rect1[0], rect1[1] + 50)
        rect3.topleft = (rect2[0], rect2[1] + 50)
        rect4.topleft = (rect3[0], rect3[1] + 50)
        rect5.topleft = (rect4[0], rect4[1] + 50)
        self.screen.blit(text1, rect1)
        self.screen.blit(text2, rect2)
        self.screen.blit(text3, rect3)
        self.screen.blit(text4, rect4)
        self.screen.blit(text5, rect5)
        original_image = pygame.image.load(os.path.join(IMAGE_PATH, "player/player1_1_1.png"))
        image = pygame.transform.scale(original_image, (25, 25))
        image = pygame.transform.rotate(image, -90)
        image_rect = image.get_rect()
        if self.menu_selected == 1:
            image_rect.center = (rect1.midleft[0] - 30, rect1.midleft[1])
        elif self.menu_selected == 2:
            image_rect.center = (rect2.midleft[0] - 30, rect2.midleft[1])
        elif self.menu_selected == 3:
            image_rect.center = (rect3.midleft[0] - 30, rect3.midleft[1])
        elif self.menu_selected == 4:
            image_rect.center = (rect4.midleft[0] - 30, rect4.midleft[1])
        elif self.menu_selected == 5:
            image_rect.center = (rect5.midleft[0] - 30, rect5.midleft[1])
        self.screen.blit(image, image_rect)

    def run_menu_selection(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.menu_selected -= 1
                        if self.menu_selected < 1:
                            self.menu_selected = 5
                    if event.key == pygame.K_DOWN:
                        self.menu_selected += 1
                        if self.menu_selected > 5:
                            self.menu_selected = 1
                    if event.key == pygame.K_RETURN:
                        return self.menu_selected
            self.screen.fill(COLORS["BLACK"])
            self.draw_menu_selection()
            pygame.display.flip()
            self.clock.tick(60)

    def draw_stage(self, level):
        font = pygame.font.Font(os.path.join(FONT_PATH, "ARCADECLASSIC-1.ttf"), 36)
        text = font.render(f"Stage {level}", True, COLORS["BLACK"])
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.screen.blit(text, text_rect)

    def run_select_stage(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.stage_selected += 1
                        self.press_up_time = pygame.time.get_ticks()
                    if event.key == pygame.K_DOWN:
                        self.stage_selected -= 1
                        if self.stage_selected < 1:
                            self.stage_selected = 1
                        self.press_down_time = pygame.time.get_ticks()
                    if event.key == pygame.K_RETURN:
                        return self.stage_selected
                    
            self.current_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                if self.current_time - self.press_up_time > 500:
                    self.stage_selected += 1
            if keys[pygame.K_DOWN]:
                if self.current_time - self.press_down_time > 500:
                    self.stage_selected -= 1
                    if self.stage_selected < 1:
                        self.stage_selected = 1
            self.screen.fill((200, 200, 200))
            self.draw_stage(self.stage_selected)
            pygame.display.flip()
            self.clock.tick(60)

    def run_level_interface(self, level, start_time):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill((200, 200, 200))
            self.draw_stage(level)
            if pygame.time.get_ticks() - start_time > 1000:
                return
            pygame.display.flip()
            self.clock.tick(60)