# Asteroids / Cement Game by MQ and Platypus
import pygame
import parameters
import banners
import background
import asteroid
import rocket
import rocket_explosion

# debugging
DEBUG = False

# initialize pygame
print(pygame.init())
print(pygame.font.init())
print(pygame.mixer.get_init())

# initialize screen
flags = pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE
screen = pygame.display.set_mode(parameters.SCREEN_SIZE, flags, vsync=0)
pygame.display.set_caption(parameters.SCREEN_CAPTION)

# initialize background
background = background.Background(screen)

# initialize in-game gauges (aka banners)
banners = banners.Banners(screen)

# initialize rocket and rocket_explosion, which are separate objects
# this also resets rocket_explosion and rocket_destroyed
rocket = rocket.Rocket(screen)
rocket.explosion = True

rocket_explosion = rocket_explosion.RocketExplosion(screen)
rocket_explosion.rocket_destroyed = True

MAX_ASTEROIDS = 16
game_score = 0
game_lives = 0
start_new_game = False

# initialize asteroids
asteroids = []
asteroid_explosion_sound = pygame.mixer.Sound('sounds/explosions/asteroid_explodes.wav')
asteroid_explosion_sound.set_volume(0.4)
for i in range(MAX_ASTEROIDS):
    asteroids.append(asteroid.Asteroid(screen))

# initialize in-game music
pygame.mixer.music.load("tracks/track_01.ogg")
pygame.mixer.music.set_volume(0.3)

# init clocks
clock = pygame.time.Clock()
fps = 0

if __name__ == "__main__":
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
                    if game_lives:
                        rocket.blaster_triggered = True
                    else:
                        start_new_game = True
                if event.key == pygame.K_ESCAPE:
                    running = False
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

        # check for asteroids collisions (cheat, if necessary, do collision checking each even frame, redraw every frame)
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
                # hack (first explosion, then inertia or asteroid off)
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
                    next_game_countdown = parameters.GAME_RESTARTS_IN
                    game_lives -= 1
                    if game_lives == 0:
                        pygame.mixer.music.fadeout(5000)

        # draw explosion
        if rocket.explosion:
            rocket_explosion.redraw(rocket_x, rocket_y)

        # print in-game stats all the time
        fps = int((fps + clock.get_fps()) / 2)
        banners.game_stats(fps, game_score, game_lives)

        # handle game restarts
        if game_lives == 0:
            if start_new_game:
                if banners.game_restarts():
                    game_lives = parameters.GAME_LIVES
                    game_score = 0
                    rocket.explosion = False
                    rocket_explosion.rocket_destroyed = False
                    start_new_game = False
                    pygame.mixer.music.play(1)
            else:
                banners.game_your_score(game_score)
        else:
            if rocket_explosion.rocket_destroyed:
                if banners.game_restarts():
                    next_game_countdown = parameters.GAME_RESTARTS_IN
                    rocket_explosion.rocket_destroyed = False
                    rocket.reset_rocket()
                    background_scroll_in_y = 0

        # swap buffers
        pygame.display.update()
        clock.tick(parameters.FPS_LIMIT)
