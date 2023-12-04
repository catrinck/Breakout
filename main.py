import pygame
from pygame.cursors import *
from pygame.locals import Rect
from pygame.locals import *
import sys
import math
import random

pygame.init()

#screen
screen_width = 600
screen_height = 700

#define colors
BG = (0, 0, 0)
BLOCK_RED = (255, 0, 0)
BLOCK_GREEN = (0, 255, 0)
BLOCK_ORANGE = (255 * 65536 + 165 * 256 + 0)
BLOCK_YELLOW = (255, 255, 0)
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
pallet_size = 15
pallet_width = 100
paddle_outline = (100, 100, 100)

# sound effects
bounce_sound_effect = pygame.mixer.Sound('assets/bounce.wav')

class PADDLE:
    direction = None

    def __init__(self, x, y, width, height, VELOCIDADE = 10):
        self.VELOCIDADE = 10
        self.width = width
        self.height = height
        self.speed = VELOCIDADE
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = (screen_width - self.width) // 2
        self.y = screen_height - self.height - 10
        self.direction = 0
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def move (self):
        self.direction = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.x -= self.VELOCIDADE
            self.direction = -1
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.x += self.VELOCIDADE
            self.direction = 1
        self.rect.x = self.x

    def reset(self):
        self.rect.width = pallet_width
        self.rect.x = (screen_width - pallet_width) // 2
        self.rect.y = screen_height - self.rect.height - 10

    def draw(self):
        pygame.draw.rect(screen, PADDLE_COLOR, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)


radius = 10
class BALL:
    max_speed = 7 # to decide
    ball_color = (255, 255, 255)

    def __init__(self, x, y, radius):
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.speed_x = self.max_speed
        self.speed_y = - self.max_speed
        self.game_over = 0

    def move(self):
        # Update ball position based on speed
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x
        self.rect.y = self.y

        collision_thresh = 5

        # check collision with paddle
        if self.rect.colliderect(player):
            if self.speed_y > 0:  # only if the balls falling
                self.speed_y *= -1
            if abs(self.rect.bottom - player.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x *= player.direction
                relative_collision_point = (self.rect.centerx - player.rect.x) / player.rect.width
                reflection_angle = (relative_collision_point - 0.5) * 3 * (math.pi / 4)

                # Add randomness to the reflection angle:
                random_factor = random.uniform(-math.pi / 8, math.pi / 8)
                reflection_angle += random_factor

                # Update ball velocities based on reflection angle
                self.speed_x = self.max_speed * -math.cos(reflection_angle)
                self.speed_y = -self.max_speed * math.sin(reflection_angle)

        # Check collision with blocks
        for row in range(rows):
            for col in range(cols):
                block = wall.blocks[row][col][0]
                if block.colliderect(self.rect):
                    # Collision with a block
                    # Do whatever is necessary upon colliding with a block
                    wall.blocks[row][col][1] = 0 # Reduce the strength of the block, or use other logic
                    wall.blocks[row][col][0] = pygame.Rect(0, 0, 0, 0)  # "Remove" the block
                    bounce_sound_effect.play()

                    # Update ball velocities (example: invert)
                    self.speed_x *= -1
                    self.speed_y *= -1
                    bounce_sound_effect.play()

        # Check collision with walls and update velocities
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1
            bounce_sound_effect.play()

        # Check collision with top
        if self.rect.top < 0 :
            self.speed_y *= -1
            bounce_sound_effect.play()


        # Return the game over state
        return self.game_over


    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.speed_y = -self.max_speed
        self.speed_x = random.choice([6, -6])

    def draw(self):
        pygame.draw.circle(screen, PADDLE_COLOR, (self.rect.x + self.radius, self.rect.y + self.radius),
                           self.radius)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.radius, self.rect.y + self.radius),
                           self.radius, 3)

class BLOCK:
    def __init__(self):
        self.game_over = 0
        self.live_ball = False
        self.blocks = None
        self.width = screen_width // cols
        self.height = 20

#create the wall of blocks
    def create_wall(self):
        self.blocks = []
        # empty list fot individual blocks
        block_individual = []
        for row in range(rows):
            # reset the block row list
            block_row = []
            # iterate through each column in that row
            for col in range(cols):
                # generate x and y positions for each block and create a rectangle from that
                block_x = col * self.width
                block_y = row * self.height + 70
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
                    block_col = BLOCK_RED
                elif block[1] == 3:
                    block_col = BLOCK_ORANGE
                elif block[1] == 2:
                    block_col = BLOCK_GREEN
                elif block[1] == 1:
                    block_col = BLOCK_YELLOW
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, BG, (block[0]), 2)


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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if game_over == -1:
                    player.reset()
        elif event.type == KEYUP:
            if game_over == - 1:
                if event.key == K_r:
                    player.reset()
                    game_over = 0
                    ball.reset()


        if event.type == pygame.MOUSEBUTTONDOWN :
          live_ball = True
          ball.reset()
          player.reset()
          wall.create_wall()

    if live_ball:
        # draw paddle
        player.move()
        #player.draw()
        # draw ball
        game_over = ball.move()
        ball.draw()

        if ball.rect.bottom > screen_height:
            live_ball = False
            game_over = -1

    if not live_ball:
        if game_over == -1:
            player.rect.width = screen_width
            player.rect.x = 0
            player.rect.y = screen_height - player.height - 10
            player.draw()
    pygame.display.update()
pygame.display.flip()
pygame.quit()
