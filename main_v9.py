import pygame
import random
pygame.init()

white = (255, 255, 255)

class Main:
    def __init__(self):
        """Initialize and reset the game."""
        self.reset_game()
        self.show_start = True

    def reset_game(self):
        """Reset game state."""
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
        """Setup window and high score."""
        pygame.display.set_icon(pygame.image.load("assets/llama_icon.png"))
        pygame.display.set_caption("Llama Game - by Daniel Wu")
        self.highscore = self.load_high_score()

    def run_game(self):
        """Main game loop."""
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
                self.screen.blit(bg, (0, 0))
                title = self.font.render("Llama Game - Daniel Wu", True, (255, 255, 0))
                hs_text = self.small_font.render(f"High Score: {self.highscore:.1f}s", True, white)
                info = self.small_font.render("Press ESC to Start", True, white)
                title_rect = title.get_rect(center=(500, 250))
                hs_rect = hs_text.get_rect(center=(500, 320))
                info_rect = info.get_rect(center=(500, 400))
                self.screen.blit(title, title_rect)
                self.screen.blit(hs_text, hs_rect)
                self.screen.blit(info, info_rect)
            elif not self.game_over and not self.paused:
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
                spd_text = self.tiny_font.render(f"Speed: {self.obstacle_speed:.1f}", True, white)
                self.screen.blit(spd_text, (20, 40))
            elif self.paused:
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
                pause_rect = pause_text.get_rect(center=(500, 300))
                hs_rect = hs_text.get_rect(center=(500, 370))
                info_rect = info_text.get_rect(center=(500, 420))
                self.screen.blit(pause_text, pause_rect)
                self.screen.blit(hs_text, hs_rect)
                self.screen.blit(info_text, info_rect)
            pygame.display.flip()
            self.clock.tick(60)

    def handle_input(self):
        """Handle jump input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.llama.jump()

    def load_high_score(self):
        """Load high score from file."""
        try:
            with open("highscore.txt", "r", encoding="utf-8") as f:
                value = f.read().strip()
                return float(value) if value else 0.0
        except IOError:
            with open("highscore.txt", "w", encoding="utf-8") as f:
                f.write("0.0")
            return 0.0

    def update_high_score(self, score):
        """Update high score in file."""
        if score > self.load_high_score():
            with open("highscore.txt", "w", encoding="utf-8") as f:
                f.write(f"{score:.1f}")

class Llama:
    def __init__(self, x, y):
        """Initialize the Llama."""
        self.x = x
        self.y = 345
        self.velocity = 0
        self.is_jumping = False
        self.gravity = 1
        self.jump_strength = -15
        self.animation_frames = [
            pygame.image.load("assets/llama.png").convert_alpha(),
            pygame.image.load("assets/llama2.png").convert_alpha(),
            pygame.image.load("assets/llama3.png").convert_alpha(),
        ]
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_delay = 5

    def jump(self):
        """Jump if not already jumping."""
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = self.jump_strength

    def update(self):
        """Update position and animation."""
        if self.is_jumping:
            self.velocity += self.gravity
            self.y += self.velocity
            if self.y >= 345:
                self.y = 345
                self.is_jumping = False
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

    def draw(self, screen):
        """Draw llama."""
        screen.blit(pygame.transform.smoothscale(self.animation_frames[self.current_frame], (80, 80)), (self.x, self.y))

    def get_rect(self):
        """Rectangle for collision detection."""
        margin = 0.3
        width = 80
        height = 80
        shrink_w = int(width * margin)
        shrink_h = int(height * margin)
        return pygame.Rect(
            self.x + shrink_w // 2,
            self.y + shrink_h // 2,
            width - shrink_w,
            height - shrink_h
        )

class Obstacle:
    def __init__(self, x, y, scale=0.8, speed=5):
        """Initialize Obstacle."""
        size = int(50 * scale)
        self.size = size
        self.x = x
        self.y = 425 - size
        self.image = pygame.transform.scale(pygame.image.load("assets/cactus.png"), (size, size))
        self.speed = speed

    def update(self):
        """Move left."""
        self.x -= self.speed

    def draw(self, screen):
        """Draw obstacle."""
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        """Rectangle for collision detection."""
        margin = 0.3
        shrink = int(self.size * margin)
        return pygame.Rect(
            self.x + shrink // 2,
            self.y + shrink // 2,
            self.size - shrink,
            self.size - shrink
        )

if __name__ == "__main__":
    main = Main()
    main.run_game()
