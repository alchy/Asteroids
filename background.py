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
        self.background = []
        self.background_width = []
        self.background_height = []
        self.active_background = 0
        self.next_background = self.active_background + 1
        for background_id in range(0, parameters.MAX_BACKGROUNDS + 1):
            self.background.append(pygame.image.load('images/level_backgrounds/background_level_' +
                                  str('{:0>3}'.format(background_id)) +
                                  '.jpg'))
            self.background_width.append(0)
            self.background_height.append(0)
            (self.background_width[background_id], self.background_height[background_id]) = \
                self.background[background_id].get_rect().bottomright

        self.background_scroll_in_x = 0
        self.background_scroll_in_x_amount = 0 #-0.2
        self.background_scroll_in_y = (self.background_height[self.active_background] * -1) + parameters.SCREEN_HEIGHT
        self.background_scroll_in_y_amount = 0.2

        self.stars_byteplan = pygame.Surface(parameters.SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.stars_byteplan.set_colorkey((0, 0, 0))
        self.stars = []
        for star in range(parameters.BACKGROUND_STARS_COUNT):
            self.stars.append(Star())

    def redraw(self):
        # pozadi v ose x dojizdi, je nutne vykreslovat zprava nove pozadi nebo zacatek stareho
        if self.background_scroll_in_x_amount < 0:
            self.screen.blit(self.background, (int(self.background_scroll_in_x +
                                                   self.background_width[self.active_background]),
                                               int(self.background_scroll_in_y)))
        # pozadi v ose y dojizdi, je nutne vykreslovat zvrchu nove pozadi nebo zacatek stareho
        if self.background_scroll_in_y_amount > 0:
            self.screen.blit(self.background[self.next_background],
                             (int(self.background_scroll_in_x),
                              int(self.background_scroll_in_y) -
                              self.background_height[self.next_background]))
        # vykresli pozadi
        self.screen.blit(self.background[self.active_background], (int(self.background_scroll_in_x),
                                                                   int(self.background_scroll_in_y)))
        # dalsi scroll pozadi v ose x
        self.background_scroll_in_x += self.background_scroll_in_x_amount
        if abs(self.background_scroll_in_x) > self.background_width[self.active_background]:
            self.background_scroll_in_x = 0

        # dalsi scroll pozadi v ose y
        self.background_scroll_in_y += self.background_scroll_in_y_amount

        # osetreni toho, ze bude nadale jako primarni pozadi vykreslovano pozadi s id self.next_background
        if self.background_scroll_in_y > parameters.SCREEN_HEIGHT:
            # aktivni pozadi je dalsi pozadi
            self.active_background = self.next_background
            self.next_background += 1
            if self.next_background > parameters.MAX_BACKGROUNDS:
                # dosly pozadi, jedeme dokola
                self.next_background = 0
            # vyrezetuje offset vykreslovani
            self.background_scroll_in_y = \
                (self.background_height[self.active_background] * -1) + parameters.SCREEN_HEIGHT

        for star in self.stars:
            self.stars_byteplan.set_at((int(star.x), int(star.y)), (255, 255, 255))
            star.update_position()
        self.screen.blit(self.stars_byteplan, (0, 0))
        self.stars_byteplan.fill((0, 0, 0))