import pygame
import parameters


class Banners:
    def __init__(self, screen):
        self.screen = screen

        #
        self.next_game_countdown = parameters.GAME_RESTARTS_IN

        # init game fonts
        self.game_font_small = pygame.font.Font('fonts/supercomputer.ttf', 20)
        self.game_font_large = pygame.font.Font('fonts/supercomputer.ttf', 64)
        self.game_font_extra = pygame.font.Font('fonts/supercomputer.ttf', 128)

        # init and compute position of "FPS: ..." banner
        self.text_info_fps = self.game_font_small.render('FPS: ' + '{:0>3}'.format(str(0)),
                                                         False, parameters.GAME_STATS_COLOR)
        self.TEXT_FPS_POS = (parameters.GAME_BANNER_EDGE_OFFSET, parameters.GAME_BANNER_EDGE_OFFSET)

        # init and compute position of "SCORE: ..." banner
        self.text_info_score = self.game_font_small.render('SCORE: ' + '{:0>8}'.format(str(int(0))),
                                                           False, parameters.GAME_STATS_COLOR)
        text_pos_x, text_pos_y = self.text_info_score.get_rect().bottomright
        self.TEXT_SCORE_POS = ((int((parameters.SCREEN_WIDTH - text_pos_x) / 2)), parameters.GAME_BANNER_EDGE_OFFSET)

        # init and compute position of "LIVES/COINS: ..." banner
        self.text_info_lives = self.game_font_small.render('COINS: ' + '{:0>2}'.format(str(int(0))),
                                                           False, parameters.GAME_STATS_COLOR)
        text_pos_x, text_pos_y = self.text_info_lives.get_rect().bottomright
        self.TEXT_LIVES_POS = (int(parameters.SCREEN_WIDTH - text_pos_x - parameters.GAME_BANNER_EDGE_OFFSET),
                               parameters.GAME_BANNER_EDGE_OFFSET)

        # init and compute position of "YOUR SCORE ..." banner
        self.text_info_final_score = self.game_font_large.render("12345678", False, parameters.GAME_RESTART_COLOR)
        self.TEXT_LEVEL_FINAL_SCORE_POS = []
        for screen, banner in zip(parameters.SCREEN_SIZE,
                                  self.text_info_final_score.get_rect().bottomright):
            self.TEXT_LEVEL_FINAL_SCORE_POS.append(int((screen - banner) / 2))
        # init banner voice
        self.sound_ready = pygame.mixer.Sound('sounds/banners/robot_ready.wav')
        self.sound_ready.set_volume(0.3)
        self.sound_steady = pygame.mixer.Sound('sounds/banners/robot_steady.wav')
        self.sound_steady.set_volume(0.3)
        self.sound_go = pygame.mixer.Sound('sounds/banners/robot_go.wav')
        self.sound_go.set_volume(0.3)

    def game_stats(self, actual_fps, game_score, game_lives):
        # draw stats
        text_info_fps = self.game_font_small.render('FPS: ' + str(int(actual_fps)),
                                                    False, parameters.GAME_STATS_COLOR)
        text_info_score = self.game_font_small.render('SCORE: ' + '{:0>8}'.format(str(game_score)),
                                                      False, parameters.GAME_STATS_COLOR)
        text_info_lives = self.game_font_small.render('COINS: ' + '{:0>2}'.format(str(game_lives)),
                                                      False, parameters.GAME_STATS_COLOR)
        self.screen.blit(text_info_fps, self.TEXT_FPS_POS)
        self.screen.blit(text_info_score, self.TEXT_SCORE_POS)
        self.screen.blit(text_info_lives, self.TEXT_LIVES_POS)

    def game_restarts(self):
        if self.next_game_countdown > 0:
            if self.next_game_countdown == parameters.GAME_RESTARTS_IN:
                self.text_info_countdown = self.game_font_extra.render("READY", False,
                                                                       parameters.GAME_RESTART_COLOR)
                self.sound_ready.play()
            if self.next_game_countdown == int(parameters.GAME_RESTARTS_IN / 3) * 2:
                self.text_info_countdown = self.game_font_extra.render("STEADY", False,
                                                                       parameters.GAME_RESTART_COLOR)
                self.sound_steady.play()
            if self.next_game_countdown == int(parameters.GAME_RESTARTS_IN / 3) * 1:
                self.text_info_countdown = self.game_font_extra.render("GO", False,
                                                                       parameters.GAME_RESTART_COLOR)
                self.sound_go.play()
            self.next_game_countdown -= 1
            self.TEXT_LEVEL_RESTARTS_POS = [int((screen - banner) / 2) for screen, banner in
                                            zip(parameters.SCREEN_SIZE,
                                                self.text_info_countdown.get_rect().bottomright)]
            alpha = int((self.next_game_countdown / parameters.GAME_RESTARTS_IN) * 254)
            self.text_info_countdown.set_alpha(alpha)
            self.screen.blit(self.text_info_countdown, self.TEXT_LEVEL_RESTARTS_POS)
            return False
        else:
            self.next_game_countdown = parameters.GAME_RESTARTS_IN
            return True

    def game_your_score(self, game_score):
        self.text_info_final_score = self.game_font_large.render('{:0>8}'.format(str(game_score)),
                                                                 False, parameters.GAME_RESTART_COLOR)
        self.text_info_final_score.set_alpha(parameters.FINAL_SCORE_TEXT_ALPHA)
        self.screen.blit(self.text_info_final_score, self.TEXT_LEVEL_FINAL_SCORE_POS)
