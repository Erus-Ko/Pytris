import time
import pygame
pygame.init()
done = False
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GREY = (200, 200, 200)
GREY2 = (225, 225, 225)
RED = (255, 0, 0)
RED2 = (200, 0, 0)
BLUE = (0, 0, 255)
magnifier = 20

screen = pygame.display.set_mode((20 * magnifier, 21 * magnifier))
pygame.display.set_caption("Pytris")

matrix = []
for y in range(40):
    line = []
    for x in range(10):
        line.append(0)
    matrix.append(line)

spinPoint = [-1, -1]

def spawnMino(pos, minoType):
    matrix[pos[1]][pos[0] - 1] = minoType

def spawnTetromino(shape):
    global spinPoint
    match shape:
        case "I":
            spawnMino([4, 21], 1)
            spawnMino([5, 21], 1)
            spawnMino([6, 21], 1)
            spawnMino([7, 21], 1)
            spinPoint = [5.5, 20.5]

def rotateMinos(direction):
    blocked = False
    make = []
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == 1:
                point = [x, y]
                global spinPoint
                diffX = point[0] - spinPoint[0]
                diffY = point[1] - spinPoint[1]
                newPoint = []
                match direction:
                    case "CCW":
                        make.append((int(spinPoint[0] - diffY), int(spinPoint[1] + diffX + 1)))
                    case "CW":
                        make.append((int(spinPoint[0] + diffY), int(spinPoint[1] - diffX - 1)))
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == 1:
                matrix[y][x] = 0
    for i in make:
        if matrix[i[1]][i[0]] != 0:
            blocked = True
    if not blocked:
        for i in make:
            spawnMino(i, 1)
    else:
        for i in remove:
            spawnMino(i, 1)

def fall():
    global spinPoint
    blocked = False
    make = []
    for y in range(len(matrix) - 1, -1, -1):
        for x in range(len(matrix[y])):
            if matrix[y][x] == 1 and not blocked:
                make.append((x+1, y-1))
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == 1:
                matrix[y][x] = 0
    for i in make:
        spawnMino(i, 1)
    spinPoint[1] -= 1

def drawMinos():
    global spinPoint
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[y][x] == 1:
                pygame.draw.rect(screen, RED, [
                    (x + 5) * magnifier,
                    (21 - y) * magnifier,
                    magnifier,
                    magnifier,
                    ]
                )
                pygame.draw.rect(screen, RED2, [
                    (x + 5) * magnifier,
                    (21 - y) * magnifier,
                    magnifier,
                    magnifier,
                    ],
                    2
                )
    pygame.draw.circle(screen, BLUE, [(spinPoint[0] + 4.5) * magnifier, (21.5 - spinPoint[1]) * magnifier], 5, 2)

spawnTetromino("I")

for y in range(len(matrix)):
    for x in range(len(matrix[y])):
        print(matrix[y][x], end="")
    print()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rotateMinos("CCW")
            if event.key == pygame.K_RIGHT:
                rotateMinos("CW")
            if event.key == pygame.K_RETURN:
                fall()

    screen.fill(WHITE)

    pygame.draw.rect(screen, GREY, [0, 0, 5 * magnifier, 21 * magnifier])
    pygame.draw.rect(screen, GREY, [15 * magnifier, 0, 5 * magnifier, 21 * magnifier])
    pygame.draw.rect(screen, GREY2, [5 * magnifier, 0, 10 * magnifier, magnifier])

    drawMinos()

    pygame.display.flip()

    clock.tick(60)
pygame.quit()

