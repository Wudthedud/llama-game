import pygame
import time
import random
pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)

class Main:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.screen = pygame.display.set_mode((1000, 720))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("assets/lemonmilk.ttf", 50)
        self.llama = Llama(200, 500)
        self.obstacles = [Obstacle(1000 + i * 300, 0, random.choice([1.0, 0.9, 0.8, 0.7, 0.6])) for i in range(2)]
        self.quit_game = False
        self.game_over = False
        self.score = 0
        self.spawn_timer = 0
        self.spawn_interval = 120
        self.min_spawn_interval = 40

    def initialize_game(self):
        """Sets up game window"""
        game_icon = pygame.image.load("assets/llama_icon.png")
        pygame.display.set_icon(game_icon)
        pygame.display.set_caption("Llama Game - by Daniel Wu")
        highscore = self.load_high_score()
        print(f"High Score: {highscore}")
    
    def run_game(self):
        self.initialize_game()
        background = pygame.image.load("assets/ground.png").convert()
        background = pygame.transform.scale(background, (1000, 720))
        while not self.quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True
                # --- Restart logic ---
                if self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.reset_game()
                    self.initialize_game()
                    background = pygame.image.load("assets/ground.png").convert()
                    background = pygame.transform.scale(background, (1000, 720))
            if not self.game_over:
                self.handle_input()
                self.screen.blit(background, (0, 0))
                self.llama.update()
                # Update and draw obstacles
                for obstacle in self.obstacles:
                    obstacle.update()
                    obstacle.draw(self.screen)
                # Remove obstacles that have gone off screen
                self.obstacles = [obs for obs in self.obstacles if obs.x > -obs.size]
                # Spawn new obstacles at intervals, increasing frequency over time
                self.spawn_timer += 1
                if self.spawn_timer >= self.spawn_interval:
                    self.spawn_timer = 0
                    scale = random.choice([1.0, 0.9, 0.8, 0.7, 0.6])
                    self.obstacles.append(Obstacle(1000, 0, scale))
                    # Increase difficulty by reducing spawn interval, but not below minimum
                    if self.spawn_interval > self.min_spawn_interval:
                        self.spawn_interval -= 2
                self.llama.draw(self.screen)

                # --- Collision detection ---
                llama_rect = self.llama.get_rect()
                for obstacle in self.obstacles:
                    if llama_rect.colliderect(obstacle.get_rect()):
                        self.game_over = True
                        break
            else:
                # Draw everything frozen
                self.screen.blit(background, (0, 0))
                for obstacle in self.obstacles:
                    obstacle.draw(self.screen)
                self.llama.draw(self.screen)
                # Draw "Game Over" text
                game_over_text = self.font.render("Game Over", True, (255, 0, 0))
                self.screen.blit(game_over_text, (350, 300))
                restart_text = self.font.render("Press ESC to Restart", True, (255, 255, 255))
                self.screen.blit(restart_text, (230, 380))

            pygame.display.flip()
            self.clock.tick(60)

    def handle_input(self):
        """Handle user input for jumping"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.llama.jump()
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            with open("highscore.txt", "r", encoding="utf-8") as highscore_file:
                value = highscore_file.read().strip()
                if not value:
                    return 0
                return int(value)
        except IOError:
            with open("highscore.txt", "w", encoding="utf-8") as highscore_file:
                highscore_file.write("0")
            return 0

    def update_high_score(self, score):
        """Update high score in file"""
        highscore = self.load_high_score()
        if score > highscore:
            with open("highscore.txt", "w", encoding="utf-8") as highscore_file:
                highscore_file.write(str(score))



class Llama:
    def __init__(self, x, y):
        self.x = x
        self.y = 425 - 80  # Correct initial position
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
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = self.jump_strength

    def update(self):
        if self.is_jumping:
            self.velocity += self.gravity
            self.y += self.velocity
            if self.y >= 425 - 80:
                self.y = 425 - 80
                self.is_jumping = False

        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)

    def draw(self, screen):
        resized_llama = pygame.transform.smoothscale(self.animation_frames[self.current_frame], (80, 80))
        screen.blit(resized_llama, (self.x, self.y))

    def get_rect(self):
        """Returns the rectangle for collision detection, smaller than the image."""
        margin = 0.2  # 20% margin
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
    def __init__(self, x, y, scale=0.8):
        base_size = 50
        self.size = int(base_size * scale)
        self.x = x
        self.y = 425 - self.size  # Adjust y for new height
        self.image = pygame.image.load("assets/cactus.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.speed = 5

    def update(self):
        """Move the obstacle to the left"""
        self.x -= self.speed

    def draw(self, screen):
        """Draw the obstacle on the screen"""
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        """Returns the rectangle for collision detection, smaller than the image."""
        margin = 0.2  # 20% margin
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
