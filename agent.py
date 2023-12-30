from constant import *
import pygame

class Agent(pygame.sprite.Sprite):
    def __init__(self, initPos):
        pygame.sprite.Sprite.__init__(self)
        #Graphic
        self.image = pygame.image.load(s_agent_right)
        self.imageList = [pygame.image.load(s_agent_up), pygame.image.load(s_agent_down), pygame.image.load(s_agent_left), self.image]
                         #0-Up, 1-Down, 2-Left, 3-Right
        self.arrow = [pygame.image.load(s_agent_arrow_up), pygame.image.load(s_agent_arrow_down), pygame.image.load(s_agent_arrow_left), pygame.image.load(s_agent_arrow_right)]
        #Control
        self.position = initPos
        self.facing = s_agent_direction_right #[0-up, 1-down, 2-left, 3-right]

    def graphicPos(self, pos):
        #x = 20 + 60 * col_pos , y = 20 + 60 * row_pos
        return (20 + 60 * pos[1], 20 + 60 * pos[0])

    #Call Agent to appear
    def agent_appear(self, screen):
        screen.blit(self.image, self.graphicPos(self.position))
        pygame.display.update()

    #CONTROL ===========================================================================================================
    def turn(self, screen, direction):
        #direction = [0-up, 1-down, 2-left, 3-right]
        self.facing = direction
        self.image  = self.imageList[direction]
        self.agent_appear(screen)

    def move(self, screen, direction):
        #đây là di chuyển theo góc nhìn người xem, không phải agent
        if direction == s_agent_direction_up:
            self.position = (self.position[0] - 1, self.position[1])
        elif direction == s_agent_direction_down:
            self.position = (self.position[0] + 1, self.position[1])
        elif direction == s_agent_direction_left:
            self.position = (self.position[0], self.position[1] - 1)
        elif direction == s_agent_direction_right:
            self.position = (self.position[0], self.position[1] + 1)
        self.agent_appear(screen)

    def shoot(self, screen, shoot_pos):
        arrow_image = None
        direction   = 0
        if self.position[0] == shoot_pos[0]: #Shoot LEFT/RIGHT
            if self.position[1] + 1 == shoot_pos[1]: #Right
                arrow_image = self.arrow[s_agent_direction_right]
                direction = s_agent_direction_right
            else: #Left
                arrow_image = self.arrow[s_agent_direction_left]
                direction = s_agent_direction_left
        elif self.position[1] == shoot_pos[1]: #Turn UP/DOWN
            if self.position[0] + 1 == shoot_pos[0]: #Down
                arrow_image = self.arrow[s_agent_direction_down]
                direction = s_agent_direction_down
            else: #Up
                arrow_image = self.arrow[s_agent_direction_up]
                direction = s_agent_direction_up
        #Show
        screen.blit(arrow_image, self.graphicPos(shoot_pos))
        pygame.display.update()
        return direction