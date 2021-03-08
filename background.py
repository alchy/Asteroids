import pygame
import random
import parameters

class Star:
    def __init__(self):
        self.x = random.randint(0, parameters.SCREEN_WIDTH)
        self.y = random.randint(parameters.SCREEN_HEIGHT * -1, 0)
        self.speed = random.random() + 0.2

    def update_position(self):
        self.y += self.speed
        if self.y > parameters.SCREEN_HEIGHT:
            self.y = random.randint(parameters.SCREEN_HEIGHT * -1, 0)

class Background:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('images/world-space-atmosphere-ship-panorama-small.jpg')
        self.background_width, self.background_height = self.background.get_rect().bottomright

        self.background_scroll_in_x = 0
        self.background_scroll_in_x_amount = 0 #-0.2
        self.background_scroll_in_y = (self.background_height * -1) + parameters.SCREEN_HEIGHT
        self.background_scroll_in_y_amount = 0.2

        self.stars_byteplan = pygame.Surface(parameters.SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.stars_byteplan.set_colorkey((0, 0, 0))
        self.stars = []
        for star in range(parameters.BACKGROUND_STARS_COUNT):
            self.stars.append(Star())

    def redraw(self):
        if self.background_scroll_in_x_amount < 0:
            self.screen.blit(self.background, (int(self.background_scroll_in_x + self.background_width), \
                                               int(self.background_scroll_in_y)))
        if self.background_scroll_in_y_amount > 0:
            self.screen.blit(self.background, (int(self.background_scroll_in_x), \
                                               int(self.background_scroll_in_y) - self.background_height))
        self.screen.blit(self.background, (int(self.background_scroll_in_x), int(self.background_scroll_in_y)))
        self.background_scroll_in_x += self.background_scroll_in_x_amount
        if abs(self.background_scroll_in_x) > self.background_width:
            self.background_scroll_in_x = 0
        self.background_scroll_in_y += self.background_scroll_in_y_amount
        if self.background_scroll_in_y > self.background_height:
            self.background_scroll_in_y = 0

        for star in self.stars:
            self.stars_byteplan.set_at((int(star.x), int(star.y)), (255, 255, 255))
            star.update_position()
        self.screen.blit(self.stars_byteplan, (0, 0))
        self.stars_byteplan.fill((0, 0, 0))