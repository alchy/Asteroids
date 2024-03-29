import pygame
import parameters
import random

DEBUG = False


class AsteroidGoldLoader:
    def __init__(self):
        # gold asteroid
        self.mass = 1
        self.asteroid_animation_frame_timer_limit = 3
        self.asteroid_image = []
        self.asteroid_mask = []
        self.asteroid_frames = 30
        for frame in range(0, self.asteroid_frames):
            load_filename = 'images/asteroid_animated_908/blender_output' \
                            + str('{:0>4}'.format(frame)) \
                            + '.png'
            print(load_filename)
            asteroid_image_tmp = pygame.image.load(load_filename)
            self.asteroid_image.append(asteroid_image_tmp)
            self.asteroid_mask.append(pygame.mask.from_surface(asteroid_image_tmp))
            self.asteroid_treasure = True


class Asteroid800Loader:
    def __init__(self):
        # 800 asteroid
        self.mass = 5
        self.asteroid_frames = 30
        self.asteroid_animation_frame_timer_limit = 3
        self.asteroid_image = []
        self.asteroid_mask = []
        self.asteroid_frames = 29
        for frame in range(0, self.asteroid_frames + 1):
            load_filename = 'images/asteroid_animated_800/' \
                            + str('{:0>4}'.format(frame)) \
                            + '.png'
            asteroid_image_tmp = pygame.image.load(load_filename)
            self.asteroid_image.append(asteroid_image_tmp)
            self.asteroid_mask.append(pygame.mask.from_surface(asteroid_image_tmp))
            self.asteroid_treasure = False


class Asteroid802Loader:
    def __init__(self):
        # 802 asteroid
        self.mass = 2
        self.asteroid_animation_frame_timer_limit = 3
        self.asteroid_image = []
        self.asteroid_mask = []
        self.asteroid_frames = 29
        for frame in range(0, self.asteroid_frames + 1):
            load_filename = 'images/asteroid_animated_802/' \
                            + str('{:0>4}'.format(frame)) \
                            + '.png'
            asteroid_image_tmp = pygame.image.load(load_filename)
            self.asteroid_image.append(asteroid_image_tmp)
            self.asteroid_mask.append(pygame.mask.from_surface(asteroid_image_tmp))
            self.asteroid_treasure = False


class AsteroidLavaBig:
    def __init__(self):
        # 802 asteroid
        self.mass = 2
        self.asteroid_animation_frame_timer_limit = 1
        self.asteroid_image = []
        self.asteroid_mask = []
        self.asteroid_frames = 36
        for frame in range(1, self.asteroid_frames + 1):
            load_filename = 'images/asteroid_lava_big/' \
                            + str('{:0>4}'.format(frame)) \
                            + '.png'
            asteroid_image_tmp = pygame.image.load(load_filename)
            self.asteroid_image.append(asteroid_image_tmp)
            self.asteroid_mask.append(pygame.mask.from_surface(asteroid_image_tmp))
            self.asteroid_treasure = False


class AsteroidLoader:
    def __init__(self, screen):
        self.screen = screen
        self.asteroid_gold_data = AsteroidGoldLoader()
        self.asteroid_800_data = Asteroid800Loader()
        self.asteroid_802_data = Asteroid802Loader()
        self.asteroid_lava_big = AsteroidLavaBig()

    def reset(self, count_of_asteroids):
        asteroids = []
        for asteroid_id in range(count_of_asteroids):
            asteroid_type = random.randint(0, 3)
            if asteroid_type == 0:
                asteroids.append(Asteroid(self.asteroid_gold_data, self.screen))
            if asteroid_type == 1:
                asteroids.append(Asteroid(self.asteroid_800_data, self.screen))
            if asteroid_type == 2:
                asteroids.append(Asteroid(self.asteroid_802_data, self.screen))
            if asteroid_type == 3:
                asteroids.append(Asteroid(self.asteroid_lava_big, self.screen))
        return asteroids


class Asteroid:
    def __init__(self, asteroid_data, screen):
        self.screen = screen
        self.asteroid_image = asteroid_data.asteroid_image
        self.asteroid_mask = asteroid_data.asteroid_mask
        self.collision_buffer = []
        self.width = asteroid_data.asteroid_image[0].get_width()
        self.height = asteroid_data.asteroid_image[0].get_height()
        self.asteroid_animation_frame = random.randint(0, 19)
        self.asteroid_animation_frame_timer = random.randint(0, 8)
        self.asteroid_frames = asteroid_data.asteroid_frames
        self.asteroid_animation_frame_timer_limit = 3
        self.asteroid_treasure = asteroid_data.asteroid_treasure
        self.asteroid_position_x, self.asteroid_position_y, \
            self.asteroid_acceleration_x, self.asteroid_acceleration_y = self.initial_inertia()
        self.mass = asteroid_data.mass
        self.asteroid_hit = False
        self.asteroid_destroyed = False

    def in_collision(self, other_asteroid):
        offset_x_a = other_asteroid.asteroid_position_x - self.asteroid_position_x
        offset_x_b = other_asteroid.asteroid_position_x + other_asteroid.width - self.asteroid_position_x + self.width
        offset_y_a = other_asteroid.asteroid_position_y - self.asteroid_position_y
        offset_y_b = other_asteroid.asteroid_position_y + other_asteroid.width - self.asteroid_position_y + self.width
        if offset_x_a < self.width and offset_x_b > 0 and offset_y_a < self.height and offset_y_b > 0:
            return True

        f = 3  # extend to future frames
        for f in range(1, f + 1):
            offset_x_a = other_asteroid.asteroid_position_x + (f * other_asteroid.asteroid_acceleration_x) \
                - self.asteroid_position_x + (f * self.asteroid_acceleration_x)
            offset_x_b = other_asteroid.asteroid_position_x + (f * self.asteroid_acceleration_x) \
                         + other_asteroid.width - self.asteroid_position_x + self.width + (f * self.asteroid_acceleration_x)
            offset_y_a = other_asteroid.asteroid_position_y + (f * self.asteroid_acceleration_y) \
                         - self.asteroid_position_y + (f * self.asteroid_acceleration_y)
            offset_y_b = other_asteroid.asteroid_position_y + (f * self.asteroid_acceleration_y) \
                         + other_asteroid.width - self.asteroid_position_y + self.width + (f * self.asteroid_acceleration_y)
            if offset_x_a < self.width and offset_x_b > 0 and offset_y_a < self.height and offset_y_b > 0:
                return True

        return False

    def in_viewport(self):
        if self.asteroid_position_x < parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_LEFT_TO:
            return False
        elif self.asteroid_position_x > parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_RIGHT_FROM:
            return False
        elif self.asteroid_position_y < parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_TOP_TO:
            return False
        elif self.asteroid_position_y > parameters.VIRTUAL_SCREEN_RESPAWN_STRIP_BOTTOM_FROM:
            return False
        else:
            return True

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

        inertia_x = random.uniform(-2.5, +2.5)
        while inertia_x == 0.0:
            inertia_x = random.uniform(-2.5, +2.5)
        inertia_y = random.uniform(-2.5, +2.5)
        while inertia_y == 0.0:
            inertia_y = random.uniform(-2.5, +2.5)
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
