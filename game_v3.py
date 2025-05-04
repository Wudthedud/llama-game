"""Module containing the Game class for running the llama game."""

import random
import pygame
from llama_v3 import Llama
from obstacle_v3 import Obstacle

white = (255, 255, 255)

class Game:
    """Main game class handling game state, rendering, input, and logic."""
    def __init__(self):
        """Initialize the game and set up the initial state."""
        pygame.init()
        self.reset_game()
        self.show_start = True

    def reset_game(self):
        """Reset the game state to start a new game."""
        self.screen = pygame.display.set_mode((1000, 720))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("assets/lemonmilk.ttf", 50)
        self.small_font = pygame.font.Font("assets/lemonmilk.ttf", 28)
        self.tiny_font = pygame.font.Font("assets/lemonmilk.ttf", 20)
        self.llama = Llama(200, 500)
        self.obstacles = [
            Obstacle(
                1000 + i * 300, 0, random.choice([1, 0.9, 0.8, 0.7, 0.6]), 5
            ) for i in range(2)
        ]
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
        """Initialize display settings and load the high score."""
        pygame.display.set_icon(
            pygame.image.load("assets/llama_icon.png")
        )
        pygame.display.set_caption("Llama Game - by Daniel Wu")
        self.highscore = self.load_high_score()

    def run_game(self):
        """Main game loop handling events, updates, and rendering."""
        self.initialize_game()
        bg = pygame.transform.scale(
            pygame.image.load("assets/ground.png").convert(), (1000, 720)
        )
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
                        self.obstacles = [
                            Obstacle(
                                1000 + i * 300, 0,
                                random.choice([1, 0.9, 0.8, 0.7, 0.6]), 5
                            ) for i in range(2)
                        ]
                    elif event.key == pygame.K_ESCAPE:
                        if self.game_over:
                            self.reset_game()
                            self.initialize_game()
                            bg = pygame.transform.scale(
                                pygame.image.load(
                                    "assets/ground.png"
                                ).convert(), (1000, 720)
                            )
                        elif self.paused:
                            self.paused = False
                        elif not self.game_over:
                            self.paused = True

            if self.show_start:
                self.draw_start_screen(bg)
            elif not self.game_over and not self.paused:
                self.update_game(bg)
            elif self.paused:
                self.draw_pause_screen(bg)

            pygame.display.flip()
            self.clock.tick(60)

    def handle_input(self):
        """Handle player input for jumping."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.llama.jump()

    def draw_start_screen(self, bg):
        """Draw the start screen with title and instructions."""
        self.screen.blit(bg, (0, 0))
        title = self.font.render(
            "Llama Game - Daniel Wu", True, (255, 255, 0)
        )
        hs_text = self.small_font.render(
            f"High Score: {self.highscore:.1f}s", True, white
        )
        jump_info = self.small_font.render(
            "Press SPACE to Jump", True, white
        )
        esc_info = self.small_font.render(
            "Press ESC to Start/Pause/Unpause", True, white
        )
        self.screen.blit(title, title.get_rect(center=(500, 250)))
        self.screen.blit(hs_text, hs_text.get_rect(center=(500, 320)))
        self.screen.blit(jump_info, jump_info.get_rect(center=(500, 380)))
        self.screen.blit(esc_info, esc_info.get_rect(center=(500, 430)))

    def update_game(self, bg):
        """Update game state, handle collisions, and draw game elements."""
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
                self.obstacle_speed = min(
                    self.obstacle_speed + 0.4, self.max_obstacle_speed
                )
            for o in self.obstacles:
                o.speed = self.obstacle_speed

        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            min_jump_gap = 220
            last_x = max([o.x for o in self.obstacles], default=0)
            group_chance = random.random()
            if group_chance < 0.25:
                group_size = random.randint(2, 4)
                base_x = max(1000, last_x + min_jump_gap)
                scale = random.choice([1, 0.9, 0.8, 0.7, 0.6])
                jump_distance = 180
                min_gap = int(jump_distance + 30 * scale)
                max_gap = min_gap + 60
                group_y = random.choice([0, 20, 40, 60])
                for i in range(group_size):
                    gap = random.randint(min_gap, max_gap)
                    x = base_x + i * gap
                    y = group_y + random.choice([0, 10, 20])
                    self.obstacles.append(
                        Obstacle(x, y, scale, self.obstacle_speed)
                    )
            else:
                scale = random.choice([1, 0.9, 0.8, 0.7, 0.6])
                y = random.choice([0, 10, 20, 30, 40, 50, 60])
                spawn_x = max(1000, last_x + min_jump_gap)
                self.obstacles.append(
                    Obstacle(spawn_x, y, scale, self.obstacle_speed)
                )
            variation = random.randint(-20, 20)
            self.spawn_interval = max(
                self.min_spawn_interval, self.spawn_interval + variation
            )

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
        self.screen.blit(
            self.small_font.render(f"Time: {seconds:.1f}s", True, white),
            (20, 10)
        )
        self.screen.blit(
            self.tiny_font.render(
                f"Speed: {self.obstacle_speed:.1f}", True, white
            ),
            (20, 40)
        )

    def draw_pause_screen(self, bg):
        """Draw the pause or game over screen."""
        self.screen.blit(bg, (0, 0))
        for o in self.obstacles:
            o.draw(self.screen)
        self.llama.draw(self.screen)
        if self.game_over:
            pause_text = self.font.render(
                "Game Over", True, (255, 0, 0)
            )
            info_text = self.small_font.render(
                "Press ESC to Restart", True, white
            )
            score_text = self.small_font.render(
                f"Score: {self.ticks_survived / 60:.1f}s", True, white
            )
        else:
            pause_text = self.font.render(
                "Paused", True, (255, 255, 0)
            )
            info_text = self.small_font.render(
                "Press ESC to Resume", True, white
            )
            score_text = None
        hs_text = self.small_font.render(
            f"High Score: {self.highscore:.1f}s", True, white
        )
        self.screen.blit(
            pause_text, pause_text.get_rect(center=(500, 300))
        )
        self.screen.blit(
            hs_text, hs_text.get_rect(center=(500, 370))
        )
        if score_text:
            self.screen.blit(
                score_text, score_text.get_rect(center=(500, 400))
            )
            self.screen.blit(
                info_text, info_text.get_rect(center=(500, 440))
            )
        else:
            self.screen.blit(
                info_text, info_text.get_rect(center=(500, 420))
            )

    def load_high_score(self):
        """Load the high score from a file, creating it if necessary."""
        try:
            with open(
                "highscore.txt", "r", encoding="utf-8"
            ) as f:
                value = f.read().strip()
                return float(value) if value else 0.0
        except IOError:
            with open(
                "highscore.txt", "w", encoding="utf-8"
            ) as f:
                f.write("0.0")
            return 0.0

    def update_high_score(self, score):
        """Update the high score file if the current score is higher."""
        if score > self.load_high_score():
            with open(
                "highscore.txt", "w", encoding="utf-8"
            ) as f:
                f.write(f"{score:.1f}")
