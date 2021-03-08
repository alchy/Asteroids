import pygame
import parameters


class Banners:
    def __init__(self, screen):
        self.screen = screen

        # init game fonts
        self.game_font_small = pygame.font.Font('fonts/supercomputer.ttf', 20)
        self.game_font_large = pygame.font.Font('fonts/supercomputer.ttf', 40)

        # init "GAME RESTARTS IN: ..."
        self.next_game_countdown = parameters.GAME_RESTARTS_IN
        self.text_info_countdown = self.game_font_large.render("LEVEL RESTARTS IN 4", False, \
                                                               parameters.GAME_RESTART_COLOR)
        self.LEVEL_RESTARTS = self.text_info_countdown.get_rect().bottomright
        self.LEVEL_RESTARTS_POS = [int((screen - banner) / 2) for screen, banner in
                                   zip(parameters.SCREEN_SIZE, self.LEVEL_RESTARTS)]

    def game_stats(self, actual_fps, game_score, game_lives):
        # draw stats
        text_info_fps = self.game_font_small.render('FPS: ' + str(int((actual_fps))), \
                                                    False, parameters.GAME_STATS_COLOR)
        text_info_score = self.game_font_small.render('SCORE: ' + '{:0>5}'.format(str(game_score)), \
                                                      False, parameters.GAME_STATS_COLOR)
        text_info_lives = self.game_font_small.render('LIVES: ' + '{:0>2}'.format(str(game_lives)), \
                                                      False, parameters.GAME_STATS_COLOR)
        self.screen.blit(text_info_fps, (8, 8))
        self.screen.blit(text_info_score, (350, 8))
        self.screen.blit(text_info_lives, (712, 8))

    def game_restarts(self):
        if self.next_game_countdown > 0:
            if self.next_game_countdown == parameters.GAME_RESTARTS_IN:
                self.text_info_countdown = self.game_font_large.render("LEVEL RESTARTS IN 4", False,
                                                                       parameters.GAME_RESTART_COLOR)
            if self.next_game_countdown == int(parameters.GAME_RESTARTS_IN / 4) * 3:
                self.text_info_countdown = self.game_font_large.render("LEVEL RESTARTs IN 3", False,
                                                                       parameters.GAME_RESTART_COLOR)
            if self.next_game_countdown == int(parameters.GAME_RESTARTS_IN / 4) * 2:
                self.text_info_countdown = self.game_font_large.render("LEVEL RESTARTs IN 2", False,
                                                                       parameters.GAME_RESTART_COLOR)
            if self.next_game_countdown == int(parameters.GAME_RESTARTS_IN / 4) * 1:
                self.text_info_countdown = self.game_font_large.render("LEVEL RESTARTS IN 1", False,
                                                                       parameters.GAME_RESTART_COLOR)
            self.next_game_countdown -= 1
            self.screen.blit(self.text_info_countdown, self.LEVEL_RESTARTS_POS)
            return False
        else:
            self.next_game_countdown = parameters.GAME_RESTARTS_IN
            return True
