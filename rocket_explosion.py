import pygame

MUTE_SOUND = False

class RocketExplosion:
    def __init__(self, screen):
        self.screen = screen
        self.rocket_explosion_animation_frame_timer = 0
        self.rocket_explosion_animation_frame = 0
        self.rocket_explosion_image = []
        self.rocket_destroyed = False
        self.explosion_sound = pygame.mixer.Sound('sounds/explosions/arcade_game_ship_explosion_simple.wav')
        self.explosion_sound.set_volume(0.5)
        for frame in range(1, 13):
            print('[i] Loading explosion: ')
            load_filename = 'images/explosion_animated/rocket_explosion_page_' \
                            + str('{:0>4}'.format(frame)) \
                            + '.gif'
            explosion_image_tmp = pygame.image.load(load_filename)
            self.rocket_explosion_image.append(explosion_image_tmp)

    def redraw(self, rocket_explosion_x, rocket_explosion_y):
        if not self.rocket_destroyed:
            if self.rocket_explosion_animation_frame_timer > 16:
                self.rocket_explosion_animation_frame += 1
                self.rocket_explosion_animation_frame_timer = 0
            if self.rocket_explosion_animation_frame > 11:
                self.rocket_explosion_animation_frame = 0
                self.rocket_destroyed = True
            self.rocket_explosion_animation_frame_timer += 1
            self.screen.blit(self.rocket_explosion_image[self.rocket_explosion_animation_frame], \
                             (rocket_explosion_x - 16, rocket_explosion_y - 16))
            if not MUTE_SOUND:
                if self.rocket_explosion_animation_frame == 0:
                    self.explosion_sound.play()