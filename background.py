import pygame
import parameters

class Background:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('images/world-space-atmosphere-ship-panorama-small.jpg')
        self.background_width, self.background_height = self.background.get_rect().bottomright

        self.background_scroll_in_x = 0
        self.background_scroll_in_x_amount = 0 #-0.2
        self.background_scroll_in_y = (self.background_height * -1) + parameters.SCREEN_HEIGHT
        self.background_scroll_in_y_amount = 0.2

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
        print(self.background_scroll_in_y, self.background_height)


