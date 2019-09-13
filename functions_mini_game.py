import pygame

ROWS = 8
COLUMNS = 8
SQUARESIZE = 60
BORDER = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (130, 130, 130)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
D_SQUARE = (80, 80, 80)
L_SQUARE = (180, 180, 180)

pygame.init()

screen_size = (COLUMNS * SQUARESIZE + (2 * BORDER), ROWS * SQUARESIZE + (2 * BORDER))
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("CHESS: MINI-GAME")


def start_game():
    clicked = False
    player_turn = 0
    curr_piece = ""
    first_x = ""
    first_y = ""
    grid = [["", "", "", "Q", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["", "", "", "", "", "", "", ""],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["", "", "", "", "", "", "", ""]]
    return clicked, player_turn, curr_piece, first_x, first_y, grid


def draw_board(grid, clicked):
    pawndiff = -25
    queenx = 3
    queeny = 4

    pawn = pygame.image.load(r"C:\\Users\\jesse\\OneDrive\\Pictures\\pawn.png")
    queen = pygame.image.load(r"C:\\Users\\jesse\\OneDrive\\Pictures\\queen.png")

    pygame.draw.rect(screen, GREEN, (BORDER, BORDER, SQUARESIZE * 8, SQUARESIZE * 8))
    for r in range(ROWS):
        for c in range(COLUMNS):
            if clicked[0] != r or clicked[1] != c:
                if c % 2 != r % 2:
                    pygame.draw.rect(screen, D_SQUARE, (SQUARESIZE * c + BORDER, SQUARESIZE * r + BORDER, SQUARESIZE, SQUARESIZE))
                else:
                    pygame.draw.rect(screen, L_SQUARE, (SQUARESIZE * c + BORDER, SQUARESIZE * r + BORDER, SQUARESIZE, SQUARESIZE))
            if grid[r][c] != "":
                if grid[r][c] == "p":
                    screen.blit(pawn, (c * SQUARESIZE + BORDER + pawndiff, r * SQUARESIZE + BORDER + pawndiff))
                else:
                    screen.blit(queen, (c * SQUARESIZE + BORDER + queenx, r * SQUARESIZE + BORDER + queeny))

    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    for i in range(len(letters)):
        font = pygame.font.SysFont("Courier New", 26, True)

        text1 = font.render(letters[i], True, WHITE)
        x, y, x1, y1 = text1.get_rect()
        x1 = (SQUARESIZE - x1) / 2
        y1 = (BORDER - y1) / 2

        text2 = font.render(str(ROWS - i), True, WHITE)
        x, y, x2, y2 = text2.get_rect()
        x2 = (BORDER - x2) / 2
        y2 = (SQUARESIZE - y2) / 2

        screen.blit(text1, (i * SQUARESIZE + BORDER + x1, ROWS * SQUARESIZE + BORDER + y1, SQUARESIZE - x1, BORDER - y1))
        screen.blit(text2, (x2, i * SQUARESIZE + BORDER + y2, BORDER - x2, SQUARESIZE - y2))

    pygame.display.update()


def get_cell(x, y):
    if BORDER < x < COLUMNS * SQUARESIZE + BORDER and BORDER < y < ROWS * SQUARESIZE + BORDER:
        return int((y - BORDER) / SQUARESIZE), int((x - BORDER) / SQUARESIZE)
    else:
        return -1, -1


def valid_pmove(firstx, firsty, nextx, nexty, grid):
    if grid[nextx][nexty] == "p" or firstx <= nextx or firstx - nextx > 2 or firsty - nexty > 1:
        return False
    if nextx < firstx:
        if nexty == firsty:
            if firstx - nextx > 1 and firstx != ROWS - 2 or grid[nextx][nexty] == "Q":
                return False
            else:
                return True
        else:
            if grid[nextx][nexty] == "" or firstx - nextx > 1:
                return False
            else:
                return True


def valid_Qmove(firstx, firsty, nextx, nexty, grid):
    if grid[nextx][nexty] == "Q":
        return False

    # down 
    # down right 
    # down left 
    # right 
    # left 
    if nextx >= firstx:
        # down
        if nexty == firsty:
            for i in range(nextx - firstx):
                if grid[firstx + i][firsty] == "p":
                    return False
            return True
        # right
        # down right
        elif nexty > firsty:
            # right
            if nextx == firstx:
                for i in range(nexty - firsty):
                    if grid[firstx][firsty + i] == "p":
                        return False
                return True
            # down right
            elif abs(nextx - firstx) == abs(nexty - firsty):
                for i in range(abs(nextx - firstx)):
                    if grid[firstx + i][firsty + i] == "p":
                        return False
                return True
            # invalid move
            else:
                return False
        # left
        elif nextx == firstx:
            for i in range(firsty - nexty):
                if grid[firstx][firsty - i] == "p":
                    return False
            return True
        # down left
        elif abs(nextx - firstx) == abs(nexty - firsty):
            for i in range(abs(nextx - firstx)):
                if grid[firstx + i][firsty - i] == "p":
                    return False
            return True
        # invalid move
        else:
            return False
    # up
    elif nexty == firsty:
        for i in range(firstx - nextx):
            if grid[firstx - i][firsty] == "p":
                return False
        return True
    # up right
    # up left
    elif abs(nextx - firstx) == abs(nexty - firsty):
        # up right 
        if nexty > firsty:
            for i in range(abs(nextx - firstx)):
                if grid[firstx - i][firsty + i] == "p":
                    return False
            return True
        # up left
        else:
            for i in range(abs(nextx - firstx)):
                if grid[firstx - i][firsty - i] == "p":
                    return False
            return True
    # invalid move
    else:
        return False


def check_end(grid):
    if "p" in grid[0]:
        return True
    pawn = False
    queen = False
    for r in range(ROWS):
        for c in range(COLUMNS):
            if grid[r][c] == "p":
                pawn = True
            if grid[r][c] == "Q":
                queen = True
            if pawn and queen:
                return False
    return True


def game_over(player):
    pygame.time.wait(1000)
    pygame.draw.rect(screen, GRAY, (SQUARESIZE * 2.5 + BORDER, SQUARESIZE * 2.5 + BORDER, SQUARESIZE * 3, SQUARESIZE * 1.5))
    pygame.draw.rect(screen, RED, (SQUARESIZE * 2.5 + BORDER, SQUARESIZE * 4 + BORDER, SQUARESIZE * 1.5, SQUARESIZE * 1.5))
    pygame.draw.rect(screen, GREEN, (SQUARESIZE * 4 + BORDER, SQUARESIZE * 4 + BORDER, SQUARESIZE * 1.5, SQUARESIZE * 1.5))

    if player % 2 == 0:
        winner = "BLACK WINS"
    else:
        winner = "WHITE WINS"

    font = pygame.font.SysFont("Courier New", 28, True)
    text = font.render(winner, True, BLACK)
    x1, y1, x2, y2 = text.get_rect()
    x = (SQUARESIZE * 3 - x2) / 2
    y = (SQUARESIZE * 1.5 / 2 - y2) / 2
    screen.blit(text, (SQUARESIZE * 2.5 + BORDER + x, SQUARESIZE * 2.5 + BORDER + y, SQUARESIZE * 3 - x, SQUARESIZE * 1.5 / 2 - y))

    font = pygame.font.SysFont("Courier New", 24, True)
    text = font.render("PLAY AGAIN?", True, BLACK)
    x1, y1, x2, y2 = text.get_rect()
    x = (SQUARESIZE * 3 - x2) / 2
    y = (SQUARESIZE * 1.5 / 2 - y2) / 2
    screen.blit(text, (SQUARESIZE * 2.5 + BORDER + x, SQUARESIZE * 2.5 + (SQUARESIZE * 1.5 / 2) + BORDER + y, SQUARESIZE * 3 - x, SQUARESIZE * 1.5 / 2 - y))

    font = pygame.font.SysFont("Courier New", 26, True)
    text = font.render("NO", True, BLACK)
    x1, y1, x2, y2 = text.get_rect()
    x = (SQUARESIZE * 1.5 - x2) / 2
    y = (SQUARESIZE * 1.5 - y2) / 2
    screen.blit(text, (SQUARESIZE * 2.5 + BORDER + x, SQUARESIZE * 4 + BORDER + y, SQUARESIZE * 1.5 - x, SQUARESIZE * 1.5 - y))

    font = pygame.font.SysFont("Courier New", 26, True)
    text = font.render("YES", True, BLACK)
    x1, y1, x2, y2 = text.get_rect()
    x = (SQUARESIZE * 1.5 - x2) / 2
    y = (SQUARESIZE * 1.5 - y2) / 2
    screen.blit(text, (SQUARESIZE * 4 + BORDER + x, SQUARESIZE * 4 + BORDER + y, SQUARESIZE * 1.5 - x, SQUARESIZE * 1.5 - y))

    pygame.display.update()

    repeat = None
    while True:
        for event2 in pygame.event.get():
            if event2.type == pygame.QUIT:
                sys.exit()
            if event2.type == pygame.MOUSEBUTTONDOWN:
                x = event2.pos[0]
                y = event2.pos[1]
                if SQUARESIZE * 4 + BORDER <= x <= SQUARESIZE * 5.5 + BORDER and SQUARESIZE * 4 + BORDER <= y <= SQUARESIZE * 5.5 + BORDER:
                    repeat = True
                elif SQUARESIZE * 2.5 + BORDER <= x <= SQUARESIZE * 4 + BORDER and SQUARESIZE * 4 + BORDER <= y <= SQUARESIZE * 5.5 + BORDER:
                    repeat = False
        if repeat is not None:
            break
    return repeat

