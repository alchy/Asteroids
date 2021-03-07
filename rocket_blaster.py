import pygame

class RocketBlast:
    def __init__(self, position_x, position_y, acceleration_x, acceleration_y):
        self.position_x = position_x
        self.position_y = position_y
        self.acceleration_x = acceleration_x
        self.acceleration_y = acceleration_y
        self.ttl = 1024

class RocketBlaster:
    def __init__(self, screen):
        self.screen = screen
        self.blast_image = pygame.image.load('images/blast.png')
        self.blast_mask = pygame.mask.from_surface(self.blast_image)
        self.blasts = []

    def new_blast(self, position_x, position_y, acceleration_x, acceleration_y):
        self.blasts.append(RocketBlast(position_x, position_y, acceleration_x, acceleration_y))

    def check_collision(self, object_mask, object_x, object_y):
        for blast in self.blasts:
            offset_x = int(blast.position_x - object_x)
            offset_y = int(blast.position_y - object_y)
            overlap = object_mask.overlap(self.blast_mask, (offset_x, offset_y))
            if overlap is not None:
                blast.ttl = 1
                return True
        return False

    def redraw(self):
        for blast in self.blasts:
            blast.ttl -= 1
            if blast.ttl == 0:
                self.blasts.remove(blast)
            else:
                # blast.position_x += blast.acceleration_x
                blast.position_y += blast.acceleration_y - 3
                self.screen.blit(self.blast_image, (blast.position_x, blast.position_y))