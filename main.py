import pygame
pygame.init

black = (0, 0, 0)
white = (255, 255, 255)

font = pygame.font.Font("")
screen = pygame.display.set_mode((1000, 720))
game_icon = pygame.image.load("assets/llama_icon.png")
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Llama Game - by Daniel Wu")

quit_game = False
while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

pygame.quit()
quit()
