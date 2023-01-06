#!/usr/bin/env python3

import pygame
import random
import numpy as np
import sys
from location_parser import LocationParser

class SoccerBall(): 
    def __init__(self, max_velocity = 10,  radius=50, bounds=(0,0, 1920,1080), initial_position=(1920/2,1080/2), initial_velocitiy=None):
        """Soccer ball object that interacts with the players 

        Args:
            radius (int, optional): _description_. Defaults to 100.
            bounds (tuple, optional): bounds of where the ball can move on the playing field as tuple in form of (xmin, ymin, xmax, ymax). Defaults to (0,0, 1920,1080).
            initial_position (tuple, optional): initial position of the soccer ball on screen. Defaults to (1920/2,1080/2).
            initial_velocitiy (tuple, optional): intial velocity of the ball, if None the inital velocity of the ball will be randomly determined. Defaults to None.
        """
        
        self.bounds = bounds
        self.x = initial_position[0]
        self.y = initial_position[1]
        self.radius = radius
        self.max_velocity = max_velocity

        self.sprite = pygame.image.load("images/gear.png")
        self.sprite = pygame.transform.scale(self.sprite, (2*self.radius, 2*self.radius))
        self.sprite_size = self.sprite.get_rect()

        if(initial_velocitiy is None): 
            self.vx = random.random() * max_velocity
            self.vy = random.random() * max_velocity / 5
        else: 
            self.vx = initial_velocitiy[0]
            self.vy = initial_velocitiy[1]

        self.theta = 0
        self.radial_velocity = 0.1
    
    def move(self, players): 
        """Moves the soccer ball and interacts with player positions on the field

        Args:
            players (list Vector2d): Point positions of all the players who are currently detected on the field
        """

        #first just move the ball
        self.x += self.vx
        self.y += self.vy
        self.theta += self.radial_velocity

        #little bit of damping on the ball
        self.vx *= 1
        self.vy *= 1
        self.radial_velocity *= 0.99

        if (self.x < self.bounds[0] + self.radius):
            self.vx *= -1
            self.reset()
        elif (self.x > self.bounds[2] - self.radius):
            self.vx *= -1
            self.reset()

        if (self.y < self.bounds[1] + self.radius):
            self.vy = 1
        elif (self.y > self.bounds[3] - self.radius):
            self.vy = -1

        self.vx = self.constrain(self.vx, -self.max_velocity, self.max_velocity)
        self.vy = self.constrain(self.vy, -self.max_velocity, self.max_velocity)

        for a in players: 
            dist = self.calc_distance((self.x, self.y), a)
            if(dist < self.radius + 25): 
                magnitude = max(np.sqrt(self.vx**2 + self.vy**2), 0.1)

                diff = (a[0] - self.x, a[1] - self.y)  
                bounce_direction = np.arctan2(diff[1], diff[0])
                self.vx = self.max_velocity * np.cos(np.pi + bounce_direction)
                self.vy = self.max_velocity * np.sin(np.pi + bounce_direction)
                
                self.radial_velocity = random.random() * 20 - 10

    def reset(self): 
        self.x = (self.bounds[2] + self.bounds[0])/2
        self.y = (self.bounds[3] + self.bounds[1])/2
        self.vx = (random.random() - 0.5) * self.max_velocity 
        self.vy = (random.random() - 0.5) * self.max_velocity

    def calc_distance(self, p1, p2): 
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def constrain(self, val, lower, upper): 
        ret = val
        if val < lower: 
            ret = lower
        elif val > upper: 
            ret = upper 
        return ret

    def draw(self, screen): 
        # pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.radius, 5)
    
        rotated_sprite = pygame.transform.rotate(self.sprite, int(self.theta))
        pos = rotated_sprite.get_rect()
        pos.center = (self.x, self.y)
        screen.blit(rotated_sprite, pos)

class SoccerField: 
    def __init__(self, size=(1920, 1080), line_color=(255,255,255), field_color=(0,180,0)): 
        """Soccer field object to draw to the screen

        Args:
            size (tuple, optional): size (tuple, optional): resolution of the display. Defaults to (1920, 1080).. Defaults to (1920, 1080).
            line_color (tuple, optional): color of the lines on the field. Defaults to (255,255,255).
            field_color (tuple, optional): background fill color of the field. Defaults to (0,180,0).
        """


        self.size_x = size[0]
        self.size_y = size[1] 
        self.line_color = line_color
        self.field_color = field_color
        self.line_thickness = 5

        self.scores = [0,0]

        self.font = pygame.font.Font('freesansbold.ttf', 32)

    def draw(self, screen): 
        #screen.fill(self.field_color)
        pygame.draw.circle(screen, (255,255,255), (self.size_x/2, self.size_y/2), self.size_y/6, self.line_thickness)
        pygame.draw.line(screen, self.line_color,  (self.size_x/2, self.size_y), (self.size_x/2, 0), self.line_thickness)
        
        #if we decided to track score later
        # self.draw_text(screen, (self.size_x/4, 30), "%d" % self.scores[0])
        # self.draw_text(screen, (3*self.size_x/4, 30), "%d" % self.scores[1])

    def draw_text(self, screen, position, string): 
        text = self.font.render(string, True, (0,0,0), None)
        textRect = text.get_rect()
        textRect.center = (position[0], position[1])
        screen.blit(text, textRect)


#start pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1920 , 1080 #render resolution, this will be scaled to the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)


#lidar positioner that handles the parsing of the file into a tuple array. 
#see location_parser.py for parameter description.
lidar_positioner = LocationParser()
soccer_ball = SoccerBall(radius=75)
soccer_field = SoccerField()

running = True #indicates the game is currently running
clock = pygame.time.Clock() #used to moduleate the frame rate and keep successive actions constant

while running:

    #check whether the user quit the game 
    # if so set running to False so we can close on the next iteration
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with black
    screen.fill((0,0,0, 1))
    soccer_field.draw(screen)

    #get positions from the LocationParser
    positions = lidar_positioner.getPositions()
    for xy in positions: 
       pygame.draw.circle(screen, (0,0,255), xy, 10) 

    soccer_ball.move(positions)
    soccer_ball.draw(screen)
    

    #write pixels to the display
    pygame.display.flip()
    
    #wait until next game tick
    clock.tick(120)

#exit
pygame.quit()
sys.exit()
