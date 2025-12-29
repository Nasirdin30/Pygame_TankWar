from game import *
from menu import *
from edit_map import EditMap

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(pygame.image.load(os.path.join(IMAGE_PATH, "player/player1_1_1.png")))
pygame.display.set_caption("TANK")


def main():
    running = True
    sprites = None
    while running:
        menu = Menu(screen)
        main_selected = menu.run_menu_selection()
        if main_selected == 4:
            pygame.display.set_caption("EDIT")
            edit_map = EditMap(screen)
            sprites = edit_map.run()
        elif main_selected != 5:
            level = menu.run_select_stage()
            player1_life = 3
            player2_life = 3
            player1_lv = 3
            player2_lv = 3
            player1_total_score = 0
            player2_total_score = 0

            not_lose = True
            while not_lose:
                pygame.display.set_caption("TANK")
                if main_selected == 1:  # 单人模式
                    player_mode = "1P"
                    game = Game(screen, level=level, player_mode=player_mode, player1_life=player1_life,
                                player1_lv=player1_lv, edit_sprites=sprites)
                elif main_selected == 2:  # 双人模式
                    player_mode = "2P"
                    game = Game(screen, level=level, player_mode=player_mode, player1_life=player1_life,
                                player2_life=player2_life, player1_lv=player1_lv, player2_lv=player2_lv,
                                edit_sprites=sprites)
                elif main_selected == 3:  # 1player and PC模式
                    player_mode = "2P"
                    game = Game(screen, level=level, player_mode=player_mode, player1_life=player1_life,
                                player2_life=player2_life, player1_lv=player1_lv, player2_lv=player2_lv,
                                edit_sprites=sprites, PC_player2=True)
                game_information = game.run()
                print(game_information)
                sprites = None
                level = game_information["level"]
                player1_total_score += game_information["player1"]["score"]
                player2_total_score += game_information["player2"]["score"]
                player1_life = game_information["player1"]["life"]
                player2_life = game_information["player2"]["life"]
                player1_lv = game_information["player1"]["lv"]
                player2_lv = game_information["player2"]["lv"]
                if game_information["game_ending_result"] == "lose":
                    not_lose = False
                elif game_information["game_ending_result"] == "win":
                    level += 1
                    menu.run_level_interface(level, start_time=pygame.time.get_ticks())


        else:
            running = False


if __name__ == "__main__":
    main()
    pygame.quit()