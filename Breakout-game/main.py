import pygame
import random

pygame.init()

#screen
screen_width = 800
screen_height = 600

#define font
font = pygame.font.SysFont('Constantia', 36)

#define colors
background = (0, 0, 0)
block_red = (255, 0, 0)
block_green = (0, 255, 0)
block_orange = (255 * 65536 + 165 * 256 + 0)
block_yellow = (255, 255, 0)
paddle_color = (142, 135, 123)
text_color = (78, 81, 139)

# creating screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')

#variables
clock = pygame.time.Clock()
running = True
live_ball = True
cols = 12
rows = 8


class BALL:
    max_speed = 10 # to decide
    ball_color = (255, 255, 255)
    ball_size = 30
    ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, ball_size, ball_size)

# criar funcao de colisao da bola
# criar funcao de movimentaçao
# criar funcao pra randomizar a bola

# block criar classe para blocos
class BLOCK:
    def __init__(self):
        self.width = screen_width // cols
        self.height = 30

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
                    block_col = block_yellow
                elif block[1] == 3:
                    block_col = block_green
                elif block[1] == 2:
                    block_col = block_orange
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, background, (block[0]), 2)



# function for outputting text onto the screen
def draw_text(text, font, text_color, x, y):
	img = font.render(text, True, text_color)
	screen.blit(img, (x, y))








