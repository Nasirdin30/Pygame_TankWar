from settings import *
from objects import Bricks2
import pygame
import os


class BrickLogo:
    def __init__(self, screen):
        self.screen = screen
        self.brick_group = pygame.sprite.Group()

        # 定义LOGO区域（主菜单上方）
        self.logo_area_width = SCREEN_WIDTH
        self.logo_area_height = 500
        self.logo_area_x = 0
        self.logo_area_y = 0

        # 砖块网格参数
        self.brick_size = GRID_SIZE  # 每个砖块的大小
        self.bricks_per_row = self.logo_area_width // self.brick_size
        self.bricks_per_col = self.logo_area_height // self.brick_size

        # 文字LOGO参数
        self.text = "BATTLE\nCITY"
        self.font_size = int(7 * self.brick_size)
        self.text_color = COLORS["YELLOW"]
        self.show_text = True  # 调试阶段显示文字
        self.text_line_spacing = 0
        self.font = pygame.font.Font(os.path.join(FONT_PATH, "ARCADECLASSIC-1.ttf"), self.font_size)
        self.text_center_x = SCREEN_WIDTH // 2
        self.text_center_y = self.logo_area_y + self.font_size // 2

        # 文字掩码参数
        self.text_mask_created = False
        self.text_mask_surface = None

    def create_text_mask(self):
        """创建文字掩码，用于检测砖块是否在文字范围内"""
        # 创建一个与屏幕相同大小的透明表面
        self.text_mask_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # 渲染多行文字到掩码表面
        lines = self.text.split('\n')
        total_height = len(lines) * self.font_size

        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, (255, 255, 255, 255))  # 白色不透明
            text_rect = text_surface.get_rect()

            # 计算每行文字的位置（居中显示）
            text_rect.centerx = self.text_center_x
            text_rect.centery = self.text_center_y + i * self.font_size + self.text_line_spacing * i

            # 将文字绘制到掩码表面
            self.text_mask_surface.blit(text_surface, text_rect)

        self.text_mask_created = True

    def is_brick_in_text(self, brick_rect):
        """检测砖块是否在文字范围内"""
        if not self.text_mask_created:
            self.create_text_mask()

        # 检查砖块矩形区域是否与文字相交
        for x in range(brick_rect.left, brick_rect.right, 2):  # 采样检测，提高性能
            for y in range(brick_rect.top, brick_rect.bottom, 2):
                if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
                    # 获取该像素点的alpha值
                    pixel_color = self.text_mask_surface.get_at((x, y))
                    if pixel_color[3] > 0:  # 如果alpha值大于0，表示在文字范围内
                        return True
        return False

    def create_brick_field(self):
        """创建砖块区域，只保留与文字相交的砖块"""
        self.brick_group.empty()

        # 先创建文字掩码
        self.create_text_mask()

        for row in range(int(self.bricks_per_col)):
            for col in range(int(self.bricks_per_row)):
                # 计算砖块位置
                x = self.logo_area_x + col * self.brick_size
                y = self.logo_area_y + row * self.brick_size

                for Y in range(2):
                    for X in range(2):
                        for i in range(2):
                            for j in range(2):
                                brick = Bricks2(x, y, j, i)

                                # 检查砖块是否在文字范围内
                                if self.is_brick_in_text(brick.rect):
                                    self.brick_group.add(brick)

    def draw_text_logo(self):
        """在砖块上方绘制文字LOGO"""
        if self.show_text:
            # 渲染多行文字
            lines = self.text.split('\n')
            total_height = len(lines) * self.font_size

            for i, line in enumerate(lines):
                text_surface = self.font.render(line, True, self.text_color)
                text_rect = text_surface.get_rect()

                # 计算每行文字的位置（居中显示）
                text_rect.centerx = self.text_center_x
                text_rect.centery = self.text_center_y + i * self.font_size + self.text_line_spacing * i

                # 绘制文字
                self.screen.blit(text_surface, text_rect)

    def draw(self):
        """绘制砖块LOGO"""
        self.brick_group.draw(self.screen)

        # 再绘制文字（在砖块上方）
        # self.draw_text_logo()

    def update(self):
        """更新砖块LOGO状态（如果需要动画）"""
        pass

    def toggle_text_visibility(self):
        """切换文字可见性（用于调试）"""
        self.show_text = not self.show_text

    def regenerate_brick_logo(self):
        """重新生成砖块LOGO（应用文字掩码）"""
        self.create_brick_field()
