YELLOW = (250, 250, 0)
WHITE = (250, 250, 250)
GAME_RESTART_COLOR = YELLOW
GAME_STATS_COLOR = WHITE
GAME_RESTARTS_IN = 1024

# in one loop check blasts, in other check asteroid collisions
CHECK_COLLISION_ASTEROID_BLAST = True
CHECK_COLLISION_ASTEROID_ROCKET = False
CHECK_COLLISION_ASTEROID_ASTEROID = True

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_CAPTION = "Asteroids of Cement (Platypus2nd)"
GAME_LIVES = 3
GAME_BANNER_EDGE_OFFSET = 32
VIRTUAL_SCREEN_EDGE_OFFSET_POSITIVE = 128
VIRTUAL_SCREEN_EDGE_OFFSET_NEGATIVE = -128

BLAST_TTL = 512

MAX_RESPAWN_SPRITE_WIDTH_POSITIVE = 32
MAX_RESPAWN_SPRITE_WIDTH_NEGATIVE = MAX_RESPAWN_SPRITE_WIDTH_POSITIVE * -1

VIRTUAL_SCREEN_RESPAWN_STRIP_LEFT_FROM = VIRTUAL_SCREEN_EDGE_OFFSET_NEGATIVE
VIRTUAL_SCREEN_RESPAWN_STRIP_LEFT_TO = MAX_RESPAWN_SPRITE_WIDTH_NEGATIVE
VIRTUAL_SCREEN_RESPAWN_STRIP_RIGHT_FROM = SCREEN_WIDTH + MAX_RESPAWN_SPRITE_WIDTH_POSITIVE
VIRTUAL_SCREEN_RESPAWN_STRIP_RIGHT_TO = SCREEN_WIDTH + MAX_RESPAWN_SPRITE_WIDTH_POSITIVE \
                                        + VIRTUAL_SCREEN_EDGE_OFFSET_POSITIVE
VIRTUAL_SCREEN_RESPAWN_STRIP_TOP_FROM = VIRTUAL_SCREEN_EDGE_OFFSET_NEGATIVE
VIRTUAL_SCREEN_RESPAWN_STRIP_TOP_TO = MAX_RESPAWN_SPRITE_WIDTH_NEGATIVE
VIRTUAL_SCREEN_RESPAWN_STRIP_BOTTOM_FROM = SCREEN_HEIGHT + MAX_RESPAWN_SPRITE_WIDTH_POSITIVE
VIRTUAL_SCREEN_RESPAWN_STRIP_BOTTOM_TO = SCREEN_HEIGHT + VIRTUAL_SCREEN_EDGE_OFFSET_POSITIVE

ROCKET_INITIAL_X = int(SCREEN_WIDTH / 2)
ROCKET_INITIAL_Y = int(SCREEN_HEIGHT - SCREEN_HEIGHT / 4)
ROCKET_WIDTH = 32
ROCKET_HEIGHT = 32
ROCKET_MIN_X = 0
ROCKET_MAX_X = SCREEN_WIDTH - ROCKET_WIDTH
ROCKET_MIN_Y = 0
ROCKET_MAX_Y = SCREEN_HEIGHT - ROCKET_HEIGHT

FINAL_SCORE_TEXT_ALPHA = 190  # 255
BACKGROUND_STARS_COUNT = 128
MAX_BACKGROUNDS = 8
MAX_ASTEROIDS = 20
FPS_LIMIT = 130

SOUND_FILE_ASTEROID_CLASH = 'sounds/asteroids_clashes/clash_000.wav'
SOUND_VOLUME_ASTEROID_CLASH = 0.7

SOUND_FILE_BLAST = 'sounds/weapons/laser_blast.wav'
SOUND_VOLUME_ROCKET_BLASTER = 0.2


SOUND_FILE_INTRO_MUSIC = 'tracks/track_01.ogg'
SOUND_FILE_LEVEL_MUSIC = 'tracks/track_02.ogg'
SOUND_VOLUME_MUSIC = 0.7  # 0.4
GAME_MUSIC_FADEOUT = 4000

SOUND_FILE_ASTEROID_EXPLOSION = 'sounds/explosions/asteroid_explodes.wav'
SOUND_VOLUME_ASTEROID_EXPLOSION = 0.6

SOUND_FILE_COUNTDOWN_READY = 'sounds/banners/robot_ready.wav'
SOUND_FILE_COUNTDOWN_STEADY = 'sounds/banners/robot_steady.wav'
SOUND_FILE_COUNTDOWN_GO = 'sounds/banners/robot_go.wav'
SOUND_VOLUME_READY_STEADY_GO = 0.6

SOUND_FILE_TREASURE = 'sounds/motivation/treasure.wav'
SOUND_VOLUME_TREASURE = 0.9

SOUND_FILE_THRUST = 'sounds/engines/thrust.wav'
SOUND_VOLUME_ROCKET_ENGINE = 1

SOUND_FILE_ROCKET_EXPLOSION = 'sounds/explosions/ship_explodes.wav'
SOUND_VOLUME_ROCKET_EXPLOSION = 1
