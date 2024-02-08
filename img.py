import pygame

class Target:
    def __init__(self, x, y, radius, surface):
        self.x = x
        self.y = y
        self.radius = radius
        self.surface = surface
        self.color = (255, 0, 0, 160)
    def draw(self):
        pygame.draw.circle(self.surface, self.color, (self.x, self.y), self.radius, width=3)
        pygame.draw.line(self.surface, self.color, (self.x - self.radius - 10, self.y),
                         (self.x + self.radius + 10, self.y), width=3)
        pygame.draw.line(self.surface, self.color, (self.x, self.y - self.radius - 10), (self.x, self.y + self.radius + 10), width=3)