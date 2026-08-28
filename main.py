#!/bin/python

# ===== import module ===== #
import pygame
import random
import math
import copy

# ===== CONSTANTS ===== #
TILE_SIZE = 32
MINO_LIST = ["I", "J", "L", "O", "S", "Z", "T"]
BLOCK_LIST = [item.lower() for item in MINO_LIST]

# ===== load("image") ===== #
BACK = pygame.image.load("spr/background.png")

MINO_I = pygame.image.load("spr/mino_i.png")
MINO_J = pygame.image.load("spr/mino_j.png")
MINO_L = pygame.image.load("spr/mino_l.png")
MINO_O = pygame.image.load("spr/mino_o.png")
MINO_S = pygame.image.load("spr/mino_s.png")
MINO_Z = pygame.image.load("spr/mino_z.png")
MINO_T = pygame.image.load("spr/mino_t.png")
OUTLINE_MINO = pygame.image.load("spr/outline_mino.png")


# ===== class Object ===== #
class Game:
    def __init__(self, width=10):
        self.width = width
        self.height = 40
        self.matrix = [[0 for x in range(self.width)] for y in range(self.height)]
        self.pivot = [0, 0]

        self.bag = random.sample(MINO_LIST, len(MINO_LIST))

        self.ui_width = 5

        self.running = True
        self.dead = False

        self.display = pygame.display.set_mode(
            [(self.width + self.ui_width * 2) * TILE_SIZE, 20 * TILE_SIZE]
        )
        self.clock = pygame.time.Clock()
        self.ticks = 0

    def run(self):
        self.running = True

        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_DOWN:
                        self.shift("down")
                    if event.key == pygame.K_LEFT:
                        self.shift("left")
                    if event.key == pygame.K_RIGHT:
                        self.shift("right")

            if not self.isActive():
                self.spawnTetromino(self.bagCall())

            if self.ticks > 0 and not self.ticks % 20:
                self.shift("down")

            self.attemptLineClear()

            self.drawAll()
            pygame.display.flip()

            if self.dead:
                print("BLEGH")

            self.ticks += 1
            self.clock.tick(60)
        pygame.quit()

    def print(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.matrix[y][x], end=" ")
            print()
        print()

    def drawBack(self):
        self.display.fill([49, 50, 68])
        for y in range(self.height):
            for x in range(self.width):
                self.display.blit(
                    BACK, pygame.Vector2(x + self.ui_width, y) * TILE_SIZE
                )

    def drawMino(self):
        buffer_block = []
        buffer_mino = []

        for y in range(self.height):
            for x in range(self.width):
                item = str(self.matrix[y][x])
                for key, value in list(globals().items()):
                    if "MINO_" + item.upper() == key:
                        if item == item.upper():
                            buffer_mino.append({"pos": (x, y), "mino": value})
                        else:
                            buffer_block.append({"pos": (x, y), "block": value})

        for block in buffer_block:
            x, y = block["pos"]
            block_pos = pygame.Vector2(x + self.ui_width, y - 20) * TILE_SIZE
            self.display.blit(block["block"], block_pos)

        for outline in buffer_mino:
            x, y = outline["pos"]
            outline_pos = pygame.Vector2(x + self.ui_width, y - 20) * TILE_SIZE
            outline_pos = pygame.Vector2(outline_pos) - pygame.Vector2(4, 4)
            self.display.blit(OUTLINE_MINO, outline_pos)

        for mino in buffer_mino:
            x, y = mino["pos"]
            mino_pos = pygame.Vector2(x + self.ui_width, y - 20) * TILE_SIZE
            self.display.blit(mino["mino"], mino_pos)

    def drawUI(self):
        pass

    def drawAll(self):
        self.drawBack()
        self.drawMino()
        self.drawUI()

    # converts Cartesian coordinates to cell in field
    def mapper(self, x, y=int()):
        if type(x) is tuple:
            x, y = x
        return [x - 1, self.height - y]

        count = 0
        for y in matrix:
            for x in y:
                if x:
                    count += 1
        return count

    # checks if there are any active tetrominos in the field
    def isActive(self):
        for y in self.matrix:
            for x in y:
                if x in MINO_LIST:
                    return True
        return False

    def spawnTetromino(self, shape):
        before = count(self.matrix)

        if shape in {"I", "O"}:
            offset = math.floor(self.width / 2 - 1)
        else:
            offset = math.ceil(self.width / 2 - 1)

        match shape:
            case "I":
                minos = [
                    (offset, 21),
                    (offset + 1, 21),
                    (offset + 2, 21),
                    (offset + 3, 21),
                ]
                pivot = (5.5, 20.5)
            case "J":
                minos = [(offset, 21), (offset + 1, 21), (offset + 2, 21), (offset, 22)]
                pivot = (0, 0)
            case "L":
                minos = [
                    (offset, 21),
                    (offset + 1, 21),
                    (offset + 2, 21),
                    (offset + 2, 22),
                ]
                pivot = (0, 0)
            case "O":
                minos = [
                    (offset + 1, 21),
                    (offset + 2, 21),
                    (offset + 1, 22),
                    (offset + 2, 22),
                ]
                pivot = (0, 0)
            case "S":
                minos = [
                    (offset, 21),
                    (offset + 1, 21),
                    (offset + 1, 22),
                    (offset + 2, 22),
                ]
                pivot = (0, 0)
            case "Z":
                minos = [
                    (offset + 1, 21),
                    (offset + 2, 21),
                    (offset, 22),
                    (offset + 1, 22),
                ]
                pivot = (0, 0)
            case "T":
                minos = [
                    (offset, 21),
                    (offset + 1, 21),
                    (offset + 2, 21),
                    (offset + 1, 22),
                ]
                pivot = (5, 21)
            case _:
                raise Exception(f'tetromino shape "{shape}" not recognized')

        self.pivot = self.mapper(pivot)
        for mino in minos:
            x, y = self.mapper(mino)
            self.matrix[y][x] = shape

        if before + 4 != count(self.matrix):
            self.dead = True
        else:
            self.shift("down")

    # kills active tetromino
    def place(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.matrix[y][x] in MINO_LIST:
                    self.matrix[y][x] = self.matrix[y][x].lower()

    # shifts tetromino left, right, or down (drop)
    def shift(self, direction):
        before = count(self.matrix)
        no_loss = True

        buffer_matrix = copy.deepcopy(self.matrix)

        match direction:
            case "down":
                shift_change = (0, -1)
                for y in range(self.height - 1, -1, -1):
                    for x in range(self.width):
                        try:
                            if buffer_matrix[y][x] in MINO_LIST:
                                buffer_matrix[y + 1][x] = buffer_matrix[y][x]
                                buffer_matrix[y][x] = 0
                        except:
                            no_loss = False
            case "left":
                shift_change = (-1, 0)
                for y in range(self.height):
                    for x in range(self.width):
                        if (
                            x - 1 in range(self.width)
                            and buffer_matrix[y][x] in MINO_LIST
                        ):
                            buffer_matrix[y][x - 1] = buffer_matrix[y][x]
                            buffer_matrix[y][x] = 0
            case "right":
                shift_change = (1, 0)
                for y in range(self.height):
                    for x in range(self.width - 1, -1, -1):
                        if (
                            x + 1 in range(self.width)
                            and buffer_matrix[y][x] in MINO_LIST
                        ):
                            buffer_matrix[y][x + 1] = buffer_matrix[y][x]
                            buffer_matrix[y][x] = 0
            case _:
                raise Exception(f'shift direction "{direction}" invalid')

        if count(buffer_matrix) == before and no_loss:
            self.matrix = buffer_matrix
            self.pivot = pygame.Vector2(self.pivot) + shift_change
        elif direction == "down":
            self.place()

    def rotate(self, direction):
        before = count(self.matrix)
        buffer_matrix = copy.deepcopy(field)

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
            pass  # Check every the spot above every each Mino: If it's empty or another Mino (NOT BLOCK), move them up by one, then check if we've lost any and push up by one. Do this twice.

    def attemptLineClear(self):
        for y in range(self.height):
            count = 0
            for x in self.matrix[y]:
                if x in BLOCK_LIST:
                    count += 1
                if count == self.width:
                    self.matrix.pop(y)
                    self.matrix.insert(0, [0 for x in range(self.width)])
                    return True
        return False

    # retrive tetromino from bag
    def bagCall(self):
        return_value = self.bag[0]
        self.bag.pop(0)
        if len(self.bag) <= 7:
            self.bag += random.sample(MINO_LIST, len(MINO_LIST))
        return return_value


# ===== def function ===== #
# counts number of minos in provided matrix
def count(matrix):
    count = 0
    for y in matrix:
        for x in y:
            if x:
                count += 1
    return count


# ===== Usage ===== #
pygame.init()

game = Game()

game.run()
