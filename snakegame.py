"""
@author: J-Potes
"""
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import copy

from random import seed
from random import randint

# Function to draw a line with OpenGL
def line(pA, pB, color):
    clr = [0,0,0]
    clr[0] = float(color[0]/255)
    clr[1] = float(color[1]/255)
    clr[2] = float(color[2]/255)
    glBegin(GL_LINES)
    glColor3f(clr[0], clr[1], clr[2])
    glVertex2f(pA[0], pA[1])
    glVertex2f(pB[0], pB[1])
    glEnd()


def square(ini_pos, length, color):
    i = int(length/2)
    px = ini_pos[0]
    py = ini_pos[1]
    line([px-i,py+i], [px+i,py+i], color)
    line([px+i,py+i], [px+i,py-i], color)
    line([px+i,py-i], [px-i,py-i], color)
    line([px-i,py-i], [px-i,py+i], color)

# Function to draw a square with OpenGL
def square_fill(ini_pos, length, color):
    half = int(length/2)
    
    px = ini_pos[0]
    py = ini_pos[1]
    
    start_x = px - half
    end_x = px + half
    start_y = py - half
    end_y = py + half
    
    i = start_y
    while(i <= end_y):
        line([start_x,i], [end_x,i], color)
        i += 1

def closest_mult(number, mult):
    n = number
    find = False
    while(find == False):
        if(n % mult != 0):
            n -= 1
        else:
            find = True
            break
    return n
    

class point:
    # Class contructor
    def __init__(self, pos, color, size, direction, new_direction):
        self.pos = pos
        self.color = color
        self.size = size
        self.dir = direction
        self.n_dir = new_direction
    
    def move_point(self):
        # Up
        if(self.dir == 1):
            self.pos[1] += self.size
        # Right
        elif(self.dir == 2):
            self.pos[0] += self.size
        # Down
        elif(self.dir == 3):
            self.pos[1] -= self.size
        # Left
        elif(self.dir == 4):
            self.pos[0] -= self.size
        
        if(self.dir != self.n_dir):
            self.dir = self.n_dir
    
    def show_point(self):
        square_fill(self.pos, self.size, self.color)
        square(self.pos, self.size, [0,0,0])
        
        
class snake:
    # Class contructor
    def __init__(self, point_list):
        self.p_list = point_list
    
    def check_directions(self):
        # Set the direction changes for the rest of the snake
        for i in range (1, len(self.p_list)):
            if(self.p_list[i].dir != self.p_list[i-1].dir):
                self.p_list[i].n_dir = self.p_list[i-1].dir
    
    def change_direction(self, n_direction):
        # Change direction of the head of the snake
        self.p_list[0].n_dir = n_direction
        self.p_list[0].dir = n_direction
        self.p_list[0].n_dir_pos = self.p_list[0].pos
    
    
    def show_snake(self):
        for i in range (0, len(self.p_list)):
            self.p_list[i].show_point()
            
    def move(self):
        for i in range (0, len(self.p_list)):
            self.p_list[i].move_point()
    
    def grow(self):
        last_pos = copy.deepcopy(self.p_list[len(self.p_list)-1].pos)
        last_dir = copy.deepcopy(self.p_list[len(self.p_list)-1].dir)
        last_color = copy.deepcopy(self.p_list[len(self.p_list)-1].color)
        new_dir = last_dir
        new_size = point_size
        new_color = last_color
        new_color[0] += 8
        new_color[2] += 8
        new_pos = last_pos
        # Up
        if(last_dir == 1):
            new_pos[1] -= new_size
        # Right
        elif(last_dir == 2):
            new_pos[0] -= new_size
        # Down
        elif(last_dir == 3):
            new_pos[1] += new_size
        # Left
        elif(last_dir == 4):
            new_pos[0] += new_size
        
        self.p_list.append(point(new_pos,new_color,new_size,new_dir,new_dir))
    
    def check_hit_self(self):
        hit = False
        long = len(self.p_list)
        for i in range (2, long):
            if(self.p_list[0].pos == self.p_list[i].pos):
                hit = True
                break
        return hit
    
    def check_hit_border(self, bdr):
        hit = False
        pos_x = self.p_list[0].pos[0]
        pos_y = self.p_list[0].pos[1]
        if(pos_x <= bdr.x_inf or pos_x >= bdr.x_sup):
            hit = True
        if(pos_y <= bdr.y_inf or pos_y >= bdr.y_sup):
            hit = True
        return hit
        
        

