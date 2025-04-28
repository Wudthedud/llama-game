import pygame
import random
from llama import Llama
from obstacle import Obstacle

white = (255, 255, 255)

class Game:
    def __init__(self):
        pygame.init()
        self.reset_game()
        self.show_start = True

    def reset_game(self):
        self.screen = pygame.display.set_mode((1000, 720))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("assets/lemonmilk.ttf", 50)
        self.small_font = pygame.font.Font("assets/lemonmilk.ttf", 28)
        self.tiny_font = pygame.font.Font("assets/lemonmilk.ttf", 20)
        self.llama = Llama(200, 500)
        self.obstacles = [Obstacle(1000 + i * 300, 0, random.choice([1, 0.9, 0.8, 0.7, 0.6]), 5) for i in range(2)]
        self.quit_game = False
        self.game_over = False
        self.paused = False
        self.ticks_survived = 0
        self.spawn_timer = 0
        self.spawn_interval = 120
        self.min_spawn_interval = 40
        self.obstacle_speed = 5
        self.max_obstacle_speed = 11
        self.difficulty_timer = 0
        self.highscore = self.load_high_score()
        self.show_start = True

    def initialize_game(self):
        pygame.display.set_icon(pygame.image.load("assets/llama_icon.png"))
        pygame.display.set_caption("Llama Game - by Daniel Wu")
        self.highscore = self.load_high_score()

    def run_game(self):
        self.initialize_game()
        bg = pygame.transform.scale(pygame.image.load("assets/ground.png").convert(), (1000, 720))
        while not self.quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True
                if event.type == pygame.KEYDOWN:
                    if self.show_start and event.key == pygame.K_ESCAPE:
                        self.show_start = False
                        self.game_over = False
                        self.paused = False
                        self.ticks_survived = 0
                        self.spawn_timer = 0
                        self.difficulty_timer = 0
                        self.obstacle_speed = 5
                        self.spawn_interval = 120
                        self.llama = Llama(200, 500)
                        self.obstacles = [Obstacle(1000 + i * 300, 0, random.choice([1, 0.9, 0.8, 0.7, 0.6]), 5) for i in range(2)]
                    elif event.key == pygame.K_ESCAPE:
                        if self.game_over or self.paused:
                            self.reset_game()
                            self.initialize_game()
                            bg = pygame.transform.scale(pygame.image.load("assets/ground.png").convert(), (1000, 720))
                        elif not self.game_over:
                            self.paused = not self.paused

            if self.show_start:
                self.draw_start_screen(bg)
            elif not self.game_over and not self.paused:
                self.update_game(bg)
            elif self.paused:
                self.draw_pause_screen(bg)

            pygame.display.flip()
            self.clock.tick(60)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.llama.jump()

    def draw_start_screen(self, bg):
        self.screen.blit(bg, (0, 0))
        title = self.font.render("Llama Game - Daniel Wu", True, (255, 255, 0))
        hs_text = self.small_font.render(f"High Score: {self.highscore:.1f}s", True, white)
        jump_info = self.small_font.render("Press SPACE to Jump", True, white)
        esc_info = self.small_font.render("Press ESC to Start/Pause/Unpause", True, white)
        self.screen.blit(title, title.get_rect(center=(500, 250)))
        self.screen.blit(hs_text, hs_text.get_rect(center=(500, 320)))
        self.screen.blit(jump_info, jump_info.get_rect(center=(500, 380)))
        self.screen.blit(esc_info, esc_info.get_rect(center=(500, 430)))

    def update_game(self, bg):
        self.handle_input()
        self.screen.blit(bg, (0, 0))
        self.llama.update()
        for o in self.obstacles:
            o.update()
            o.draw(self.screen)
        self.obstacles = [o for o in self.obstacles if o.x > -o.size]

        self.difficulty_timer += 1
        if self.difficulty_timer % 90 == 0:
            if self.spawn_interval > self.min_spawn_interval:
                self.spawn_interval -= 2
            if self.obstacle_speed < self.max_obstacle_speed:
                self.obstacle_speed += 0.4

        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            scale = random.choice([1, 0.9, 0.8, 0.7, 0.6])
            self.obstacles.append(Obstacle(1000, 0, scale, self.obstacle_speed))

        self.llama.draw(self.screen)
        llama_rect = self.llama.get_rect()
        for o in self.obstacles:
            if llama_rect.colliderect(o.get_rect()):
                self.game_over = True
                self.paused = True
                seconds = round(self.ticks_survived / 60, 1)
                if seconds > self.highscore:
                    self.update_high_score(seconds)
                    self.highscore = seconds
                break

        self.ticks_survived += 1
        seconds = self.ticks_survived / 60
        self.screen.blit(self.small_font.render(f"Time: {seconds:.1f}s", True, white), (20, 10))
        self.screen.blit(self.tiny_font.render(f"Speed: {self.obstacle_speed:.1f}", True, white), (20, 40))

    def draw_pause_screen(self, bg):
        self.screen.blit(bg, (0, 0))
        for o in self.obstacles:
            o.draw(self.screen)
        self.llama.draw(self.screen)
        if self.game_over:
            pause_text = self.font.render("Game Over", True, (255, 0, 0))
            info_text = self.small_font.render("Press ESC to Restart", True, white)
        else:
            pause_text = self.font.render("Paused", True, (255, 255, 0))
            info_text = self.small_font.render("Press ESC to Resume", True, white)
        hs_text = self.small_font.render(f"High Score: {self.highscore:.1f}s", True, white)
        self.screen.blit(pause_text, pause_text.get_rect(center=(500, 300)))
        self.screen.blit(hs_text, hs_text.get_rect(center=(500, 370)))
        self.screen.blit(info_text, info_text.get_rect(center=(500, 420)))

    def load_high_score(self):
        try:
            with open("highscore.txt", "r", encoding="utf-8") as f:
                value = f.read().strip()
                return float(value) if value else 0.0
        except IOError:
            with open("highscore.txt", "w", encoding="utf-8") as f:
                f.write("0.0")
            return 0.0

    def update_high_score(self, score):
        if score > self.load_high_score():
            with open("highscore.txt", "w", encoding="utf-8") as f:
                f.write(f"{score:.1f}")
