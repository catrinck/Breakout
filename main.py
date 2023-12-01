import pygame
from pygame.cursors import *
from pygame.locals import Rect

#import random

pygame.init()

#screen
screen_width = 800
screen_height = 600

#define font
font = pygame.font.SysFont('Constantia', 36)

#define colors
BG = (0, 0, 0)
BLOCK_RED = (255, 0, 0)
BLOCK_GREEN = (0, 255, 0)
BLOCK_ORANGE = (255 * 65536 + 165 * 256 + 0)
BLOCK_YELLOW = (255, 255, 0)
TEXT_COLOR = (78, 81, 139)
PADDLE_COLOR = (142, 135, 123)
block_col = None

# creating screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

#variables
clock = pygame.time.Clock()
FPS = 60
cols = 12
rows = 8
pallet_size = 10
pallet_width = 100
paddle_outline = (100, 100, 100)


class PADDLE:
    direction = None
    # player_draw = pygame.Rect(screen_width - 20, screen_height / 2, PADDLE_COLOR, pallet_width, pallet_size)

    def __init__(self, x, y, width, height, VELOCIDADE = 8):
        self.VELOCIDADE = 8
        self.width = width
        self.height = height
        self.speed = VELOCIDADE
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = (screen_width - self.width) // 2
        self.y = screen_height - self.height - 10
        self.direction = 0
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def move (self, up = True):
        if up :
            self.y -= self.VELOCIDADE
        else :
            self.y += self.VELOCIDADE
        self.rect.y = self.y

    def reset(self):
        self.x = screen_width // 2 - self.width // 2
        #  self.height = 20
     #   self.width = int(screen_width / cols)
        #self.x = screen_width //2 - self.width // 2
        #self.y = self.original_y


    def draw(self):
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)


radius = 10
class BALL:
    max_speed = 10 # to decide
    ball_color = (255, 255, 255)
    #ball_size = 30
    #ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, ball_size, ball_size)

    def __init__(self, x, y, radius):
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.speed_y = None
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.speed_x = self.max_speed

    def move(self):

        # collision
        collision_thresh = 5

        # the wall has to be completely destroyed
        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                # check collision
                if self.rect.colliderect(item[0]):
                    # check if collision was from above
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    # check if collision was from below
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    # check if collision was from left
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                    # check if collision was from right
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                    # reduce the block's strength by doing damage to it
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)

                # check if block still exists, in whcih case the wall is not destroyed
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                # increase item counter
                item_count += 1
            # increase row counter
            row_count += 1
        # after iterating through all the blocks, check if the wall is destroyed
        if wall_destroyed == 1:
            self.game_over = 1

        # check for collision with walls
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

        # check for collision with top and bottom of the screen
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1

        # look for collission with paddle
        if self.rect.colliderect(player):
            # check if colliding from the top
            if abs(self.rect.bottom - player.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player.direction
                if self.speed_x > self.max_speed:
                    self.speed_x = self.max_speed
                elif self.speed_x < 0 and self.speed_x < -self.max_speed:
                    self.speed_x = -self.max_speed
            else:
                self.speed_x *= -1

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.speed_y = 0
        self.speed_x *= -1

    def draw(self):
        pygame.draw.circle(screen, PADDLE_COLOR, (self.rect.x + self.radius, self.rect.y + self.radius),
                           self.radius)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.radius, self.rect.y + self.radius),
                           self.radius, 3)

# criar funcao pra randomizar a bola

# block cria classe para blocos
class BLOCK:
    def __init__(self):
        self.game_over = 0
        self.live_ball = False
        self.blocks = None
        self.width = screen_width // cols
        self.height = 30

#create the wall of blocks
    def create_wall(self):
        self.blocks = []
        # lista vazia para blocos individuais
        block_individual = []
        for row in range(rows):
            # reset the block row list
            block_row = []
            # iterate through each column in that row
            for col in range(cols):
                # generate x and y positions for each block and create a rectangle from that
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                # assign block strength based on row
                if row < 2:
                    strength = 4
                elif row < 4:
                    strength = 3
                elif row < 6:
                    strength = 2
                elif row < 8:
                    strength = 1
                # create a list at this point to store the rect and colour data
                block_individual = [rect, strength]
                # append that individual block to the block row
                block_row.append(block_individual)
            # append the row to the full list of blocks
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                # assign a colour based on block strength
                if block[1] == 4:
                    block_col = BLOCK_YELLOW
                elif block[1] == 3:
                    block_col = BLOCK_GREEN
                elif block[1] == 2:
                    block_col = BLOCK_ORANGE
                elif block[1] == 1:
                    block_col = BLOCK_RED
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, BG, (block[0]), 2)



# function for outputting text onto the screen
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

wall = BLOCK()
wall.create_wall()
player = PADDLE(screen_width - 20, screen_height / 2, pallet_width, pallet_size, VELOCIDADE= 8)
ball = BALL(screen_width / 2, screen_height / 2, radius)
game_over = 0
live_ball = False
run = True

#game loop
while run:

    clock.tick(FPS)
    screen.fill(BG)

    #DRAW THINGS

    wall.draw_wall()
    player.draw()
    ball.draw()

    if live_ball:
        # draw paddle
        player.move()
        # draw ball
        game_over = ball.move()
        if game_over != 0:
            live_ball = False

        # print player instructions
        if not live_ball:
            ball.reset()
            player.reset()
            if game_over == 0:
                draw_text('CLICK ANYWHERE TO START', font, TEXT_COLOR, 100, screen_height // 2 + 100)
            elif game_over == 1:
                draw_text('YOU WON!', font, TEXT_COLOR, 240, screen_height // 2 + 50)
                draw_text('CLICK ANYWHERE TO START', font, TEXT_COLOR, 100, screen_height // 2 + 100)
            elif game_over == -1:
                draw_text('YOU LOST!', font, TEXT_COLOR, 240, screen_height // 2 + 50)
                draw_text('CLICK ANYWHERE TO START', font, TEXT_COLOR, 100, screen_height // 2 + 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
                live_ball = True
                ball.reset(player.x + (player.screen_width // 2), player.y - player.height)
                player.reset()
                wall.create_wall()

        pygame.display.update()

    pygame.display.flip()

pygame.quit()