class fruit:
    # Class contructor
    def __init__(self, position, color, size):
        self.pos = position
        self.color = color
        self.size = size
    
    def reposition(self, snk):
        match = True
        # seed(1)
        while(match == True):
            match = False
            x_pos = closest_mult(randint(0 + point_size, x_axis - point_size), point_size)
            y_pos = closest_mult(randint(0 + point_size, y_axis - point_size), point_size)
            print("Apple pos: [",x_pos," , ",y_pos,"]")
            for i in range (0, len(snk.p_list)):
                if(x_pos == snk.p_list[i].pos[0] and y_pos == snk.p_list[i].pos[1]):
                    match = True
                    break
        self.pos[0] = x_pos
        self.pos[1] = y_pos
    
    def show(self):
        square_fill(self.pos, self.size-2, self.color)
        
        
class border:
    # Class contructor
    def __init__(self, x_inf, x_sup, y_inf, y_sup, color, size):
        self.x_inf = x_inf
        self.x_sup = x_sup
        self.y_inf = y_inf
        self.y_sup = y_sup
        self.color = color
        self.size = size
    
    def show(self):
        i = self.x_inf
        while(i <= self.x_sup):
            square_fill([i,self.y_inf], self.size, self.color)
            i += self.size
        
        i = self.x_inf
        while(i <= self.x_sup):
            square_fill([i,self.y_sup], self.size, self.color)
            i += self.size
        
        j = self.y_inf + self.size
        while(j < self.y_sup):
            square_fill([self.x_inf,j], self.size, self.color)
            j += self.size
        
        j = self.y_inf + self.size
        while(j < self.y_sup):
            square_fill([self.x_sup,j], self.size, self.color)
            j += self.size
    
def approve_dir(current_dir, n_dir):
    state = True
    if(current_dir == 1 and n_dir == 3):
        state = False
    
    if(current_dir == 2 and n_dir == 4):
        state = False
        
    if(current_dir == 3 and n_dir == 1):
        state = False
    
    if(current_dir == 4 and n_dir == 2):
        state = False
    
    return state

def lose(snk, bdr):
    lost = False
    auto_hit = snk.check_hit_self()
    bdr_hit = snk.check_hit_border(bdr)
    
    if(auto_hit == True or bdr_hit == True):
        lost = True
        
    return lost

# Axis limit for the 2D space
x_axis = 600
y_axis = 600

# Size of the window
width = 600
heigth = 600


point_size = 30

snake_list = []
initial_size = 4
ini_color = [43,183,185]
for i in range (0, initial_size):
    snake_list.append(point([int(x_axis/2)-(i*point_size),int(y_axis/2)],[ini_color[0]+(i*8),ini_color[1],ini_color[2]+(i*8)],point_size,2,2))

snake = snake(snake_list)
apple = fruit([closest_mult(randint(0,x_axis), point_size),closest_mult(randint(0,y_axis), point_size)],[238,61,61],point_size)
apple.reposition(snake)

border = border(0, x_axis, 0, y_axis, [231,163,238], point_size)

# Funcion principal
def main():
    global snake, apple, border
    running = True
    paused = False
    
    # Se crea la ventana
    pygame.init()
    display=(width,heigth)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluOrtho2D(0,x_axis,0,y_axis)
    
    # Ciclo para que se vaya visualizando la simulacion
    while running:
        auto_hit = False
        c_dir = False
        n_dir = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running=False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    print("Up")
                    c_dir = True
                    n_dir = 1
                elif event.key == K_DOWN:
                    print("Down")
                    c_dir = True
                    n_dir = 3
                elif event.key == K_RIGHT:
                    print("Right")
                    c_dir = True
                    n_dir = 2
                elif event.key == K_LEFT:
                    print("Left")
                    c_dir = True
                    n_dir = 4
                if event.key == K_SPACE:
                    if paused == True:
                        paused = False
                    elif paused == False:
                        paused = True
        if(running == True and paused == False):
            glFlush()
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            lost = lose(snake, border)
            if(lost == False):
                if(apple.pos == snake.p_list[0].pos):
                    snake.grow()
                    apple.reposition(snake)
                # snake.grow()
                if(c_dir == True):
                    valid = approve_dir(snake.p_list[0].dir, n_dir)
                    if(valid == True):
                        snake.change_direction(n_dir)
                snake.check_directions()
                snake.move()
            
            border.show()
            apple.show()
            snake.show_snake()
            pygame.time.wait(500)
            pygame.display.flip()
pygame.quit()

main()