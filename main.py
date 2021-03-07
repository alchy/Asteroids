# Game by MQ and Platypus

import pygame
import random
import asteroid
import rocket
import rocket_explosion

# debugging
DEBUG = False

# initalize parameters
MAX_ASTEROIDS = 16
GAME_LIVES = 3
GAME_RESTARTS_IN = 1024

# initialize pygame
print(pygame.init())
print(pygame.font.init())
print(pygame.mixer.get_init())

# initialize game contents
game_score = 0
game_lives = GAME_LIVES
next_game_countdown = GAME_RESTARTS_IN


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
asteroid_explosion_sound = pygame.mixer.Sound('sounds/rocket_explodes.wav')
asteroid_explosion_sound.set_volume(0.3)
for i in range(MAX_ASTEROIDS):
    asteroids.append(asteroid.Asteroid(screen))


# text features, prerender first text
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
game_font_small = pygame.font.SysFont('Trebuchet MS', 16)
game_font_big = pygame.font.SysFont('Trebuchet MS', 16)


# https://wallup.net/outer-space-galaxies-planets/
background = pygame.image.load('images/outer-1614965066305-5634.jpg')
background_scroll_in_x = 0
background_scroll_in_x_amount = 0 #-0.2
background_scroll_in_y = 0
background_scroll_in_y_amount = 0 #0.01

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

    # always call this, redraw rocket and bullets according to rocket condition
    rocket.redraw(rocket.explosion)

    # check for asteroids collisions
    rocket_mask, rocket_x, rocket_y = rocket.get_collision_data_rocket()
    for asteroid in asteroids:
        asteroid.redraw()
        asteroid_mask, asteroid_x, asteroid_y = asteroid.get_collision_data()
        # -= asteroid =- collides with -= blast =-
        if rocket.check_collision_data_blasts(asteroid_mask, asteroid_x, asteroid_y):
            asteroid.asteroid_hit = True
            game_score += 10
            asteroid_explosion_sound.play()
            asteroid.initial_inertia()
            # hack (fisrt explosion, then inertia or asteroid off)
            asteroid.asteroid_position_x, asteroid.asteroid_position_y, \
                asteroid.asteroid_acceleration_x, asteroid.asteroid_acceleration_y = asteroid.initial_inertia()
        # -= asteroid =- collides with -= rocket =- (if the rocket is fine)
        if not rocket.explosion:
            asteroid_mask, asteroid_x, asteroid_y = asteroid.get_collision_data()
            offset_x = rocket_x - asteroid_x
            offset_y = rocket_y - asteroid_y
            overlap = asteroid_mask.overlap(rocket_mask, (offset_x, offset_y))
            if overlap is not None:
                # -= asteroid =- hit -= rocket =-
                rocket.explosion = True
                game_lives -= 1
                next_game_countdown = GAME_RESTARTS_IN

    # draw explosion
    if rocket.explosion:
        rocket_explosion.redraw(rocket_x, rocket_y)


    # draw stats
    text_info_fps = game_font_small.render('FPS:' + str(int((clock.get_fps()))), False, YELLOW)
    text_info_score = game_font_big.render('SCORE:' + '{:0>5}'.format(str(game_score)), False, YELLOW)
    text_info_lives = game_font_big.render('LIVES:' + '{:0>2}'.format(str(game_lives)), False, YELLOW)
    screen.blit(text_info_fps, (8, 8))
    screen.blit(text_info_score, (350, 8))
    screen.blit(text_info_lives, (730, 8))

    if game_lives == 0:
        running = False
    else:
        if rocket_explosion.rocket_destroyed:
            if next_game_countdown == int(GAME_RESTARTS_IN / 4) * 4:
                text_info_countdown = game_font_big.render("LEVEL RESTART IN 4", False, WHITE)
            if next_game_countdown == int(GAME_RESTARTS_IN / 4) * 3:
                text_info_countdown = game_font_big.render("LEVEL RESTART IN 3", False, WHITE)
            if next_game_countdown == int(GAME_RESTARTS_IN / 4) * 2:
                text_info_countdown = game_font_big.render("LEVEL RESTART IN 2", False, WHITE)
            if next_game_countdown == int(GAME_RESTARTS_IN / 4) * 1:
                text_info_countdown = game_font_big.render("LEVEL RESTART IN 1", False, WHITE)
            screen.blit(text_info_countdown, (340, 550))
            next_game_countdown -= 1
            if next_game_countdown == 0:
                next_game_countdown = GAME_RESTARTS_IN
                rocket_explosion.rocket_destroyed = False
                rocket.reset_rocket()
                background_scroll_in_y = 0

    # swap buffers
    pygame.display.update()
    clock.tick(120)
