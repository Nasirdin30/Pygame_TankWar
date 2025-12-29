import sys
from awards import *
from draws import *
from enemies import *
from generateMap import *
from player import *
from game_time_manager import game_time_manager

# 初始化Pygame
pygame.init()

game_surface = pygame.Surface((GAME_WIDTH, GAME_WIDTH), pygame.SRCALPHA)
pygame.display.set_caption("TANK")
clock = pygame.time.Clock()


class Game:
    def __init__(self, screen, player_mode="1P", level=1, player1_life=3, player2_life=3, player1_lv=1, player2_lv=1,
                 edit_sprites=None, PC_player2=False):
        self.screen = screen
        self.player_mode = player_mode
        self.PC_player2 = PC_player2
        self.level = level
        self.running = True
        self.paused = False
        self.game_time = 0
        self.paused_time = 0
        # 重置全局游戏时间管理器
        game_time_manager.reset()
        game_time_manager.start()

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.bricks_group = pygame.sprite.Group()
        self.stone_group = pygame.sprite.Group()
        self.forest_group = pygame.sprite.Group()
        self.snowfield_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.player1_bullets = pygame.sprite.Group()
        self.protection = pygame.sprite.Group()
        self.awards = pygame.sprite.Group()
        self.game_objects = {
            "bricks": self.bricks_group,
            "stone": self.stone_group,
            "forest": self.forest_group,
            "snowfield": self.snowfield_group,
            "water": self.water_group,
            "enemies": self.enemy_group,
            "awards": self.awards
        }
        self.player1 = Player1(all_sprites=self.all_sprites,
                               lv=player1_lv,
                               bullets=self.player1_bullets,
                               game_objects=self.game_objects,
                               life=player1_life)
        self.player2 = pygame.sprite.Group()
        self.player2_bullets = pygame.sprite.Group()
        if self.player_mode == "2P":
            if self.PC_player2:
                print("developing")
            else:
                self.player2 = Player2(all_sprites=self.all_sprites,
                                   lv=player2_lv,
                                   bullets=self.player2_bullets,
                                   game_objects=self.game_objects,
                                   life=player2_life)
            self.all_sprites.add(self.player2)
        self.all_sprites.add(self.player1)
        self.edit_sprites = edit_sprites
        self.enemy_position = [(0, 0), (6, 0), (12, 0)]
        self.protect = None
        self.generate_map()
        self.max_enemy_spawn = 8
        self.enemies = self.enemy_list()
        self.enemy_freeze = False
        self.enemy_freeze_end_time = 0
        self.stone_defense = False
        self.stone_defense_end_time = 0
        self.over_the_end = False
        self.over_the_end_time = 0
        self.game_ending_result = ""  # win / lose
        self.player1_score = 0
        self.player2_score = 0
        self.player1_kill_list = []
        self.player2_kill_list = []
        self.game_information = None
        pygame.mixer.Sound(SOUNDS["game_start"]).play()

    def enemy_list(self):
        enemy_list = []
        for _ in range(30):
            enemy_type = random.choice([1, 2, 3, 4])
            enemy_health = random.randint(1, 5)
            is_award = random.random() < 0.3
            enemy_list.append({"type": enemy_type, "health": enemy_health, "award": is_award})
        return enemy_list

    def generate_protection(self):
        self.protect = Protect(x=13 * GRID_SIZE, y=25 * GRID_SIZE, all_sprites=self.all_sprites)
        self.protection.add(self.protect)
        self.all_sprites.add(self.protect)

    def generate_enemy(self):
        if len(self.enemies) == 0:
            return
        if len(self.enemy_group) < self.max_enemy_spawn:
            enemy_information = self.enemies.pop(0)
            pos = self.enemy_position.pop(0)
            enemy = Enemy(all_sprites=self.all_sprites,
                          type=enemy_information["type"],
                          x=(1 * GRID_SIZE) + pos[0] * GRID_SIZE * 2,
                          y=pos[1] * GRID_SIZE * 2 + (1 * GRID_SIZE),
                          health=enemy_information["health"],
                          award=enemy_information["award"],
                          bullets=self.enemy_bullets,
                          game_objects=self.game_objects,
                          freezed=self.enemy_freeze)
            self.enemy_group.add(enemy)
            self.all_sprites.add(enemy)
            self.enemy_position.append(pos)

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
            for snowfield in self.snowfield_group:
                if snowfield.rect.colliderect(rect):
                    snowfield.kill()

    def kill_bricks(self, bullet, bricks):
        if bullet.direction == "up" or bullet.direction == "down":
            kill_bricks = set()
            for brick in bricks:
                new_bricks = [(brick.rect.x, brick.rect.y),
                              (brick.rect.x + brick.rect.width, brick.rect.y),
                              (brick.rect.x - brick.rect.width, brick.rect.y)]
                for new_brick in new_bricks:
                    for target_brick in self.bricks_group:
                        if target_brick.rect.x == new_brick[0] and target_brick.rect.y == new_brick[1]:
                            kill_bricks.add(target_brick)
            for brick in kill_bricks:
                brick.kill()
        elif bullet.direction == "left" or bullet.direction == "right":
            kill_bricks = set()
            for brick in bricks:
                new_bricks = [(brick.rect.x, brick.rect.y),
                              (brick.rect.x, brick.rect.y + brick.rect.width),
                              (brick.rect.x, brick.rect.y - brick.rect.width)]
                for new_brick in new_bricks:
                    for target_brick in self.bricks_group:
                        if target_brick.rect.x == new_brick[0] and target_brick.rect.y == new_brick[1]:
                            kill_bricks.add(target_brick)
            for brick in kill_bricks:
                brick.kill()

    def run(self):
        while self.running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == CONTROLS["pause"]:
                        if not self.over_the_end:
                            if self.paused:
                                self.paused = False
                                # 更新全局游戏时间管理器
                                game_time_manager.unpause()
                            else:
                                pygame.mixer.Sound(SOUNDS["pause"]).play()
                                self.paused = True
                                self.paused_time = pygame.time.get_ticks()
                                # 更新全局游戏时间管理器
                                game_time_manager.pause()
                    if event.key == CONTROLS["player1"]["B"] and not self.paused:
                        self.player1.shoot()
                    if self.player_mode == "2P" or self.player_mode == "1P_PC":
                        if event.key == CONTROLS["player2"]["B"] and not self.paused:
                            self.player2.shoot()

            self.generate_enemy()

            if not self.paused:

                self.game_time = game_time_manager.get_game_time()

                self.timers()

                self.check_player1_bullet_hit_bricks()
                self.check_player1_bullet_hit_stone()
                self.check_player1_bullet_hit_enemy()
                self.player1_pickup_award()
                self.check_enemy_bullet_hit_player1()
                pygame.sprite.groupcollide(self.player1_bullets, self.enemy_bullets, True, True)
                if self.player_mode == "2P" or self.player_mode == "1P_PC":
                    pygame.sprite.groupcollide(self.player1_bullets, self.player2_bullets, True, True)
                    pygame.sprite.groupcollide(self.player2_bullets, self.enemy_bullets, True, True)

                    self.check_player2_bullet_hit_bricks()
                    self.check_player2_bullet_hit_stone()
                    self.check_player2_bullet_hit_enemy()
                    self.player2_pickup_award()
                    self.check_enemy_bullet_hit_player2()

                self.check_protect_is_hit()

                self.check_enemy_bullet_hit_bricks()
                self.check_enemy_bullet_hit_stone()

                self.check_game_ending()
                if self.game_end():
                    return self.game_information

                self.screen.fill((200, 200, 200))

                self.all_sprites.update()
                game_surface.fill(COLORS["BLACK"])

                self.all_sprites.draw(game_surface)
                if self.player_mode == "1P":
                    draw_player_life(self.screen, self.player_mode, self.player1.live)
                elif self.player_mode == "2P" or self.player_mode == "1P_PC":
                    draw_player_life(self.screen, self.player_mode, self.player1.live, self.player2.live)
                draw_enemy_count(self.screen, len(self.enemies))
                draw_time(self.screen, self.game_time)
                self.screen.blit(game_surface, (10, 10))
                pygame.display.flip()
            else:
                self.game_time = game_time_manager.get_game_time()

    def generate_map(self):
        if self.edit_sprites is not None:
            self.bricks_group.add(self.edit_sprites["bricks"])
            self.stone_group.add(self.edit_sprites["stone"])
            self.forest_group.add(self.edit_sprites["forest"])
            self.snowfield_group.add(self.edit_sprites["snowfield"])
            self.water_group.add(self.edit_sprites["water"])
            self.all_sprites.add(self.edit_sprites["bricks"])
            self.all_sprites.add(self.edit_sprites["stone"])
            self.all_sprites.add(self.edit_sprites["forest"])
            self.all_sprites.add(self.edit_sprites["snowfield"])
            self.all_sprites.add(self.edit_sprites["water"])
        else:
            result = generate_map(all_sprites=self.all_sprites,
                                  level=self.level,
                                  bricks_group=self.bricks_group,
                                  stone_group=self.stone_group,
                                  forest_group=self.forest_group,
                                  snowfield_group=self.snowfield_group,
                                  water_group=self.water_group)
            if not result:
                if self.level == 1:
                    print("error: please add level.")
                else:
                    self.level = 1
                    self.generate_map()
            self.clear_grid([(5, 11), (6, 11), (7, 11), (5, 12), (6, 12), (7, 12)])
            add_defense_brick(self.all_sprites, self.bricks_group)
        self.clear_grid([(4, 12), (6, 12), (8, 12)])
        self.generate_protection()
        self.clear_grid(self.enemy_position)

    def check_player1_bullet_hit_bricks(self):
        brick_hits = pygame.sprite.groupcollide(self.player1_bullets, self.bricks_group, True, False)
        for bullet, bricks in brick_hits.items():
            self.all_sprites.add(fire_Effect(bullet.rect.center))
            pygame.mixer.Sound(SOUNDS["kill_bricks"]).play()
            self.kill_bricks(bullet, bricks)

    def check_player1_bullet_hit_stone(self):
        stone_hits = pygame.sprite.groupcollide(self.player1_bullets, self.stone_group, True, False)
        for bullet, stones in stone_hits.items():
            self.all_sprites.add(fire_Effect(bullet.rect.center))

    def check_player1_bullet_hit_enemy(self):
        enemy_hits = pygame.sprite.groupcollide(self.player1_bullets, self.enemy_group, True, False)
        for bullet, enemies in enemy_hits.items():
            enemy = enemies[0]
            if enemy.award:
                for award in self.awards:
                    award.kill()
                self.awards.empty()
                award_type = random.choice([1, 2, 3, 4, 5, 6])
                x = random.randint(1, 25) * GRID_SIZE
                y = random.randint(1, 25) * GRID_SIZE
                award = Award(x=x, y=y, type=award_type)
                self.awards.add(award)
                self.all_sprites.add(award)
                pygame.mixer.Sound(SOUNDS["award_appear"]).play()
            if enemy.hit():
                self.player1_score += enemy.bonus
                self.player1_kill_list.append(enemy.type)
                self.all_sprites.add(score_Effect(enemy.rect.center, enemy.bonus, duration=1000))
                pygame.mixer.Sound(SOUNDS["enemy_explosion"]).play()
            else:
                if not enemy.award:
                    pygame.mixer.Sound(SOUNDS["bullet_hit_armor"]).play()

    def check_enemy_bullet_hit_player1(self):
        if self.player1.alive():
            enemy_bullet_hits_p1 = pygame.sprite.spritecollide(self.player1, self.enemy_bullets, True)
            if enemy_bullet_hits_p1:
                self.player1.hit()

    def check_protect_is_hit(self):
        if not self.protect.is_destroyed:
            if (pygame.sprite.groupcollide(self.player1_bullets, self.protection, True, False) or
                    pygame.sprite.groupcollide(self.player2_bullets, self.protection, True, False) or
                    pygame.sprite.groupcollide(self.enemy_bullets, self.protection, True, False)):
                self.protect.destroyed()
                pygame.mixer.Sound(SOUNDS["protect_destroyed"]).play()

    def check_player2_bullet_hit_bricks(self):
        brick_hits = pygame.sprite.groupcollide(self.player2_bullets, self.bricks_group, True, False)
        for bullet, bricks in brick_hits.items():
            self.all_sprites.add(fire_Effect(bullet.rect.center))
            pygame.mixer.Sound(SOUNDS["kill_bricks"]).play()
            self.kill_bricks(bullet, bricks)

    def check_player2_bullet_hit_stone(self):
        stone_hits = pygame.sprite.groupcollide(self.player2_bullets, self.stone_group, True, False)
        for bullet, stones in stone_hits.items():
            self.all_sprites.add(fire_Effect(bullet.rect.center))

    def check_player2_bullet_hit_enemy(self):
        enemy_hits = pygame.sprite.groupcollide(self.player2_bullets, self.enemy_group, True, False)
        for bullet, enemies in enemy_hits.items():
            enemy = enemies[0]
            if enemy.award:
                for award in self.awards:
                    award.kill()
                self.awards.empty()
                award_type = random.choice([1, 2, 3, 4, 5, 6])
                x = random.randint(1, 25) * GRID_SIZE
                y = random.randint(1, 25) * GRID_SIZE
                award = Award(x=x, y=y, type=award_type)
                self.awards.add(award)
                self.all_sprites.add(award)
                pygame.mixer.Sound(SOUNDS["award_appear"]).play()
            if enemy.hit():
                self.player2_score += enemy.bonus
                self.player2_kill_list.append(enemy.type)
                self.all_sprites.add(score_Effect(enemy.rect.center, enemy.bonus, duration=1000))
                pygame.mixer.Sound(SOUNDS["enemy_explosion"]).play()
            else:
                if not enemy.award:
                    pygame.mixer.Sound(SOUNDS["bullet_hit_armor"]).play()

    def check_enemy_bullet_hit_player2(self):
        if self.player2.alive():
            enemy_bullet_hits_p2 = pygame.sprite.spritecollide(self.player2, self.enemy_bullets, True)
            if enemy_bullet_hits_p2:
                self.player2.hit()

    def check_enemy_bullet_hit_bricks(self):
        brick_hits = pygame.sprite.groupcollide(self.enemy_bullets, self.bricks_group, True, False)
        for bullet, bricks in brick_hits.items():
            self.kill_bricks(bullet, bricks)

    def check_enemy_bullet_hit_stone(self):
        pygame.sprite.groupcollide(self.enemy_bullets, self.stone_group, True, False)

    def _pickup_award(self, player, player_type):
        hits = pygame.sprite.spritecollide(player, self.awards, True)
        if hits:
            for award in hits:
                standard_sound = True
                if award.type == 1:
                    self.clear_grid([(5, 11), (6, 11), (7, 11), (5, 12), (6, 12), (7, 12)])
                    add_defense_stone(self.all_sprites, self.stone_group)
                    self.stone_defense = True
                    self.stone_defense_end_time = self.game_time + 20000
                elif award.type == 2:
                    player.level_up()
                elif award.type == 3:
                    self.enemy_freeze = True
                    self.enemy_freeze_end_time = self.game_time + 10000
                    for enemy in self.enemy_group:
                        enemy.freezed = self.enemy_freeze
                elif award.type == 4:
                    player.set_invincible(10000)
                elif award.type == 5:
                    for enemy in self.enemy_group:
                        enemy.kill()
                        self.all_sprites.add(ExplodeEffect(enemy.rect.center))
                    pygame.mixer.Sound(SOUNDS["enemy_explosion"]).play()
                elif award.type == 6:
                    standard_sound = False
                    pygame.mixer.Sound(SOUNDS["health_up"]).play()
                    player.live += 1
                if standard_sound:
                    pygame.mixer.Sound(SOUNDS["pickup_award"]).play()

            # 更新分数
            if player_type == "player1":
                self.player1_score += 500
            else:
                self.player2_score += 500

            self.all_sprites.add(score_Effect(award.rect.center, 500))

    def player1_pickup_award(self):
        self._pickup_award(self.player1, "player1")

    def player2_pickup_award(self):
        self._pickup_award(self.player2, "player2")

    def check_game_ending(self):
        if self.player_mode == "1P":
            if not self.player1.alive() and not self.over_the_end:
                self.over_the_end = True
                self.over_the_end_time = self.game_time
                self.game_ending_result = "lose"
        elif self.player_mode == "2P" or self.player_mode == "1P_PC":
            if not self.player1.alive() and not self.player2.alive() and not self.over_the_end:
                self.over_the_end = True
                self.over_the_end_time = self.game_time
                self.game_ending_result = "lose"

        if self.protect.is_destroyed:
            self.game_ending_result = "lose"
            self.player1.can_control = False
            if self.player_mode == "2P" or self.player_mode == "1P_PC":
                self.player2.can_control = False
            if not self.over_the_end:
                self.over_the_end = True
                self.over_the_end_time = self.game_time
                self.all_sprites.add(game_over_Effect())

        if len(self.enemy_group) <= 0 and len(self.enemies) == 0 and not self.over_the_end:
            self.over_the_end = True
            self.over_the_end_time = self.game_time
            self.game_ending_result = "win"

    def game_end(self):
        if self.over_the_end and self.game_time - self.over_the_end_time >= 3000:
            self.running = False
            player1 = {
                "score": self.player1_score,
                "kill_list": self.player1_kill_list,
                "life": self.player1.live,
                "lv": self.player1.lv
            }
            if self.player_mode == "2P" or self.player_mode == "1P_PC":
                player2 = {
                    "score": self.player2_score,
                    "kill_list": self.player2_kill_list,
                    "life": self.player2.live,
                    "lv": self.player2.lv
                }
            else:
                player2 = {
                    "score": 0,
                    "kill_list": [],
                    "life": 0,
                    "lv": 0
                }
            self.game_information = {
                "game_ending_result": self.game_ending_result,
                "level": self.level,
                "player1": player1,
                "player2": player2,
            }
            return True

    def timers(self):
        if self.stone_defense and self.game_time > self.stone_defense_end_time:
            self.stone_defense = False
            self.clear_grid([(5, 11), (6, 11), (7, 11), (5, 12), (6, 12), (7, 12)])
            add_defense_brick(self.all_sprites, self.bricks_group)

        if self.enemy_freeze and self.game_time > self.enemy_freeze_end_time:
            self.enemy_freeze = False
            for enemy in self.enemy_group:
                enemy.freezed = self.enemy_freeze