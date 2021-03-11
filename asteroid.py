import pygame
import parameters
import random

DEBUG = False


class Asteroid:
    def __init__(self, screen):
        self.screen = screen
        self.asteroid_animation_frame = random.randint(0, 19)
        self.asteroid_animation_frame_timer = random.randint(0, 8)
        self.asteroid_image = []
        self.asteroid_mask = []

        if random.randint(0, 15) == 0:
            self.asteroid_frames = 30
            self.asteroid_animation_frame_timer_limit = 3
            for frame in range(1, self.asteroid_frames + 1):
                load_filename = 'images/asteroid_animated_gold/asteroid_animated_gold_page_' \
                                + str('{:0>4}'.format(frame)) \
                                + '.gif'
                asteroid_image_tmp = pygame.image.load(load_filename)
                self.asteroid_image.append(asteroid_image_tmp)
                self.asteroid_mask.append(pygame.mask.from_surface(asteroid_image_tmp))
        else:
            self.asteroid_frames = 20
            self.asteroid_animation_frame_timer_limit = 8
            for frame in range(1, self.asteroid_frames + 1):
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
        self.asteroid_hit = False
        self.asteroid_destroyed = False

    @staticmethod
    def initial_inertia():
        if random.randint(0, 1):
            initial_x = random.randint(parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_LEFT_FROM,
                                       parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_LEFT_TO)
        else:
            initial_x = random.randint(parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_RIGHT_FROM,
                                       parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_RIGHT_TO)
        if random.randint(0, 1):
            initial_y = random.randint(parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_TOP_FROM,
                                       parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_TOP_TO)
        else:
            initial_y = random.randint(parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_BOTTOM_FROM,
                                       parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_BOTTOM_TO)
        inertia_x = random.uniform(-1.5, +1.5)
        while inertia_x == 0.0:
            inertia_x = random.uniform(-1.5, +1.5)
        inertia_y = random.uniform(-1.5, +1.5)
        while inertia_y == 0.0:
            inertia_y = random.uniform(-1.5, +1.5)
        return (float(initial_x), float(initial_y),
                float(inertia_x), float(inertia_y))

    def recalculate_position(self):
        self.asteroid_position_x += self.asteroid_acceleration_x
        self.asteroid_position_y += self.asteroid_acceleration_y
        if self.asteroid_position_x < parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_LEFT_FROM or \
                self.asteroid_position_x > parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_RIGHT_TO or \
                self.asteroid_position_y < parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_TOP_FROM or \
                self.asteroid_position_y > parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_BOTTOM_TO:
            # inertia reset
            self.asteroid_position_x, self.asteroid_position_y, \
                self.asteroid_acceleration_x, self.asteroid_acceleration_y = self.initial_inertia()

    def get_collision_data(self):
        return (self.asteroid_mask[self.asteroid_animation_frame],
                int(self.asteroid_position_x), int(self.asteroid_position_y))

    def redraw(self):
        self.recalculate_position()
        self.asteroid_animation_frame_timer += 1
        if self.asteroid_animation_frame_timer > self.asteroid_animation_frame_timer_limit:
            self.asteroid_animation_frame_timer = 0
            self.asteroid_animation_frame += 1
        if self.asteroid_animation_frame > self.asteroid_frames - 1:
            self.asteroid_animation_frame = 0
        self.screen.blit(self.asteroid_image[self.asteroid_animation_frame],
                         (int(self.asteroid_position_x), int(self.asteroid_position_y)))
