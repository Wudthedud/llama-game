import pygame
import time
pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)

class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 720))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("assets/lemonmilk.ttf", 50)
        self.llama = Llama(200, 500)
        self.obstacle = Obstacle(400, 500)
        self.quit_game = False
        self.game_over = False
        self.score = 0


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
            self.handle_input()  # Handle user input
            self.screen.blit(background, (0, 0))
            self.llama.update()  # Update llama position
            self.llama.draw(self.screen)
            self.obstacle.update()  # Update obstacle position
            self.obstacle.draw(self.screen)  # Draw obstacle
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

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = 425 - 48  # Adjusted y position for new height (60 * 0.8 = 48)
        self.image = pygame.image.load("assets/cactus.png")
        self.image = pygame.transform.scale(self.image, (48, 48))  # 60 * 0.8 = 48
        self.speed = 5  # Speed of obstacle movement

    def update(self):
        """Move the obstacle to the left"""
        self.x -= self.speed
        if self.x < -48:  # Reset position when off-screen
            self.x = 1000

    def draw(self, screen):
        """Draw the obstacle on the screen"""
        screen.blit(self.image, (self.x, self.y))

if __name__ == "__main__":
    main = Main()
    main.run_game()
