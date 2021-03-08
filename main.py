# Game by MQ and Platypus
import pygame
import parameters
import banners
import background
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
game_lives = parameters.GAME_LIVES

# initialize screen
screen = pygame.display.set_mode(parameters.SCREEN_SIZE)
pygame.display.set_caption(parameters.SCREEN_CAPTION)

# initialize background
background = background.Background(screen)

# initialize in-game gauges (aka banners)
banners = banners.Banners(screen)

# initialize rocket and rocket_explosion, which are separate objects
# this also resets rocket_explosion and rocket_destroyed
rocket = rocket.Rocket(screen)
rocket_explosion = rocket_explosion.RocketExplosion(screen)

# initialize asteroids
asteroids = []
asteroid_explosion_sound = pygame.mixer.Sound('sounds/rocket_explodes.wav')
asteroid_explosion_sound.set_volume(0.3)
for i in range(MAX_ASTEROIDS):
    asteroids.append(asteroid.Asteroid(screen))

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
    background.redraw()

    # update rocket position and redraw rocket (according to rocket conditions)
    rocket.update_position()
    rocket.redraw(rocket.explosion)
    if not rocket.explosion:
        game_score += 1

    # check for asteroids collisions
    rocket_mask, rocket_x, rocket_y = rocket.get_collision_data_rocket()
    for asteroid in asteroids:
        asteroid.redraw()
        asteroid_mask, asteroid_x, asteroid_y = asteroid.get_collision_data()
        # -= asteroid =- collides with -= blast =-
        if rocket.check_collision_data_blasts(asteroid_mask, asteroid_x, asteroid_y):
            asteroid.asteroid_hit = True
            game_score += 100
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

    # print in-game stats all the time
    banners.game_stats(clock.get_fps(), game_score, game_lives)

    # handle game restarts
    if game_lives == 0:
        running = False
        print("Your Score is: ", game_score)
    else:
        if rocket_explosion.rocket_destroyed:
            if banners.game_restarts():
                next_game_countdown = GAME_RESTARTS_IN
                rocket_explosion.rocket_destroyed = False
                rocket.reset_rocket()
                background_scroll_in_y = 0

    # swap buffers
    pygame.display.update()
    clock.tick(120)