#Declare all constant variable using in this project |
#----------------------------------------------------/
import pygame

# Game Display Window
s_display_W = 820 #(20+600+200)
s_display_H = 640 #(20+600+20)
s_display_caption  = r'Wumpus the game'
s_display_iconpath = r''
s_display_font = r'assets/font/MinecraftRegular-Bmg3.otf' #r'assets/font/Product_Sans_Regular.otf'
s_display_fps = 30

# Game state
s_state_home = 'HOME'
s_state_algo = 'ALGO'
s_state_game = 'PLAY'
s_state_about = 'ABOUT'
s_state_end  = 'END'

# Stage
s_display_menu = r'assets/stage/menu.png'
s_display_game = r'assets/stage/game.png'
s_display_end  = r'assets/stage/endgame.png'
s_display_about = r'assets/stage/about.png'

# Map
s_map_list = [r'assets/map_txt/map_1.txt', r'assets/map_txt/map_2.txt', r'assets/map_txt/map_3.txt', r'assets/map_txt/map_4.txt', r'assets/map_txt/map_5.txt']
s_out_list = [r'output/out_1.txt', r'output/out_2.txt', r'output/out_3.txt', r'output/out_4.txt', r'output/out_5.txt']

# Map elements
s_map_ele_unexplored = r'assets/map_elements/init.png'
s_map_ele_explored   = r'assets/map_elements/Explored.png'
s_map_ele_gold       = r'assets/map_elements/gold.png'
s_map_ele_pit        = r'assets/map_elements/pit.png'
s_map_ele_wumpus     = r'assets/map_elements/wumpus.png'

s_agent_up    = r'assets/map_elements/hunter_up.png'
s_agent_down  = r'assets/map_elements/hunter_down.png'
s_agent_left  = r'assets/map_elements/hunter_left.png'
s_agent_right = r'assets/map_elements/hunter_right.png'

s_agent_direction_up    = 0
s_agent_direction_down  = 1
s_agent_direction_left  = 2
s_agent_direction_right = 3

s_agent_arrow_up    = r'assets/map_elements/arrow_up.png'
s_agent_arrow_down  = r'assets/map_elements/arrow_down.png'
s_agent_arrow_left  = r'assets/map_elements/arrow_left.png'
s_agent_arrow_right = r'assets/map_elements/arrow_right.png'

#[Gold, Pit, Wumpus, Breeze, Stench]
s_map_ele_exploredList = {'[True, False, False, False, False]':r'assets/map_elements/Explored/Explored-.G._._.png',
                          '[True, False, False, True, False]':r'assets/map_elements/Explored/Explored-.G.B._.png',
                          '[True, False, False, False, True]':r'assets/map_elements/Explored/Explored-.G._.S.png',
                          '[True, False, False, True, True]':r'assets/map_elements/Explored/Explored-.G.B.S.png',
                          '[False, False, False, True, False]':r'assets/map_elements/Explored/Explored-._.B._.png',
                          '[False, False, False, False, True]':r'assets/map_elements/Explored/Explored-._._.S.png',
                          '[False, False, False, True, True]':r'assets/map_elements/Explored/Explored-._.B.S.png',
                          '[False, False, False, False, False]':r'assets/map_elements/Explored.png',
                          '[False, True, False, False, False]':r'assets/map_elements/pit.png',
                          '[False, False, True, False, False]':r'assets/map_elements/wumpus.png',
                          '[True, False, True, False, False]':r'assets/map_elements/Explored/Explored-.G._._.W.png',
                          '[True, False, True, True, False]':r'assets/map_elements/Explored/Explored-.G.B._.W.png',
                          '[True, False, True, False, True]':r'assets/map_elements/Explored/Explored-.G._.S.W.png',
                          '[True, False, True, True, True]':r'assets/map_elements/Explored/Explored-.G.B.S.W.png',
                          '[False, False, True, True, False]':r'assets/map_elements/Explored/Explored-._.B._.W.png',
                          '[False, False, True, False, True]':r'assets/map_elements/Explored/Explored-._._.S.W.png',
                          '[False, False, True, True, True]':r'assets/map_elements/Explored/Explored-._.B.S.W.png'}

# Color
s_color_black = (0, 0, 0)
s_color_white = (255, 255, 255)
s_color_coral = (190, 179, 177)
s_color_dgray = (130, 124, 124)
s_color_red   = (234, 23, 21)

#Button (left, top, width, height)
    #Menu_map
s_button_map1 = pygame.Rect(260, 180, 300, 50)
s_button_map2 = pygame.Rect(260, 250, 300, 50)
s_button_map3 = pygame.Rect(260, 320, 300, 50)
s_button_map4 = pygame.Rect(260, 390, 300, 50)
s_button_map5 = pygame.Rect(260, 460, 300, 50)
s_button_crea = pygame.Rect(260, 530, 140, 50)
s_button_exit = pygame.Rect(420, 530, 140, 50)

#MAP
s_map_pos = (20, 20)

#Entities
s_entities_gold = 'GOLD'
s_entities_pit  = 'PIT'
s_entities_wum  = 'WUMPUS'
s_entities_bre  = 'BREEZE'
s_entities_ste  = 'STENCH'
s_entities_list = [s_entities_gold[0], s_entities_pit[0], s_entities_wum[0], s_entities_bre[0], s_entities_ste[0]]

#Action
s_action_fall  = 'Fall into Pit'
s_action_eaten = 'Eaten by Wumpus'
s_action_grab  = 'Grab Gold'
s_action_breeze = 'Perceive Breeze'
s_action_stench = 'Perceive Stench'
s_action_up    = 'Turn Up'
s_action_down  = 'Turn Down'
s_action_left  = 'Turn Left'
s_action_right = 'Turn Right'
s_action_move  = 'Move Foward'
s_action_shoot = 'Shoot Arrow'
s_action_kill  = 'Kill Wumpus'
s_action_nkill = 'Kill Nothing'
s_action_de_wumpus  = 'Detect Wumpus'
s_action_de_nwumpus = 'Detect no Wumpus'
s_action_de_pit     = 'Detect Pit'
s_action_de_npit    = 'Detect no Pit'
s_action_infer_safe    = "Inference Safe"
s_action_infer_nsafe   = "Inference not Safe"
s_action_infer_wumpus  = "Inference Wumpus"
s_action_infer_nwumpus = "Inference not Wumpus"
s_action_infer_pit     = "Inference Pit"
s_action_infer_npit    = "Inference not Pit"

s_action_climb   = 'Climb Out'
s_action_victory = 'Victory'
