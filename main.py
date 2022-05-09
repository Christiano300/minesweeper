import pygame
from random import choice
pygame.init()

BOARDWIDTH = 20
BOARDHEIGHT = 20
shift_pressed = False
size = width, height = BOARDWIDTH * 25, BOARDHEIGHT * 25 + 50
screen = pygame.display.set_mode(size)
game_running = True
status = 0  # 0 means nothing, 1 means won and -1 means lost

NUMBER_OF_MINES = 30
tiles = pygame.sprite.Group()
clock = pygame.time.Clock()

imagenames = ["empty", "1", "2", "3", "4",
              "5", "6", "7", "8", "flag", "mine", "tile"]
images = [pygame.image.load(
    f"files/{i}.png").convert_alpha() for i in imagenames]


class Tile:
    def __init__(self, x, y):
        self.state = 0
        self.hidden = True
        self.flagged = False
        self.x = x
        self.y = y

    def set_mine(self):
        if self.state == 10:
            choice(choice(board)).set_mine()
        else:
            self.state = 10

    def determine_mines(self):
        if self.state == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x = self.x + i
                    y = self.y + j
                    if x >= 0 and y >= 0:
                        try:
                            if board[y][x].state == 10:
                                self.state += 1
                        except IndexError:
                            pass

    def reveal(self):
        self.hidden = False
        if self.state == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x = self.x + i
                    y = self.y + j
                    if x >= 0 and y >= 0:
                        try:
                            tile = board[y][x]
                            if tile.state in range(9) and tile.hidden and not tile.flagged:
                                tile.reveal()
                        except IndexError:
                            pass

    def draw(self):
        if self.hidden:
            screen.blit(images[-1], (self.x * 25, self.y * 25 + 50))
            if self.flagged:
                screen.blit(images[9], (self.x * 25, self.y * 25 + 50))
        else:
            screen.blit(images[0], (self.x * 25, self.y * 25 + 50))
            screen.blit(images[self.state], (self.x * 25, self.y * 25 + 50))


def process_input(pos: list, reveal: bool) -> int:
    x = pos[0] // 25
    y = (pos[1] - 50) // 25
    if x >= 0 and y >= 0:
        tile = board[y][x]
        if reveal:
            if not tile.flagged:
                tile.reveal()
            if tile.state == 10:
                return -1
        else:
            if tile.hidden:
                if tile.flagged:
                    tile.flagged = False
                else:
                    tile.flagged = True

    won = all([all([j.flagged for j in i if j.state == 10]) for i in board])
    return int(won)


board = [[Tile(i, j) for i in range(BOARDWIDTH)] for j in range(BOARDHEIGHT)]
for i in range(NUMBER_OF_MINES):
    choice(choice(board)).set_mine()
for row in board:
    for tile in row:
        tile.determine_mines()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_running:
                if event.button == 1:
                    status = process_input(event.pos, True)
                elif event.button == 3:
                    status = process_input(event.pos, False)

        elif event.type == pygame.KEYDOWN:
            if game_running:
                if event.key == pygame.K_SPACE:
                    status = process_input(pygame.mouse.get_pos(), True)
                elif event.key == pygame.K_f:
                    status = process_input(pygame.mouse.get_pos(), False)
                elif event.key == pygame.K_c:
                    for row in board:
                        for tile in row:
                            tile.hidden = False

            if event.key == pygame.K_LSHIFT:
                shift_pressed = True
            elif event.key == pygame.K_r:
                if shift_pressed:
                    if game_running:
                        for i in board:
                            for j in i:
                                if j.state == 10 and not j.hidden:
                                    j.hidden = True
                else:
                    for row in board:
                        for tile in row:
                            tile.state = 0
                            tile.hidden = True
                            tile.flagged = False
                    for i in range(NUMBER_OF_MINES):
                        choice(choice(board)).set_mine()
                    for row in board:
                        for tile in row:
                            tile.determine_mines()
                    game_running = True
                    status = 0

        elif event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
            shift_pressed = False

    for row in board:
        for tile in row:
            tile.draw()

    if status:
        game_running = False
        if status == 1:
            screen.blit(pygame.font.Font(None, 35).render(
                "You won!", True, (20, 180, 0)), (5, 50))
        else:
            screen.blit(pygame.font.Font(None, 30).render(
                "You lost!", True, (230, 10, 10)), (5, 50))

    pygame.display.update()
    clock.tick(60)
