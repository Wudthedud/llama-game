"""Module for the Obstacle class used in the llama game."""

import pygame

class Obstacle:
    """Represents an obstacle in the llama game, handling its position, image, movement, and collision detection."""
    def __init__(self, x, y, scale=0.8, speed=5):
        """Initialize an obstacle with position, size, and movement speed."""
        size = int(50 * scale)
        self.size = size
        self.x = x
        self.y = 425 - size
        self.image = pygame.transform.scale(pygame.image.load("assets/cactus.png"), (size, size))
        self.speed = speed

    def update(self):
        """Update the obstacle position by moving it to the left."""
        self.x -= self.speed

    def draw(self, screen):
        """Draw the obstacle on the specified screen."""
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        """Return a pygame Rect representing the obstacle's collision hitbox."""
        margin = 0.5
        shrink = int(self.size * margin)
        return pygame.Rect(self.x + shrink // 2, self.y + shrink // 2, self.size - shrink, self.size - shrink)
