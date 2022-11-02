# Simple pygame program


# Import and initialize the pygame library

import pygame
import random
import numpy as np
import sys

pygame.init()

# Set up the drawing window

# screen = pygame.display.set_mode([1920, 1080])

#render resolution, this will be scaled to the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1920 , 1080 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)



running = True
clock = pygame.time.Clock()

class line_object(): 
    def __init__(self, vel):
        self.x, self.y = SCREEN_WIDTH /2, SCREEN_HEIGHT /2
        self.velocity = vel
        self.hue = random.random() * 360
        self.theta = random.random() * 2*np.pi

    def move(self, draw_screen): 
        self.theta += random.random() - 0.5
        
        previous_x = self.x
        previous_y = self.y 

        self.x += self.velocity * np.cos(self.theta)
        self.y += self.velocity * np.sin(self.theta)
        
        if(self.x > SCREEN_WIDTH):
            self.x =  SCREEN_WIDTH
            self.theta -= np.pi
        elif self.x < 0: 
            self.x = 0
            self.theta += np.pi
        
        if(self.y > SCREEN_HEIGHT): 
            self.y = SCREEN_HEIGHT
            self.theta -= np.pi
        elif self.y < 0: 
            self.y = 0
            self.theta += np.pi
        
        
        self.hue += random.random() / 100
        c = pygame.Color(0)
        c.hsva = (self.hue % 360, 100, 100, 100)

        # print("previous xy (%0.2f, %0.2f) new xy (%0.2f, %0.2f)" % (previous_x, previous_y, self.x, self.y))

        pygame.draw.line(draw_screen,c, (previous_x, previous_y), (self.x, self.y), 5)
        pygame.draw.circle(draw_screen, c, (self.x, self.y), 5)

lines = []

for a in range(100): 
    lines.append(line_object(random.random() * 5 + 1))

screen.fill((255,255,255))

while running:


    # Did the user click the window close button?

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


    # Fill the background with white

    screen.fill((0,0,0, 1))
    for line in lines: 
        line.move(screen)


    # Draw a solid blue circle in the center


    # Flip the display
    pygame.display.flip()

    # pygame.display.flip()
    clock.tick(60)


# Done! Time to quit.

pygame.quit()
sys.exit()
