import pygame
import sys

pygame.init()

CLOCK = pygame.time.Clock()  # Essential for regulating the FPS (done under CLOCK.tick() at the bottom)
SCREEN = pygame.display.set_mode((1000, 720))
pygame.display.set_caption("Jumping in PyGame")

X_POSITION, Y_POSITION = 400, 660  # This is the x and y postion of Mario


# 2 surfaces - 1st to represent Mario standing and 2nd comes into play when he's jumping
GROUND = pygame.transform.scale(pygame.image.load("ground.png"), (48, 64))
LLAMA_STANDING = pygame.transform.scale(pygame.image.load("Llama.png"), (48, 64))

llama_rect = LLAMA_STANDING.get_rect(center=(X_POSITION, Y_POSITION))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    llama_rect = LLAMA_STANDING.get_rect(center=(X_POSITION, Y_POSITION))

    pygame.display.update()
    CLOCK.tick(60)  # This is the FPS

