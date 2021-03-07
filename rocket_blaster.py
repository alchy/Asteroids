import pygame

class RocketBlast:
    def __init__(self, position_x, position_y, acceleration_x, acceleration_y):
        self.position_x = position_x
        self.position_y = position_y
        self.acceleration_x = acceleration_x
        self.acceleration_y = acceleration_y


class RocketBlaster:
    def __init__(self, screen):
        self.screen = screen
        self.blast_image = pygame.image.load('images/blast.png')
        self.blast_mask = pygame.mask.from_surface(self.rocket_blast)
        self.blasts = []


    def redraw(self, exploded):
        self.screen.blit(self.rocket_blast, (self.blast_x, self.blast_y))



