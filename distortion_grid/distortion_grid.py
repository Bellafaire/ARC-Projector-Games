#!/usr/bin/python3

# Simple pygame program
# Import and initialize the pygame library

import pygame
import random
import numpy as np
import sys
from location_parser import LocationParser
           
# POSITION_FILE_LOCATION = "/home/matthew/ros_ws/src/lidar-people-detect/makers_people_detection/lidar_output.txt"
POSITION_FILE_LOCATION = "/home/matthew/Documents/ARC-Projector-Games/lidar_output.txt"
lidar_positioner = LocationParser(POSITION_FILE_LOCATION, 3, 2, 1920, 1080)

pygame.init()

# Set up the drawing window
# screen = pygame.display.set_mode([1920, 1080])

#render resolution, this will be scaled to the screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1920 , 1080 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)

running = True
clock = pygame.time.Clock()

class ResponsivePoint(): 
    def __init__(self, x, y): 
        self.x = x
        self.y = y

        self.xd = x
        self.yd = y

    def draw(self, screen, distortions): 
        c = pygame.Color(255,255,255)
        # pygame.draw.line(screen,c, (self.x, 0), (self.x, SCREEN_HEIGHT), 5)
        
        #for now just take the first distortion point
        #calc distance
        force = 0
        direction_vector = [0,0]
        for a in distortions: 
            force = 1/np.sqrt((a[0] - self.x) ** 2 + (a[1] - self.y) ** 2)
            # direction_vector += np.array([(distortions_x[0] - self.x), (distortions_y[0] - self.y)]) * force 
            direction_vector[0] += (a[0] - self.x) * force
            direction_vector[1] += (a[1] - self.y) * force

        self.xd = self.x -  100*direction_vector[0]
        self.yd = self.y -  100*direction_vector[1]

        pygame.draw.circle(screen, c, (self.xd, self.yd), 5)    

class ResponsiveGrid(): 
    def __init__(self, rows, columns, draw_lines=False):
        self.rows = rows
        self.columns = columns
        self.draw_lines = draw_lines

        self.points = []

        for r in range(rows): 
            for c in range(columns):
                self.points.append(ResponsivePoint(c * (SCREEN_WIDTH / self.columns) + (SCREEN_WIDTH / self.columns) * 0.5, r * (SCREEN_HEIGHT / self.rows) + (SCREEN_HEIGHT / self.rows) * 0.5))

    def draw(self, screen, distortions): 
        for a in self.points: 
            a.draw(screen, distortions)

        if(self.draw_lines):
            for index, element in enumerate(self.points): 
                #connect line to the left dot, and the above dot 
                
                left_index = index - 1
                above_index = index - self.columns

                if(left_index > 0 and above_index > 0 and index % self.columns > 0 ): 
                    pygame.draw.line(screen, (255,255,255), (element.xd, element.yd), (self.points[left_index].xd, self.points[left_index].yd), 1)
                    pygame.draw.line(screen, (255,255,255), (element.xd, element.yd), (self.points[above_index].xd, self.points[above_index].yd), 1)
        

TOTAL_ROWS = 2 * 9 
TOTAL_COLUMNS = 2 * 16

grid = ResponsiveGrid(TOTAL_ROWS, TOTAL_COLUMNS, draw_lines=True)

screen.fill((255,255,255))

while running:


    # Did the user click the window close button?

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


    # Fill the background with white

    screen.fill((0,0,0, 1))

    positions = lidar_positioner.getPositions()
    for xy in positions: 
        pygame.draw.circle(screen, (0,0,255), xy, 10)  
    grid.draw(screen, positions)

    # Flip the display
    pygame.display.flip()

    # pygame.display.flip()
    clock.tick(120)


# Done! Time to quit.

pygame.quit()
sys.exit()
