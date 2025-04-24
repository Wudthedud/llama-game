import pygame

class Obstacle:
    def __init__(self, x, y, scale=0.8, speed=5):
        size = int(50 * scale)
        self.size = size
        self.x = x
        self.y = 425 - size
        self.image = pygame.transform.scale(pygame.image.load("assets/cactus.png"), (size, size))
        self.speed = speed

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        margin = 0.3
        shrink = int(self.size * margin)
        return pygame.Rect(self.x + shrink // 2, self.y + shrink // 2, self.size - shrink, self.size - shrink)
