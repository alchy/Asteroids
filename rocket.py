import pygame

class Rocket:
    def __init__(self, screen):
        self.screen = screen
        # https://www.flaticon.com/search?search-type=icons&word=arcade+space&license=&color=&stroke=&current_section=&author_id=&pack_id=&family_id=&style_id=&category_id=
        self.rocket_image = pygame.image.load('images/space-invaders.png')
        self.rocket_mask = pygame.mask.from_surface(self.rocket_image)
        self.rocket_rect = self.rocket_image.get_rect()
        self.rocket_x = 370
        self.rocket_y = 480
        self.rocket_acceleration_step = 0.02
        self.rocket_acceleration_actual_x = 0.0
        self.rocket_acceleration_actual_y = 0.0
        self.rocket_acceleration_x = 0.05
        self.rocket_acceleration_y = 0.0
        self.rocket_thrust_left = False
        self.rocket_thrust_right = False
        self.rocket_thrust_up = False
        self.rocket_thrust_down = False
        self.explosion = False


    def get_collision_data(self):
        return(self.rocket_mask, int(self.rocket_x), int(self.rocket_y))


    def redraw(self, exploded):
        if self.rocket_thrust_left:
            self.rocket_acceleration_actual_x -= self.rocket_acceleration_step
        if self.rocket_thrust_right:
            self.rocket_acceleration_actual_x += self.rocket_acceleration_step
        self.rocket_x += self.rocket_acceleration_actual_x
        if self.rocket_thrust_up:
            self.rocket_acceleration_actual_y -= self.rocket_acceleration_step
        if self.rocket_thrust_down:
            self.rocket_acceleration_actual_y += self.rocket_acceleration_step
        self.rocket_y += self.rocket_acceleration_actual_y

        if self.rocket_x < 0:
            self.rocket_x = 0
            self.rocket_acceleration_x = 0
        if self.rocket_x > (800 - 32):
            self.rocket_x = 800 - 32
            self.rocket_acceleration_x = 0
        if self.rocket_y < 0:
            self.rocket_y = 0
            self.rocket_acceleration_y = 0
        if self.rocket_y > (600 - 32):
            self.rocket_y = (600 - 32)
            self.rocket_acceleration_y = 0

        if not exploded:
            self.screen.blit(self.rocket_image, (self.rocket_x, self.rocket_y))
