# Asteroids / Cement Game by MQ and Platypus
import pygame
import random
import parameters
import banners
import background
import asteroid
import rocket
import rocket_explosion

# debugging
DEBUG = False

# initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.get_init()

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

game_score = 0
game_lives = 0
game_intro = 0
game_intro_fade_surface = pygame.Surface(parameters.SCREEN_SIZE)
start_new_game = False

# initialize asteroids
asteroids = []
asteroid_explosion_sound = pygame.mixer.Sound(parameters.SOUND_FILE_ASTEROID_EXPLOSION)
asteroid_explosion_sound.set_volume(parameters.SOUND_VOLUME_ASTEROID_EXPLOSION)
asteroid_treasure_sound = pygame.mixer.Sound(parameters.SOUND_FILE_TREASURE)
asteroid_treasure_sound.set_volume(parameters.SOUND_VOLUME_TREASURE)

asteroid_gold_data = asteroid.AsteroidGoldLoader()
asteroid_800_data = asteroid.Asteroid800Loader()
asteroid_802_data = asteroid.Asteroid802Loader()

for i in range(parameters.MAX_ASTEROIDS):
    asteroid_type = random.randint(0, 2)
    if asteroid_type == 0:
        asteroids.append(asteroid.Asteroid(asteroid_gold_data, screen))
    if asteroid_type == 1:
        asteroids.append(asteroid.Asteroid(asteroid_800_data, screen))
    if asteroid_type == 2:
        asteroids.append(asteroid.Asteroid(asteroid_802_data, screen))

# initialize in-game music
pygame.mixer.music.load(parameters.SOUND_FILE_LEVEL_MUSIC)
pygame.mixer.music.set_volume(parameters.SOUND_VOLUME_MUSIC)

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
                    rocket.rocket_engine_sound_plays = True
                    rocket.rocket_thrust_right = True
                    rocket.rocket_direction = 'right'
                if event.key == pygame.K_LEFT:
                    rocket.rocket_engine_sound_plays = True
                    rocket.rocket_thrust_left = True
                    rocket.rocket_direction = 'left'
                if event.key == pygame.K_UP:
                    rocket.rocket_engine_sound_plays = True
                    rocket.rocket_thrust_up = True
                if event.key == pygame.K_DOWN:
                    rocket.rocket_engine_sound_plays = True
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
                    rocket.rocket_engine_sound_plays = False
                    rocket.rocket_thrust_right = False
                    rocket.rocket_direction = 'center'
                if event.key == pygame.K_LEFT:
                    rocket.rocket_engine_sound_plays = False
                    rocket.rocket_thrust_left = False
                    rocket.rocket_direction = 'center'
                if event.key == pygame.K_UP:
                    rocket.rocket_engine_sound_plays = False
                    rocket.rocket_thrust_up = False
                if event.key == pygame.K_DOWN:
                    rocket.rocket_engine_sound_plays = False
                    rocket.rocket_thrust_down = False

        # if rocket is exploding, engines produce no thrust
        if rocket.explosion:
            rocket.rocket_thrust_right = False
            rocket.rocket_thrust_left = False
            rocket.rocket_thrust_up = False
            rocket.rocket_thrust_down = False
            rocket.rocket_engine_sound_plays = False
            rocket.rocket_direction = 'center'

        # redraw background
        background.redraw()

        # update rocket position and redraw rocket (according to rocket conditions)
        rocket.update_position()
        rocket_mask, rocket_x, rocket_y = rocket.get_collision_data_rocket()
        rocket.redraw(rocket.explosion)
        if not rocket.explosion:
            game_score += 1

        # check for asteroids collisions
        if parameters.CHECK_COLLISION_BLASTS:
            parameters.CHECK_COLLISION_BLASTS = False
            for asteroid in asteroids:
                asteroid_mask, asteroid_x, asteroid_y = asteroid.get_collision_data()
                # -= asteroid =- collides with -= blast =-
                if rocket.check_collision_data_blasts(asteroid_mask, asteroid_x, asteroid_y):
                    asteroid.asteroid_hit = True
                    if asteroid.asteroid_hit:
                        asteroid.initial_inertia()
                        if asteroid.asteroid_treasure:
                            game_score += 1000
                            asteroid_explosion_sound.play()
                        else:
                            game_score += 100
                            asteroid_explosion_sound.play()
                    # hack (first explosion, then inertia or asteroid off)
                    asteroid.asteroid_position_x, asteroid.asteroid_position_y, \
                        asteroid.asteroid_acceleration_x, asteroid.asteroid_acceleration_y = asteroid.initial_inertia()
        else:
            parameters.CHECK_COLLISION_BLASTS = True

        if parameters.CHECK_COLLISION_ASTEROIDS:
            parameters.CHECK_COLLISION_ASTEROIDS = False
            for asteroid in asteroids:
                asteroid_mask, asteroid_x, asteroid_y = asteroid.get_collision_data()
                # -= asteroid =- collides with -= rocket =- (if the rocket is fine)
                if not rocket.explosion:
                    asteroid_mask, asteroid_x, asteroid_y = asteroid.get_collision_data()
                    offset_x = rocket_x - asteroid_x
                    offset_y = rocket_y - asteroid_y
                    overlap = asteroid_mask.overlap(rocket_mask, (offset_x, offset_y))
                    if overlap is not None:
                        # -= asteroid =- hit -= rocket =-
                        if asteroid.asteroid_treasure:
                            game_score += 10000
                            asteroid_treasure_sound.play()
                            asteroid.asteroid_position_x, asteroid.asteroid_position_y, \
                            asteroid.asteroid_acceleration_x, asteroid.asteroid_acceleration_y = asteroid.initial_inertia()
                        else:
                            rocket.explosion = True
                            next_game_countdown = parameters.GAME_RESTARTS_IN
                            game_lives -= 1
                            if game_lives == 0:
                                pygame.mixer.music.fadeout(parameters.GAME_MUSIC_FADEOUT)
        else:
            parameters.CHECK_COLLISION_ASTEROIDS = True

        # redraw asteroids
        for asteroid in asteroids:
            asteroid.redraw()

        # draw explosion
        if rocket.explosion:
            rocket.rocket_engine_sound.stop()
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

        # game just run
        if game_intro < 255:
            game_intro_fade_surface.fill((0, 32, 64))
            game_intro_fade_surface.set_alpha(255 - game_intro)
            screen.blit(game_intro_fade_surface, (0, 0))
            game_intro += 1

        # swap buffers
        pygame.display.update()
        clock.tick(parameters.FPS_LIMIT)
