import pygame


# 全局游戏时间管理器
class GameTimeManager:
    def __init__(self):
        self.start_time = 0
        self.game_time = 0
        self.paused_time = 0
        self.paused = False
    
    def start(self):
        """开始游戏时间计数"""
        self.start_time = pygame.time.get_ticks()
        self.paused_time = 0
        self.paused = False

    def get_game_time(self):
        """获取当前游戏时间（考虑暂停）"""
        if self.paused:
            return self.paused_time
        else:
            return pygame.time.get_ticks() - self.start_time

    def pause(self):
        """暂停游戏时间计数"""
        self.paused = True
        self.paused_time = pygame.time.get_ticks() - self.start_time
    
    def unpause(self):
        """继续游戏时间计数"""
        self.paused = False
        self.start_time = pygame.time.get_ticks() - self.paused_time

    def reset(self):
        """重置游戏时间管理器，用于新游戏开始"""
        self.start_time = 0
        self.game_time = 0
        self.paused_time = 0
        self.paused = False


# 创建全局游戏时间管理器实例
game_time_manager = GameTimeManager()