# https://www.youtube.com/watch?v=UZg49z76cLw

import pygame
import random
import time
import asteroid
import rocket
import rocket_explosion

# debugging
DEBUG = False

# initalize parameters
MAX_ASTEROIDS = 10

# initialize pygame
print(pygame.init())
print(pygame.font.init())
print(pygame.mixer.get_init())

# initialize game contents
game_lives = 3
game_countdown = 1024

# initialize screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Asteroids")

# initialize rocket
rocket = rocket.Rocket(screen)

# initialize rocket_explosion, which is separate object from rocket
# this also resets rocket_explosion and rocket_destroyed
rocket_explosion = rocket_explosion.RocketExplosion(screen)

# initialize asteroids
asteroids = []
for i in range(MAX_ASTEROIDS):
    asteroids.append(asteroid.Asteroid(screen))

# text features, prerender first text
FPS_TEXT_COLOUR = (255, 255, 0)
game_font = pygame.font.SysFont('Trebuchet MS', 16)
text_info_fps = game_font.render('FPS', False, FPS_TEXT_COLOUR)

# https://wallup.net/outer-space-galaxies-planets/
background = pygame.image.load('images/outer-1614965066305-5634.jpg')
background_scroll_in_x = 0
background_scroll_in_x_amount = 0 #-0.2
background_scroll_in_y = 0
background_scroll_in_y_amount = 0 #0.2

# init clocks
clock = pygame.time.Clock()

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                rocket.rocket_thrust_right = True
            if event.key == pygame.K_LEFT:
                rocket.rocket_thrust_left = True
            if event.key == pygame.K_UP:
                rocket.rocket_thrust_up = True
            if event.key == pygame.K_DOWN:
                rocket.rocket_thrust_down = True
            if event.key == pygame.K_SPACE:
                rocket.blaster_triggered = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                rocket.rocket_thrust_right = False
            if event.key == pygame.K_LEFT:
                rocket.rocket_thrust_left = False
            if event.key == pygame.K_UP:
                rocket.rocket_thrust_up = False
            if event.key == pygame.K_DOWN:
                rocket.rocket_thrust_down = False

    # if rocket is exploding, engines produce no thrust
    if rocket.explosion:
        rocket.rocket_thrust_right = False
        rocket.rocket_thrust_left = False
        rocket.rocket_thrust_up = False
        rocket.rocket_thrust_down = False

    # draw background
    screen.blit(background, (int(background_scroll_in_x), int(background_scroll_in_y)))
    background_scroll_in_x += background_scroll_in_x_amount
    background_scroll_in_y += background_scroll_in_y_amount

    # update rocket position all the time regardless the damage
    rocket.update_position()

    # redraw rocket
    if not rocket.explosion:
        rocket.redraw()

    # check for asteroids collisions
    rocket_mask, rocket_x, rocket_y = rocket.get_collision_data_rocket()
    for asteroid in asteroids:
        asteroid.redraw()
        asteroid_mask, asteroid_x, asteroid_y = asteroid.get_collision_data()
        # -= asteroid =- collides with -= blast =-
        if rocket.check_collision_data_blasts(asteroid_mask, asteroid_x, asteroid_y):
            asteroid.asteroid_hit = True
            asteroid.initial_inertia()
            # hack (fisrt explosion, then inertia or asteroid off)
            asteroid.asteroid_position_x, asteroid.asteroid_position_y, \
                asteroid.asteroid_acceleration_x, asteroid.asteroid_acceleration_y = asteroid.initial_inertia()
            print("HIT!")

        # -= asteroid =- collides with -= rocket =- (if the rocket is fine)
        if not rocket.explosion:
            asteroid_mask, asteroid_x, asteroid_y = asteroid.get_collision_data()
            offset_x = rocket_x - asteroid_x
            offset_y = rocket_y - asteroid_y
            overlap = asteroid_mask.overlap(rocket_mask, (offset_x, offset_y))
            if overlap is not None:
                # -= asteroid =- hit -= rocket =-
                rocket.explosion = True

    # draw explosion
    if rocket.explosion:
        rocket_explosion.redraw(rocket_x, rocket_y)

    # check FPS performance, randomly
    if random.randint(0, 100) == 0:
        fps = str(int((clock.get_fps())))
        text_info_fps = game_font.render('FPS:' + fps, False, FPS_TEXT_COLOUR)

    # all the time draw the FPS performance
    screen.blit(text_info_fps, (8, 8))

    # swap buffers
    pygame.display.update()
    clock.tick(120)

    # for every new game this must be reset
    #rocket.explosion = False
    #self.rocket_destroyed = False
    #self.rocket.rocket_blast = False