import sys
import os
import pygame
import pygame.freetype

from constant import *
import readmap as Map
import agent as Agent
import propositionalLogic as prop

class wumpus_game:
    #Init
    def __init__(self):
        pygame.init()
        pygame.font.init()

        #GRAPHIC -------------------------------------------------------------------------------------------------------
        # Window Frame
        self.screen  = pygame.display.set_mode((s_display_W, s_display_H))
        self.caption = pygame.display.set_caption(s_display_caption, s_display_iconpath)
        # Font
        self.font = pygame.font.Font(s_display_font, 20)
        self.font_big = pygame.font.Font(s_display_font, 120)
        # Load Stage
        self.menu_about= pygame.image.load(s_display_about)
        self.menu_map  = pygame.image.load(s_display_menu)
        self.menu_algo = pygame.image.load(s_display_menu)
        self.game_play = pygame.image.load(s_display_game)
        self.game_end  = pygame.image.load(s_display_end)

        # Stage, Mouse and FPS Control
        self.stage = s_state_home
        self.clock = pygame.time.Clock()
        self.mouse = None

        #Map
        self.map_index = 0
        self.map = s_map_list[self.map_index]

        #Algorithm
        self.algo_pick = 0

        #Game logic
        self.score = 0

    #Button
    def drawButton(self, surf, rect, button_color, text_color, text):
        pygame.draw.rect(surf, button_color, rect)
        text_surf = self.font.render(text, True, text_color)
        text_rect = text_surf.get_rect()
        text_rect.center = rect.center
        self.screen.blit(text_surf, text_rect)

    # RUN THE GAME -----------------------------------------------------------------------------------------------------
    def run(self):
        while True:
            if self.stage == s_state_home:
                #Set default
                self.score = 0
                self.map_index = 0
                self.algo_pick = 0
                #Load and display
                self.stageHome_display()
                self.stageHome_getAction()
            elif self.stage == s_state_about:
                self.stageAbout_display()
                self.stageAbout_action()
            elif self.stage == s_state_algo:
                #Load and display
                self.stageAlgo_display()
                self.stageAlgo_getAction()
            elif self.stage == s_state_game:
                #Load and display
                self.stageGame_display()
                #Run game
                if self.algo_pick == 0:
                    self.propositionalLogic_BW()
                elif self.algo_pick == 1:
                    self.propositionalLogic_RE()
                #
            elif self.stage == s_state_end:
                self.stageEnd_display()
                self.stageEnd_action()

            self.clock.tick(s_display_fps)

    # ABOUT ============================================================================================================
    def stageAbout_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.menu_about, (0, 0))

    def stageAbout_action(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 260 <= self.mouse[0] <= 560 and 460 <= self.mouse[1] <= 510:
                    self.stage = s_state_home
            # Quit game :<
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.mouse = pygame.mouse.get_pos()
            if 260 <= self.mouse[0] <= 560 and 460 <= self.mouse[1] <= 510:
                self.drawButton(self.screen, s_button_map5, s_color_dgray, s_color_white, 'Back')
            else:
                self.drawButton(self.screen, s_button_map5, s_color_coral, s_color_white, 'Back')
            pygame.display.update()

    # Home Stage============================| PICK MAP
    def stageHome_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.menu_map, (0, 0))
        #pygame.display.update()

    def stageHome_getAction(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 260 <= self.mouse[0] <= 560 and 180 <= self.mouse[1] <= 230:
                    self.stage = s_state_algo
                    self.map_index = 1 - 1
                elif 260 <= self.mouse[0] <= 560 and 250 <= self.mouse[1] <= 300:
                    self.stage = s_state_algo
                    self.map_index = 2 - 1
                elif 260 <= self.mouse[0] <= 560 and 320 <= self.mouse[1] <= 370:
                    self.stage = s_state_algo
                    self.map_index = 3 - 1
                elif 260 <= self.mouse[0] <= 560 and 390 <= self.mouse[1] <= 440:
                    self.stage = s_state_algo
                    self.map_index = 4 - 1
                elif 260 <= self.mouse[0] <= 560 and 460 <= self.mouse[1] <= 510:
                    self.stage = s_state_algo
                    self.map_index = 5 - 1
                elif 260 <= self.mouse[0] <= 400 and 530 <= self.mouse[1] <= 580:
                    self.stage = s_state_about
                elif 420 <= self.mouse[0] <= 560 and 530 <= self.mouse[1] <= 580:
                    pygame.quit()
                    sys.exit()
            # Quit game :<
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.mouse = pygame.mouse.get_pos()
            if 260 <= self.mouse[0] <= 560 and 180 <= self.mouse[1] <= 230:
                self.drawButton(self.screen, s_button_map1, s_color_dgray, s_color_white, 'Map 1')
            else:
                self.drawButton(self.screen, s_button_map1, s_color_coral, s_color_white, 'Map 1')
            if 260 <= self.mouse[0] <= 560 and 250 <= self.mouse[1] <= 300:
                self.drawButton(self.screen, s_button_map2, s_color_dgray, s_color_white, 'Map 2')
            else:
                self.drawButton(self.screen, s_button_map2, s_color_coral, s_color_white, 'Map 2')
            if 260 <= self.mouse[0] <= 560 and 320 <= self.mouse[1] <= 370:
                self.drawButton(self.screen, s_button_map3, s_color_dgray, s_color_white, 'Map 3')
            else:
                self.drawButton(self.screen, s_button_map3, s_color_coral, s_color_white, 'Map 3')
            if 260 <= self.mouse[0] <= 560 and 390 <= self.mouse[1] <= 440:
                self.drawButton(self.screen, s_button_map4, s_color_dgray, s_color_white, 'Map 4')
            else:
                self.drawButton(self.screen, s_button_map4, s_color_coral, s_color_white, 'Map 4')
            if 260 <= self.mouse[0] <= 560 and 460 <= self.mouse[1] <= 510:
                self.drawButton(self.screen, s_button_map5, s_color_dgray, s_color_white, 'Map 5')
            else:
                self.drawButton(self.screen, s_button_map5, s_color_coral, s_color_white, 'Map 5')
            #
            if 260 <= self.mouse[0] <= 400 and 530 <= self.mouse[1] <= 580:
                self.drawButton(self.screen, s_button_crea, s_color_dgray, s_color_white, 'About')
            else:
                self.drawButton(self.screen, s_button_crea, s_color_coral, s_color_white, 'About')
            if 420 <= self.mouse[0] <= 560 and 530 <= self.mouse[1] <= 580:
                self.drawButton(self.screen, s_button_exit, s_color_dgray, s_color_red, 'Exit')
            else:
                self.drawButton(self.screen, s_button_exit, s_color_coral, s_color_white, 'Exit')
            #
            pygame.display.update()

    # Algo Stage============================| PICK ALGORITHM
    def stageAlgo_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.menu_algo, (0, 0))

    def stageAlgo_getAction(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 260 <= self.mouse[0] <= 560 and 250 <= self.mouse[1] <= 300:
                    self.stage = s_state_game
                    self.algo_pick = 1 - 1
                    break
                elif 260 <= self.mouse[0] <= 560 and 320 <= self.mouse[1] <= 370:
                    self.stage = s_state_game
                    self.algo_pick = 2 - 1
                    break
                elif 260 <= self.mouse[0] <= 560 and 390 <= self.mouse[1] <= 440:
                    self.stage = s_state_home
            # Quit game :<
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.mouse = pygame.mouse.get_pos()
            if 260 <= self.mouse[0] <= 560 and 250 <= self.mouse[1] <= 300:
                self.drawButton(self.screen, s_button_map2, s_color_dgray, s_color_white, 'Propositional Logic (BW)')
            else:
                self.drawButton(self.screen, s_button_map2, s_color_coral, s_color_white, 'Propositional Logic (BW)')
            if 260 <= self.mouse[0] <= 560 and 320 <= self.mouse[1] <= 370:
                self.drawButton(self.screen, s_button_map3, s_color_dgray, s_color_white, 'Propositional Logic (Re)')
            else:
                self.drawButton(self.screen, s_button_map3, s_color_coral, s_color_white, 'Propositional Logic (Re)')
            if 260 <= self.mouse[0] <= 560 and 390 <= self.mouse[1] <= 440:
                self.drawButton(self.screen, s_button_map4, s_color_dgray, s_color_white, 'Back')
            else:
                self.drawButton(self.screen, s_button_map4, s_color_coral, s_color_white, 'Back')
            pygame.display.update()

    # Game play=============================| PLAY GAME
    def stageGame_display(self):
        self.screen.fill(s_color_black)
        self.screen.blit(self.game_play, (0, 0))
        pygame.display.update()

    def stageGame_action(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 645 <= self.mouse[0] <= 795 and 574 <= self.mouse[1] <= 624:
                    self.stage = s_state_home
                    break
            # Quit game :<
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.mouse = pygame.mouse.get_pos()
            if 645 <= self.mouse[0] <= 795 and 574 <= self.mouse[1] <= 624:
                self.drawButton(self.screen, pygame.Rect(645, 574, 150, 50), s_color_dgray, s_color_white, 'Home')
            else:
                self.drawButton(self.screen, pygame.Rect(645, 574, 150, 50), s_color_coral, s_color_white, 'Home')
            pygame.display.update()

    #GAME ==============================================================================================================
    def propositionalLogic_BW(self):
        sys.setrecursionlimit(100000)
        #Read and Show map
        map = Map.Map()
        map.read_map(s_map_list[self.map_index])
        map.show_map1st(self.screen)
        #Agent
        agent = Agent.Agent(map.getInit_agent())
        agent.agent_appear(self.screen)
        #Run
        outfile = open(s_out_list[self.map_index], 'w')
        self.score = prop.Propositional_Logic(self, self.screen, map, agent, (9, 0), outfile).solving_BW()
        outfile.close()
        #
        self.stage = s_state_end

    def propositionalLogic_RE(self):
        sys.setrecursionlimit(100000)
        # Read and Show map
        map = Map.Map()
        map.read_map(s_map_list[self.map_index])
        map.show_map1st(self.screen)
        # Agent
        agent = Agent.Agent(map.getInit_agent())
        agent.agent_appear(self.screen)
        # Run
        outfile = open(s_out_list[self.map_index], 'w')
        self.score = prop.Propositional_Logic(self, self.screen, map, agent, (9, 0), outfile).solving_RE()
        outfile.close()
        #
        self.stage = s_state_end

    #END ===============================================================================================================
    def stageEnd_display(self):
        #Background
        self.screen.fill(s_color_black)
        self.screen.blit(self.game_end, (0, 0))
        #Score
        score_text = self.font_big.render(str(self.score), True, s_color_black)
        score_rect = score_text.get_rect(center=(s_display_W // 2, s_display_H // 2))
        self.screen.blit(score_text, score_rect)

    def stageEnd_action(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 260 <= self.mouse[0] <= 560 and 460 <= self.mouse[1] <= 510:
                    self.stage = s_state_home
            # Quit game :<
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            self.mouse = pygame.mouse.get_pos()
            if 260 <= self.mouse[0] <= 560 and 460 <= self.mouse[1] <= 510:
                self.drawButton(self.screen, s_button_map5, s_color_dgray, s_color_white, 'Back')
            else:
                self.drawButton(self.screen, s_button_map5, s_color_coral, s_color_white, 'Back')
            pygame.display.update()