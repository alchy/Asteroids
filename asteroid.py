import pygame
import random


DEBUG = False


class Asteroid:
    def __init__(self, screen):
        self.screen = screen
        self.asteroid_animation_frame = random.randint(0, 19)
        self.asteroid_animation_frame_timer = random.randint(0, 8)
        self.asteroid_image = []
        self.asteroid_mask = []
        for frame in range(1, 21):
            print('[i] Loading asteroids: ')
            load_filename = 'images/asteroid_animated/asteroid_animated_page_' \
                            + str('{:0>4}'.format(frame)) \
                            + '.gif'
            asteroid_image_tmp = pygame.image.load(load_filename)
            self.asteroid_image.append(asteroid_image_tmp)
            self.asteroid_mask.append(pygame.mask.from_surface(asteroid_image_tmp))
        self.asteroid_rect = self.asteroid_image[0].get_rect()
        self.asteroid_position_x, self.asteroid_position_y, \
            self.asteroid_acceleration_x, self.asteroid_acceleration_y = self.initial_inertia()
        self.asteroid_rect.x = int(self.asteroid_position_x)
        self.asteroid_rect.y = int(self.asteroid_position_y)


    def initial_inertia(self):
        # 800x600
        initial_x = random.randint(-200, 1000)
        while initial_x > -100 and initial_x < 900:
            initial_x = random.randint(-200, 1000)
        initial_y = random.randint(-200, 800)
        while initial_y > -100 and initial_y < 700:
            initial_y = random.randint(-200, 800)
        inertia_x = random.uniform(-1.5, +1.5)
        while inertia_x == 0.0:
            inertia_x = random.uniform(-1.5, +1.5)
        inertia_y = random.uniform(-1.5, +1.5)
        while inertia_y == 0.0:
            inertia_y = random.uniform(-1.5, +1.5)

        return(float(initial_x), float(initial_y), \
              float(inertia_x), float(inertia_y))


    def recalculate_position(self):
        self.asteroid_position_x += self.asteroid_acceleration_x
        self.asteroid_position_y += self.asteroid_acceleration_y
        self.asteroid_rect.x = int(self.asteroid_position_x)
        self.asteroid_rect.y = int(self.asteroid_position_y)
        if self.asteroid_rect.x > 1000 or self.asteroid_rect.x < -200 \
                or self.asteroid_position_y > 800 or self.asteroid_position_y < -200:
            if DEBUG:
                print("Inertia reset...")
            self.asteroid_position_x, self.asteroid_position_y, \
            self.asteroid_acceleration_x, self.asteroid_acceleration_y = self.initial_inertia()

        #print(self.asteroid_rect.x, self.asteroid_rect.y)


    def get_collision_data(self):
        return(self.asteroid_mask[self.asteroid_animation_frame], \
               self.asteroid_rect.x, self.asteroid_rect.y, )


    def redraw(self):
        self.recalculate_position()
        self.asteroid_animation_frame_timer += 1
        if self.asteroid_animation_frame_timer > 8:
            self.asteroid_animation_frame_timer = 0
            self.asteroid_animation_frame += 1
        if self.asteroid_animation_frame > 19:
            self.asteroid_animation_frame = 0
        self.screen.blit(self.asteroid_image[self.asteroid_animation_frame], \
                         (self.asteroid_rect.x, self.asteroid_rect.y))
