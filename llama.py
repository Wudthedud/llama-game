import pygame

class Llama:
    def __init__(self, x, y):
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
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = self.jump_strength

    def update(self):
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
        screen.blit(pygame.transform.smoothscale(self.animation_frames[self.current_frame], (80, 80)), (self.x, self.y))

    def get_rect(self):
        margin = 0.3
        width = 80
        height = 80
        shrink_w = int(width * margin)
        shrink_h = int(height * margin)
        return pygame.Rect(self.x + shrink_w // 2, self.y + shrink_h // 2, width - shrink_w, height - shrink_h)
