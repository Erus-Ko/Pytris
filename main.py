#!/bin/python

import pygame
import random
import copy

# ========== CONSTANT_INITIALIZATIONS ========== #

ACTIVE_IDS = {"I", "J", "L", "O", "S", "Z", "T"}

# ========== variable_initializations ========== #

magnify = 20

# ========== ClassDefinitions ========== #

class Bagger:
    def __init__(self):
        self.bag = ACTIVE_IDS

class AutoDropper:
    def __init__(self):
        self.progress = 0
    def drop(self, gravity):
        self.progress += gravity
        while self.progress > 0:
            self.progress -= 1
            drop()

# ========== functionDefinitions ========== #

def mapper(x, y):
    return [x - 1, 40 - y]

def constructField(width = 10, height = 40):
    global field
    field = []
    for y in range(height):
        line = []
        for x in range(width):
            line.append(0)
        field.append(line)

def setMatrixElement(selection, coord, identity):
    selection[coord[1]][coord[0]] = identity

def count(selection):
    count = 40
    for y in selection:
        count -= y.count(0)
    return count

def block(selection):
    for y in range(len(selection)):
        for x in range(len(selection[y])):
            if selection[y][x] in ACTIVE_IDS:
                selection[y][x] = selection[y][x].lower()

def spawnTetromino(shape):
    global pivot
    
    before = count(field)

    match shape:
        case "I": # Too Low
            setMatrixElement(field, mapper(4, 21), shape)
            setMatrixElement(field, mapper(5, 21), shape)
            setMatrixElement(field, mapper(6, 21), shape)
            setMatrixElement(field, mapper(7, 21), shape)
            pivot = mapper(5.5, 20.5)
        case "J":
            setMatrixElement(field, mapper(4, 21), shape)
            setMatrixElement(field, mapper(5, 21), shape)
            setMatrixElement(field, mapper(6, 21), shape)
            setMatrixElement(field, mapper(4, 22), shape)
        case "L":
            setMatrixElement(field, mapper(4, 21), shape)
            setMatrixElement(field, mapper(5, 21), shape)
            setMatrixElement(field, mapper(6, 21), shape)
            setMatrixElement(field, mapper(6, 22), shape)
        case "O":
            setMatrixElement(field, mapper(5, 21), shape)
            setMatrixElement(field, mapper(6, 21), shape)
            setMatrixElement(field, mapper(5, 22), shape)
            setMatrixElement(field, mapper(6, 22), shape)
        case "S":
            setMatrixElement(field, mapper(4, 21), shape)
            setMatrixElement(field, mapper(5, 21), shape)
            setMatrixElement(field, mapper(5, 22), shape)
            setMatrixElement(field, mapper(6, 22), shape)
        case "Z":
            setMatrixElement(field, mapper(5, 21), shape)
            setMatrixElement(field, mapper(6, 21), shape)
            setMatrixElement(field, mapper(4, 22), shape)
            setMatrixElement(field, mapper(5, 22), shape)
        case "T":
            setMatrixElement(field, mapper(4, 21), shape)
            setMatrixElement(field, mapper(5, 21), shape)
            setMatrixElement(field, mapper(6, 21), shape)
            setMatrixElement(field, mapper(5, 22), shape)
            pivot = mapper(5, 21)

    if before + 4 != count(field):
        print("DEAD")
    #drop()

def rotateTetromino(direction):
    global pivot
    global field
    
    buffer_matrix = copy.deepcopy(field)
    before = count(buffer_matrix)
    points = []
    
    for y in range(len(buffer_matrix)):
        for x in range(len(buffer_matrix[y])):
            if buffer_matrix[y][x] in ACTIVE_IDS:
                points.append((x - pivot[0], y - pivot[1], buffer_matrix[y][x]))
                buffer_matrix[y][x] = 0
                
    match direction:
        case "ccw":
            for i in points:
                newX = pivot[0] + i[1]
                newY = pivot[1] - i[0]
                if -1 < newX < 10 and -1 < newY < 40:
                    buffer_matrix[int(newY)][int(newX)] = i[2]
        case "cw":
            for i in points:
                newX = pivot[0] - i[1]
                newY = pivot[1] + i[0]
                if -1 < newX < 10 and -1 < newY < 40:
                    buffer_matrix[int(newY)][int(newX)] = i[2]
                
    if before == count(buffer_matrix):
        field = buffer_matrix
    else:
        pass # Check every the spot above every each Mino: If it's empty or another Mino (NOT BLOCK), move them up by one, then check if we've lost any and push up by one. Do this twice.

def moveTetromino(direction):
    global field
    
    buffer_matrix = copy.deepcopy(field)
    before = count(buffer_matrix)
                
    match direction:
        case "left":
            for y in range(len(buffer_matrix)):
                for x in range(len(buffer_matrix[y])):
                    if buffer_matrix[y][x] in ACTIVE_IDS and x > 0:
                        buffer_matrix[y][x - 1] = buffer_matrix[y][x]
                        buffer_matrix[y][x] = 0
            pivot[0] -= 1
        case "right":
            for y in range(len(buffer_matrix)):
                for x in range(len(buffer_matrix[y]) - 1, -1, -1):
                    if buffer_matrix[y][x] in ACTIVE_IDS and x < 9:
                        buffer_matrix[y][x + 1] = buffer_matrix[y][x]
                        buffer_matrix[y][x] = 0
            pivot[0] += 1
                
    if before == count(buffer_matrix):
        field = buffer_matrix

def drop():
    global field
    
    buffer_matrix = copy.deepcopy(field)
    before = count(buffer_matrix)
    
    for y in range(len(buffer_matrix) - 1, -1, -1):
        for x in range(len(buffer_matrix[y])):
            if buffer_matrix[y][x] in ACTIVE_IDS and y < 39:
                buffer_matrix[y + 1][x] = buffer_matrix[y][x]
                buffer_matrix[y][x] = 0
    pivot[1] += 1
    
    if buffer_matrix == field:
        block(buffer_matrix)
        field = buffer_matrix
    elif before == count(buffer_matrix):
        field = buffer_matrix

def hardDrop():
    pass

def printMatrix(selection):
    matrix = "╭────────────────────╮\n"
    for y in range(len(selection)):
        line = ""
        for x in range(len(selection[y])):
            char = " "
            if selection[y][x] in ACTIVE_IDS:
                char = "█"
            elif selection[y][x]:
                char = "▒"
            line += char + char
        matrix += "│" + line + "│" + "\n"
    matrix += "╰────────────────────╯"
    print(matrix)

# ========== Pre-Loop Code ========== #

constructField()

pygame.init()

display = pygame.display.set_mode([20 * magnify, 21 * magnify])
clock = pygame.time.Clock()
fps = 60
done = False

auto_drop = AutoDropper()

G = 5

# ========== Game Loop Code ========== #

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key in {pygame.K_w, pygame.K_UP}:
                hardDrop()
            if event.key in {pygame.K_s, pygame.K_DOWN}:
                drop()
            if event.key in {pygame.K_a, pygame.K_LEFT}:
                moveTetromino("left")
            if event.key in {pygame.K_d, pygame.K_RIGHT}:
                moveTetromino("right")
            if event.key in {pygame.K_q}:
                rotateTetromino("ccw")
            if event.key in {pygame.K_e}:
                rotateTetromino("cw")
    
    auto_drop.drop(G)

    printMatrix(field)
    
    clock.tick(fps)
pygame.quit()
