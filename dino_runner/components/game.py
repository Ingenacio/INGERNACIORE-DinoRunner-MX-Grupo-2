import pygame
from dino_runner.components.obstacles.obstacle_manager import ObstacleManage
from dino_runner.components.player_heart.player_heart_manager import PlayerHeartManager
from dino_runner.components.powerups.power_up_manager import PowerUpManager

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, WHITE_COLOR, RUNNING
from dino_runner.components.dinosaur import Dinosaur

from dino_runner.components.text_utils import get_score_element
from dino_runner.components import text_utils


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.dino = Dinosaur()
        self.obstacle_manager = ObstacleManage()
        self.player_heart_manager = PlayerHeartManager()
        self.power_up_manager = PowerUpManager()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 390
        self.points = 0
        self.death_count = 0
        self.running = True



    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()

    def run(self):
        # Game loop: events - update - draw
        self.obstacle_manager = ObstacleManage()
        self.player_heart_manager = PlayerHeartManager()
        self.power_up_manager.reser_power_ups(self.points)
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        imput_user = pygame.key.get_pressed()
        self.dino.update(imput_user)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.dino)


    def draw(self):
        self.screen.fill((255, 255, 255))

        self.clock.tick(FPS)
        self.score()
        self.draw_background()
        self.dino.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.player_heart_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)


        pygame.display.update()
        pygame.display.flip()


    def show_menu(self):
        self.running = True
        white_color = (255, 255, 255)
        self.screen.fill(WHITE_COLOR)
        self.print_menu_elements()

        pygame.display.update()

        self.handle_key_events_on_menu()


    def print_menu_elements(self):
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            text, text_rext = text_utils.get_centered_message('Press any key to start')
            self.screen.blit(text, text_rext)
        elif self.death_count > 0:
            text, text_rect = text_utils.get_centered_message('Press any key to restart')
            score, score_rect = text_utils.get_centered_message('Your score is: ' + str(self.points), height=half_screen_height + 50)
            death, death_rect = text_utils.get_centered_message('Death count: ' + str(self.death_count), height=half_screen_height + 100)
            self.screen.blit(score, score_rect)
            self.screen.blit(text, text_rect)
            self.screen.blit(death, death_rect)
            #self.screen.blit(RUNNING[0], (half_screen_width  - 20, half_screen_height - 20))

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                pygame.display.quit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                self.run()

    def score(self):
        self.points += 1 

        if self.points % 100 == 0:
            self.game_speed += 1

        text, text_rect = text_utils.get_score_element(self.points)
        self.dino.check_visibility(self.screen)

        self.screen.blit(text, text_rect)



    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
