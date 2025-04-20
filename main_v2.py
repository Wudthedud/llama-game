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
        while not self.quit_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True

            self.screen.fill((255, 255, 255))  # white background
            self.llama.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)  # Limit to 60 FPS

    
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
        self.y = y
        self.image = pygame.image.load("assets/llama.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))


    def draw(self, screen):
        """Draw food on screen"""
        llama = pygame.image.load("assets/llama.png").convert_alpha()
        resized_llama = pygame.transform.smoothscale(llama, (20, 20))
        screen.blit(resized_llama, (self.x, self.y))

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/cactus.png")
        self.image = pygame.transform.scale(self.image, (100, 100))

if __name__ == "__main__":
    main = Main()
    main.run_game()
