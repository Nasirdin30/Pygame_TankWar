import sys
import csv
from generateMap import *

pygame.init()

game_surface = pygame.Surface((GAME_WIDTH, GAME_WIDTH), pygame.SRCALPHA)
clock = pygame.time.Clock()


class EditMap:
    def __init__(self, screen):
        self.screen = screen
        self.thumbnails = None
        self.running = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.bricks_group = pygame.sprite.Group()
        self.stone_group = pygame.sprite.Group()
        self.forest_group = pygame.sprite.Group()
        self.snowfield_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.grid_cursor_width = GRID_SIZE * 2
        self.grid_cursor_height = GRID_SIZE * 2
        self.grid_cursor_x = 0
        self.grid_cursor_y = 0
        self.last_click_position = None
        add_defense_brick(all_sprites=self.all_sprites, bricks_group=self.bricks_group)
        self.selected_object = None
        self.selected_object_type = "B"
        self.init_objects()
        self.csv_data = []
        self.init_csv()

    def run(self):
        while self.running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if event.button == 1:
                        if mouse_x > GAME_WIDTH + 10:
                            self.select_object(mouse_x, mouse_y)
                    elif event.button == 3:
                        self.selected_object_type = None
                        self.last_click_position = None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        with open(os.path.join(LEVEL_PATH, "level.csv"), "w", newline="") as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerows(self.csv_data)
                        sprites = {
                            "bricks": self.bricks_group,
                            "stone": self.stone_group,
                            "forest": self.forest_group,
                            "snowfield": self.snowfield_group,
                            "water": self.water_group,
                        }
                        return sprites

            self.screen.fill((200, 200, 200))
            self.all_sprites.update()
            game_surface.fill(COLORS["BLACK"])

            self.all_sprites.draw(game_surface)
            self.draw_thumbnails()
            self.draw_grid_cursor()
            self.screen.blit(game_surface, (10, 10))
            pygame.display.flip()

    def draw_grid_cursor(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if 10 < mouse_x < GAME_WIDTH + 10 and 10 < mouse_y < GAME_HEIGHT + 10:
            self.grid_cursor_x = int((mouse_x - 10) // (GRID_SIZE * 2))
            self.grid_cursor_y = int((mouse_y - 10) // (GRID_SIZE * 2))
            cursor_rect = pygame.Surface((self.grid_cursor_width, self.grid_cursor_height), pygame.SRCALPHA)
            cursor_rect.fill((255, 255, 255, 100))
            game_surface.blit(cursor_rect, (self.grid_cursor_x * GRID_SIZE * 2, self.grid_cursor_y * GRID_SIZE * 2))
            mouse_button = pygame.mouse.get_pressed()
            if mouse_button[0]:
                if self.last_click_position != (self.grid_cursor_x, self.grid_cursor_y):
                    self.clear_grid([(self.grid_cursor_x, self.grid_cursor_y)])
                    if self.selected_object_type == "B":
                        B(self.grid_cursor_x, self.grid_cursor_y, all_sprites=self.all_sprites,
                          bricks_group=self.bricks_group)
                        self.csv_data[self.grid_cursor_y][self.grid_cursor_x] = "B"
                    elif self.selected_object_type == "BU":
                        B(self.grid_cursor_x, self.grid_cursor_y, Y=(0,), all_sprites=self.all_sprites,
                          bricks_group=self.bricks_group)
                        self.csv_data[self.grid_cursor_y][self.grid_cursor_x] = "BU"
                    elif self.selected_object_type == "BD":
                        B(self.grid_cursor_x, self.grid_cursor_y, Y=(1,), all_sprites=self.all_sprites,
                          bricks_group=self.bricks_group)
                        self.csv_data[self.grid_cursor_y][self.grid_cursor_x] = "BD"
                    elif self.selected_object_type == "BL":
                        B(self.grid_cursor_x, self.grid_cursor_y, X=(0,), all_sprites=self.all_sprites,
                          bricks_group=self.bricks_group)
                        self.csv_data[self.grid_cursor_y][self.grid_cursor_x] = "BL"
                    elif self.selected_object_type == "BR":
                        B(self.grid_cursor_x, self.grid_cursor_y, X=(1,), all_sprites=self.all_sprites,
                          bricks_group=self.bricks_group)
                        self.csv_data[self.grid_cursor_y][self.grid_cursor_x] = "BR"
                    elif self.selected_object_type == "S":
                        S(self.grid_cursor_x, self.grid_cursor_y, all_sprites=self.all_sprites,
                          stone_group=self.stone_group)
                        self.csv_data[self.grid_cursor_y][self.grid_cursor_x] = "S"
                    elif self.selected_object_type == "SU":
                        S(self.grid_cursor_x, self.grid_cursor_y, Y=(0,), all_sprites=self.all_sprites,
                          stone_group=self.stone_group)
                        self.csv_data[self.grid_cursor_y][self.grid_cursor_x] = "SU"
                    elif self.selected_object_type == "SD":
                        S(self.grid_cursor_x, self.grid_cursor_y, Y=(1,), all_sprites=self.all_sprites,
                          stone_group=self.stone_group)
                        self.csv_data[self.grid_cursor_y][self.grid_cursor_x] = "SD"
                    elif self.selected_object_type == "SL":
                        S(self.grid_cursor_x, self.grid_cursor_y, X=(0,), all_sprites=self.all_sprites,
                          stone_group=self.stone_group)
                        self.csv_data[self.grid_cursor_y][self.grid_cursor_x] = "SL"
                    elif self.selected_object_type == "SR":
                        S(self.grid_cursor_x, self.grid_cursor_y, X=(1,), all_sprites=self.all_sprites,
                          stone_group=self.stone_group)
                        self.csv_data[self.grid_cursor_y][self.grid_cursor_x] = "SR"
                    elif self.selected_object_type == "F":
                        F(self.grid_cursor_x, self.grid_cursor_y, all_sprites=self.all_sprites,
                          forest_group=self.forest_group)
                        self.csv_data[self.grid_cursor_y][self.grid_cursor_x] = "F"
                    elif self.selected_object_type == "SN":
                        SN(self.grid_cursor_x, self.grid_cursor_y, all_sprites=self.all_sprites,
                          snowfield_group=self.snowfield_group)
                        self.csv_data[self.grid_cursor_y][self.grid_cursor_x] = "SN"
                    elif self.selected_object_type == "W":
                        W(self.grid_cursor_x, self.grid_cursor_y, all_sprites=self.all_sprites,
                          water_group=self.water_group)
                        self.csv_data[self.grid_cursor_y][self.grid_cursor_x] = "W"
                    else:
                        self.csv_data[self.grid_cursor_y][self.grid_cursor_x] = "0"
                    self.last_click_position = (self.grid_cursor_x, self.grid_cursor_y)

    def clear_grid(self, grid_positions):
        for x, y in grid_positions:
            rect = pygame.Rect(x * GRID_SIZE * 2, y * GRID_SIZE * 2, GRID_SIZE * 2, GRID_SIZE * 2)
            for brick in self.bricks_group:
                if brick.rect.colliderect(rect):
                    brick.kill()
            for stone in self.stone_group:
                if stone.rect.colliderect(rect):
                    stone.kill()
            for forest in self.forest_group:
                if forest.rect.colliderect(rect):
                    forest.kill()
            for water in self.water_group:
                if water.rect.colliderect(rect):
                    water.kill()

    def draw_thumbnails(self):
        for i, (key, value) in enumerate(self.thumbnails.items()):
            self.screen.blit(value, (GAME_WIDTH + 40, 10 + i * (GRID_SIZE * 2)))
            if self.selected_object_type == key:
                pygame.draw.rect(self.screen, COLORS["RED"],
                                 (GAME_WIDTH + 40, 10 + i * (GRID_SIZE * 2), GRID_SIZE * 2, GRID_SIZE * 2), 3)
            else:
                pygame.draw.rect(self.screen, COLORS["BLACK"],
                                 (GAME_WIDTH + 40, 10 + i * (GRID_SIZE * 2), GRID_SIZE * 2, GRID_SIZE * 2), 3)

    def init_objects(self):
        self.thumbnails = {
            "B": B(0, 0, surface=pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)),
            "BU": B(0, 0, Y=(0,), surface=pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)),
            "BD": B(0, 0, Y=(1,), surface=pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)),
            "BL": B(0, 0, X=(0,), surface=pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)),
            "BR": B(0, 0, X=(1,), surface=pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)),
            "S": S(0, 0, surface=pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)),
            "SU": S(0, 0, Y=(0,), surface=pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)),
            "SD": S(0, 0, Y=(1,), surface=pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)),
            "SL": S(0, 0, X=(0,), surface=pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)),
            "SR": S(0, 0, X=(1,), surface=pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)),
            "F": F(0, 0, surface=pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)),
            "SN": SN(0, 0, surface=pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA)),
            "W": W(0, 0, surface=pygame.Surface((GRID_SIZE * 2, GRID_SIZE * 2), pygame.SRCALPHA))
        }

    def select_object(self, mouse_x, mouse_y):
        for i, (key, value) in enumerate(self.thumbnails.items()):
            value_rect = pygame.Rect(GAME_WIDTH + 40, 10 + i * (GRID_SIZE * 2), GRID_SIZE * 2, GRID_SIZE * 2)
            if 10 < mouse_y < GAME_HEIGHT + 10:
                if value_rect.collidepoint(mouse_x, mouse_y):
                    self.selected_object_type = key
                    self.last_click_position = None
                    break

    def init_csv(self):
        # 初始化13x13的CSV数据矩阵
        self.csv_data = []
        for y in range(13):
            row = []
            for x in range(13):
                row.append("0")
            self.csv_data.append(row)