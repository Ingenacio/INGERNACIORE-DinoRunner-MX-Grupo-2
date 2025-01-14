import random
import pygame
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.utils.constants import (LARGE_CACTUS, SMALL_CACTUS, BIRD) 
from dino_runner.components.obstacles.bird import bird

class ObstacleManage():
    def __init__(self):
        self.obstacles = []



    def update(self, game):
        if len(self.obstacles) == 0:
            cactus_size = random.randint(0,1)
            if cactus_size == 0:
                Large_cactus = (Cactus(LARGE_CACTUS))
                Large_cactus.rect.y = 310
                self.obstacles.append(Large_cactus)
            elif cactus_size == 3:
                self.obstacles.append(bird(BIRD))
            else:
                small_cactus = Cactus(SMALL_CACTUS)
                small_cactus.rect.y = 325
                self.obstacles.append(Cactus(SMALL_CACTUS))
        
        
        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.dino.dino_rect.colliderect(obstacle.rect) and game.dino.shield == False:
                pygame.time.delay(100)
                game.player_heart_manager.reduce_heart()

                if game.player_heart_manager.heart_count > 0:
                    self.obstacles.pop()
                    game.dino.has_lives = True
                else:
                    pygame.time.delay(500)
                    game.dino.has_lives = False
                    game.playing = False
                    game.death_count += 1
                    break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)