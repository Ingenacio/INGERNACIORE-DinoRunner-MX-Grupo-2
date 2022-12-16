from dino_runner.components.powerups.shield import Shield
import pygame
import random


class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.points = 0
        self.when_appears = 0
        self.sound_collision = pygame.mixer.Sound("dino_runner/components/sound/golpe.mp3")

    def update(self, points, game_speed, player):
        self.generate_power_ups(points)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if (player.dino_rect.colliderect(power_up.rect)):
                self.sound_collision.play()
                power_up.star_time = pygame.time.get_ticks()
                player.shield = True
                player.type = power_up.type
                power_up.start_time = pygame.time.get_ticks()
                time_random = random.randrange(5, 8)
                player.shield_time_up = power_up.start_time + (time_random *1000)


                self.power_ups.remove(power_up)


    def generate_power_ups(self, points):
        self.points = points
        if len(self.power_ups) == 0:
            if self.when_appears == self.points:
                self.when_appears = random.randint(self.when_appears + 200, self.when_appears + 500)
                self.power_ups.append(Shield())



    def draw(self, screen):
        for power_ups in self.power_ups:
            power_ups.draw(screen)


    def reser_power_ups(self, points):
        self.power_ups = []
        self.points = points
        self.when_appears = random.randint(200,300) + self.points