#!/bin/python

import pygame
import random
import copy

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

# Tetromino Colors
I_COLOR = (  4, 165, 229)
J_COLOR = ( 30, 102, 245)
L_COLOR = (254, 100,  11)
O_COLOR = (223, 142,  29)
S_COLOR = ( 64, 160,  43)
Z_COLOR = (210,  15,  57)
T_COLOR = (136,  57, 239)
ACTIVE_IDS = {"I", "J", "L", "O", "S", "Z", "T"}

width = 10
height = 40
magnify = 30

pivot = [0, 0]

def setMatrixElement(point, identity):
    matrix[40 - point[1]][point[0] - 1] = identity

def spawnTetromino(shape):
    global pivot
    match shape:
        case "I": # Too Low
            setMatrixElement([4, 21], shape)
            setMatrixElement([5, 21], shape)
            setMatrixElement([6, 21], shape)
            setMatrixElement([7, 21], shape)
            pivot = [1, 20]
        case "J":
            setMatrixElement([4, 21], shape)
            setMatrixElement([5, 21], shape)
            setMatrixElement([6, 21], shape)
            setMatrixElement([4, 22], shape)
            pivot = [5, 21]
        case "L":
            setMatrixElement([4, 21], shape)
            setMatrixElement([5, 21], shape)
            setMatrixElement([6, 21], shape)
            setMatrixElement([6, 22], shape)
            pivot = [5, 21]
        case "O": # Too Low
            setMatrixElement([5, 21], shape)
            setMatrixElement([6, 21], shape)
            setMatrixElement([5, 22], shape)
            setMatrixElement([6, 22], shape)
            pivot = [5.5, 21.5]
        case "S":
            setMatrixElement([4, 21], shape)
            setMatrixElement([5, 21], shape)
            setMatrixElement([5, 22], shape)
            setMatrixElement([6, 22], shape)
            pivot = [5, 21]
        case "Z":
            setMatrixElement([5, 21], shape)
            setMatrixElement([6, 21], shape)
            setMatrixElement([4, 22], shape)
            setMatrixElement([5, 22], shape)
            pivot = [5, 21]
        case "T":
            setMatrixElement([4, 21], shape)
            setMatrixElement([5, 21], shape)
            setMatrixElement([6, 21], shape)
            setMatrixElement([5, 22], shape)
            pivot = [5, 21]
    fall()

def spawnRandom():
    index = random.randrange(7)
    spawnTetromino(list(ACTIVE_IDS)[index])

def countMinos(chosenMatrix):
    count = 0
    for y in range(len(chosenMatrix)):
        for x in range(len(chosenMatrix[y])):
            if chosenMatrix[y][x]:
                count += 1
    return count

def rotate(direction):
    global matrix
    global pivot
    buffer = copy.deepcopy(matrix)
    minosBefore = countMinos(matrix)
    
    for y in range(len(buffer)):
        for x in range(len(buffer[y])):
            if buffer[y][x] in ACTIVE_IDS:
                buffer[y + 1][x] = buffer[y][x]
                buffer[y][x] = 0

def killMinos():
    global matrix
    count = 0
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] in ACTIVE_IDS:
                matrix[y][x] = matrix[y][x].lower()

def fall():
    global matrix
    buffer = copy.deepcopy(matrix)
    minosBefore = countMinos(matrix)
    
    for y in range(len(buffer) - 1, 0, -1):
        for x in range(len(buffer[y])):
            if buffer[y][x] and y < 39 and matrix[y][x] in ACTIVE_IDS:
                buffer[y + 1][x] = buffer[y][x]
                buffer[y][x] = 0
                
    matrixBefore = copy.deepcopy(matrix)
    
    if minosBefore == countMinos(buffer):
        matrix = copy.deepcopy(buffer)
        pivot[1] += 1
    if matrixBefore == matrix:
        killMinos()
        spawnRandom()

def move(direction):
    global matrix
    buffer = copy.deepcopy(matrix)
    minosBefore = countMinos(matrix)
    match direction:
        case "left":
            for y in range(len(buffer)):
                for x in range(len(buffer[y])):
                    if buffer[y][x] in ACTIVE_IDS and x - 1 > -1:
                        buffer[y][x - 1] = buffer[y][x]
                        buffer[y][x] = 0
            
            if minosBefore == countMinos(buffer):
                matrix = copy.deepcopy(buffer)
        case "right":
            for y in range(len(buffer)):
                for x in range(len(buffer[y]) - 1, -1, -1):
                    if buffer[y][x] in ACTIVE_IDS and x < 9:
                        buffer[y][x + 1] = buffer[y][x]
                        buffer[y][x] = 0
            
            if minosBefore == countMinos(buffer):
                matrix = copy.deepcopy(buffer)

def getColor(ids):
    match ids.upper():
        case "I":
            return I_COLOR
        case "J":
            return J_COLOR
        case "L":
            return L_COLOR
        case "O":
            return O_COLOR
        case "S":
            return S_COLOR
        case "Z":
            return Z_COLOR
        case "T":
            return T_COLOR

def drawBoard():
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] != 0:
                pygame.draw.rect(screen, getColor(matrix[y][x]), [0 + (magnify * (x + 5)), 0 + (magnify * (y - 19)), magnify, magnify])
    pygame.draw.rect(screen, (192, 192, 192), [0, 0, 5 * magnify, screen.get_size()[1]])
    pygame.draw.rect(screen, (192, 192, 192), [15 * magnify, 0, 5 * magnify, screen.get_size()[1]])
    pygame.draw.rect(screen, (128, 128, 128), [0, 0, 20 * magnify, magnify * 0.75])
    pygame.draw.circle(screen, BLACK, [0 + (magnify * (pivot[0] + 4)), 0 + (magnify * (pivot[1] - 18))], 5)

pygame.init()
screen = pygame.display.set_mode((20 * magnify, 21 * magnify))
pygame.display.set_caption("Pytris")
clock = pygame.time.Clock()
done = False

matrix = []
for y in range(height):
    line = []
    for x in range(width):
        line.append(0)
    matrix.append(line)

spawnRandom()
setMatrixElement([1, 1], "i")
setMatrixElement([1, 2], "i")
setMatrixElement([4, 2], "i")

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fall()
            if event.key == pygame.K_a:
                move("left")
            if event.key == pygame.K_d:
                move("right")
            if event.key == pygame.K_q:
                rotate("left")
            if event.key == pygame.K_e:
                rotate("right")
            if event.key == pygame.K_RETURN:
                killMinos()

    screen.fill(WHITE)

    drawBoard()

    pygame.display.flip()

    clock.tick(60)
pygame.quit()
