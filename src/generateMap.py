import os.path

from objects import *
from settings import *
import csv


def B(x=0, y=0, X=(0, 1), Y=(0, 1), all_sprites=None, bricks_group=None, surface=None):
    for YY in Y:
        for XX in X:
            for i in range(2):
                for j in range(2):
                    brick = Bricks((x * 2 + XX) * GRID_SIZE, (y * 2 + YY) * GRID_SIZE, j, i)
                    if all_sprites is not None:
                        all_sprites.add(brick)
                    if bricks_group is not None:
                        bricks_group.add(brick)
                    if surface is not None:
                        surface.blit(brick.image, brick.rect)
    if surface is not None:
        return surface
    else:
        return None


def S(x=0, y=0, X=(0, 1), Y=(0, 1), all_sprites=None, stone_group=None, surface=None):
    for YY in Y:
        for XX in X:
            stone = Stone((x * 2 + XX) * GRID_SIZE, (y * 2 + YY) * GRID_SIZE)
            if all_sprites is not None:
                all_sprites.add(stone)
            if stone_group is not None:
                stone_group.add(stone)
            if surface is not None:
                surface.blit(stone.image, stone.rect)
    if surface is not None:
        return surface
    else:
        return None


def F(x=0, y=0, X=(0, 1), Y=(0, 1), all_sprites=None, forest_group=None, surface=None):
    for YY in Y:
        for XX in X:
            forest = Forest((x * 2 + XX) * GRID_SIZE, (y * 2 + YY) * GRID_SIZE)
            if all_sprites is not None:
                all_sprites.add(forest)
            if forest_group is not None:
                forest_group.add(forest)
            if surface is not None:
                surface.blit(forest.image, forest.rect)
    if surface is not None:
        return surface
    else:
        return None

def SN(x=0, y=0, X=(0, 1), Y=(0, 1), all_sprites=None, snowfield_group=None, surface=None):
    for YY in Y:
        for XX in X:
            snowfield = Snowfield((x * 2 + XX) * GRID_SIZE, (y * 2 + YY) * GRID_SIZE)
            if all_sprites is not None:
                all_sprites.add(snowfield)
            if snowfield_group is not None:
                snowfield_group.add(snowfield)
            if surface is not None:
                surface.blit(snowfield.image, snowfield.rect)
    if surface is not None:
        return surface
    else:
        return None


def W(x=0, y=0, X=(0, 1), Y=(0, 1), all_sprites=None, water_group=None, surface=None):
    for YY in Y:
        for XX in X:
            water = Water((x * 2 + XX) * GRID_SIZE, (y * 2 + YY) * GRID_SIZE)
            if all_sprites is not None:
                all_sprites.add(water)
            if water_group is not None:
                water_group.add(water)
            if surface is not None:
                surface.blit(water.image, water.rect)
    if surface is not None:
        return surface
    else:
        return None


def generate_map(all_sprites, level=1, bricks_group=None, stone_group=None, forest_group=None, water_group=None, snowfield_group=None):
    if not os.path.exists(os.path.join(LEVEL_PATH, f"level{level}.csv")):
        return False

    # 加载地图数据
    with open(os.path.join(LEVEL_PATH, f"level{level}.csv"), "r", newline='') as file:
        csv_reader = csv.reader(file)

        for y, row in enumerate(csv_reader):
            if y >= 13:  # 只读取前13行
                break
            for x, cell in enumerate(row[:13]):
                if cell == "B":  # 砖块
                    B(x, y, (0, 1), (0, 1), all_sprites, bricks_group)

                elif cell == "BU":  # 砖块
                    B(x, y, (0, 1), (0,), all_sprites, bricks_group)

                elif cell == "BD":  # 砖块
                    B(x, y, (0, 1), (1,), all_sprites, bricks_group)

                elif cell == "BL":  # 砖块
                    B(x, y, (0,), (0, 1), all_sprites, bricks_group)

                elif cell == "BR":  # 砖块
                    B(x, y, (1,), (0, 1), all_sprites, bricks_group)

                elif cell == "S":  # 石头
                    S(x, y, (0, 1), (0, 1), all_sprites, stone_group)

                elif cell == "SU":  # 石头
                    S(x, y, (0, 1), (0,), all_sprites, stone_group)

                elif cell == "SD":  # 石头
                    S(x, y, (0, 1), (1,), all_sprites, stone_group)

                elif cell == "SL":  # 石头
                    S(x, y, (0,), (0, 1), all_sprites, stone_group)

                elif cell == "SR":  # 石头
                    S(x, y, (1,), (0, 1), all_sprites, stone_group)

                elif cell == "F":  # 森林
                    F(x, y, (0, 1), (0, 1), all_sprites, forest_group)
                
                elif cell == "SN":  # 雪
                    SN(x, y, (0, 1), (0, 1), all_sprites, snowfield_group)

                elif cell == "W":  # 水
                    W(x, y, (0, 1), (0, 1), all_sprites, water_group)
    return True


def add_defense_brick(all_sprites, bricks_group):
    x, y = 5, 11
    B(x, y, (1,), (1,), all_sprites, bricks_group)

    x, y = 6, 11
    B(x, y, (0, 1), (1,), all_sprites, bricks_group)

    x, y = 7, 11
    B(x, y, (0,), (1,), all_sprites, bricks_group)

    x, y = 5, 12
    B(x, y, (1,), (0, 1), all_sprites, bricks_group)

    x, y = 7, 12
    B(x, y, (0,), (0, 1), all_sprites, bricks_group)


def add_defense_stone(all_sprites, stone_group):
    x, y = 5, 11
    S(x, y, (1,), (1,), all_sprites, stone_group)

    x, y = 6, 11
    S(x, y, (0, 1), (1,), all_sprites, stone_group)

    x, y = 7, 11
    S(x, y, (0,), (1,), all_sprites, stone_group)

    x, y = 5, 12
    S(x, y, (1,), (0, 1), all_sprites, stone_group)

    x, y = 7, 12
    S(x, y, (0,), (0, 1), all_sprites, stone_group)
