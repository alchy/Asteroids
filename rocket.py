import pygame
import rocket_blaster
import parameters

MUTE_SOUND = False


class Rocket:
    def __init__(self, screen):
        self.screen = screen
        # https://www.flaticon.com/search?search-type=icons&word=arcade+space&license=&color=&stroke=&current_section=&author_id=&pack_id=&family_id=&style_id=&category_id=
        self.rocket_direction = 'center'
        self.rocket_image = {}
        for (str_nr, direction) in (('0001', 'left'), ('0002', 'center'), ('0003', 'right')):
            image_name = 'images/rockets/blender_output' + str_nr + '.png'
            print(image_name)
            self.rocket_image[direction] = pygame.image.load(image_name)
        self.rocket_mask = pygame.mask.from_surface(self.rocket_image['center'])
        self.rocket_blaster_sound = pygame.mixer.Sound(parameters.SOUND_FILE_BLAST)
        self.rocket_blaster_sound.set_volume(parameters.SOUND_VOLUME_ROCKET_BLASTER)
        self.rocket_engine_sound = pygame.mixer.Sound(parameters.SOUND_FILE_THRUST)
        self.rocket_engine_sound_plays = False
        self.rocket_engine_sound_last = self.rocket_engine_sound_plays
        self.rocket_rect = self.rocket_image['center'].get_rect()
        self.rocket_x = parameters.ROCKET_INITIAL_X
        self.rocket_y = parameters.ROCKET_INITIAL_Y
        self.rocket_acceleration_step = 0.025
        self.rocket_acceleration_actual_x = 0.0
        self.rocket_acceleration_actual_y = 0.0
        self.rocket_acceleration_x = 0.0
        self.rocket_acceleration_y = 0.0
        self.rocket_thrust_left = False
        self.rocket_thrust_right = False
        self.rocket_thrust_up = False
        self.rocket_thrust_down = False
        self.explosion = False
        self.blaster_triggered = False
        self.rocket_blaster = rocket_blaster.RocketBlaster(self.screen)

    def reset_rocket(self):
        self.rocket_x = parameters.ROCKET_INITIAL_X
        self.rocket_y = parameters.ROCKET_INITIAL_Y
        self.rocket_acceleration_actual_x = 0.0
        self.rocket_acceleration_actual_y = 0.0
        self.rocket_acceleration_x = 0.0
        self.rocket_acceleration_y = 0.0
        self.rocket_thrust_left = False
        self.rocket_thrust_right = False
        self.rocket_thrust_up = False
        self.rocket_thrust_down = False
        self.explosion = False

    def get_collision_data_rocket(self):
        return self.rocket_mask, int(self.rocket_x), int(self.rocket_y)

    def check_collision_data_blasts(self, object_mask, object_x, object_y):
        return self.rocket_blaster.check_collision(object_mask, object_x, object_y)

    def update_position(self):
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

        if self.rocket_x < parameters.ROCKET_MIN_X:
            self.rocket_x = parameters.ROCKET_MIN_X
            self.rocket_acceleration_x = self.rocket_acceleration_x * -1
            self.rocket_acceleration_actual_x = self.rocket_acceleration_actual_x * -1
        if self.rocket_x > parameters.ROCKET_MAX_X:
            self.rocket_x = parameters.ROCKET_MAX_X
            self.rocket_acceleration_x = self.rocket_acceleration_x * -1
            self.rocket_acceleration_actual_x = self.rocket_acceleration_actual_x * -1
        if self.rocket_y < parameters.ROCKET_MIN_Y:
            self.rocket_y = parameters.ROCKET_MIN_Y
            self.rocket_acceleration_y = self.rocket_acceleration_y * -1
            self.rocket_acceleration_actual_y = self.rocket_acceleration_actual_y * -1
        if self.rocket_y > parameters.ROCKET_MAX_Y:
            self.rocket_y = parameters.ROCKET_MAX_Y
            self.rocket_acceleration_y = self.rocket_acceleration_y * -1
            self.rocket_acceleration_actual_y = self.rocket_acceleration_actual_y * -1

    def redraw(self, explosion):
        # redraw bullets
        self.rocket_blaster.redraw()
        if not explosion:
            # redraw rocket
            self.screen.blit(self.rocket_image[self.rocket_direction], (self.rocket_x, self.rocket_y))
            # rocket engine sound in vacuum
            if self.rocket_engine_sound_plays != self.rocket_engine_sound_last:
                self.rocket_engine_sound_last = self.rocket_engine_sound_plays
                if self.rocket_engine_sound_plays:
                    self.rocket_engine_sound.play(-1)
                else:
                    self.rocket_engine_sound.stop()
            # fire bullet
            if self.blaster_triggered:
                if not MUTE_SOUND:
                    self.rocket_blaster_sound.play()
                self.rocket_blaster.new_blast(self.rocket_x, self.rocket_y,
                                              self.rocket_acceleration_actual_x, self.rocket_acceleration_actual_y)
                self.blaster_triggered = False
