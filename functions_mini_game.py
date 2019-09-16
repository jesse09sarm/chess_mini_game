import pygame

# board
ROWS = 8
COLUMNS = 8
SQUARESIZE = 60
BORDER = 40

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (130, 130, 130)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
D_SQUARE = (80, 80, 80)
L_SQUARE = (180, 180, 180)

pygame.init()

# creates screen to display board
screen_size = (COLUMNS * SQUARESIZE + (2 * BORDER), ROWS * SQUARESIZE + (2 * BORDER))
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("CHESS: MINI-GAME")


# intitializes variables for the start of the game
# variables -> selection, turn, selected_piece, prev_x, prev_y, board
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


# draws game board using pygame
# takes in the array of the board as grid
# takes in index of the current selected piece
# if incorrect location or no piece is selected clicked is [-1, -1]
def draw_board(grid, clicked):
    # loads picture file of pawn and queen into variables 
    pawn = pygame.image.load(r"C:\\Users\\jesse\\OneDrive\\Pictures\\pawn.png")
    queen = pygame.image.load(r"C:\\Users\\jesse\\OneDrive\\Pictures\\queen.png")

    # corrects for position in pixels of pawn picture file
    # in order to center the pawn on a square on the chessboard
    pawndiff = -25

    # corrects for position in pixels of x and y direction of queen picture file
    # in order to center the queen on a square on the chessboard
    queenx = 3
    queeny = 4

    # makes the game board by default green 
    pygame.draw.rect(screen, GREEN, (BORDER, BORDER, SQUARESIZE * 8, SQUARESIZE * 8))
    # reason is when a piece is selected the cell will not be colored light gray or dark gray
    # therefore the cell will be highlighted green
    # shows the user which piece will be moved with the next click

    # iterates through every cell of the board 
    # colors in light and dark squares
    # places a pawn image and queen image on the correct cells 
    for r in range(ROWS):
        for c in range(COLUMNS):

            # colors in light and dark squares only if the cell is not the selected piece's cell
            if clicked[0] != r or clicked[1] != c:

                # colors in dark squares on the board
                if c % 2 != r % 2:
                    pygame.draw.rect(screen, D_SQUARE, (SQUARESIZE * c + BORDER, SQUARESIZE * r + BORDER, SQUARESIZE, SQUARESIZE))
                
                # colors in light squares on the board
                else:
                    pygame.draw.rect(screen, L_SQUARE, (SQUARESIZE * c + BORDER, SQUARESIZE * r + BORDER, SQUARESIZE, SQUARESIZE))
            
            # places a pawn image on the board where the value of the cell is "p"
            if grid[r][c] == "p":
                screen.blit(pawn, (c * SQUARESIZE + BORDER + pawndiff, r * SQUARESIZE + BORDER + pawndiff))

            # places a pawn image on the board where the value of the cell is "Q"
            elif grid[r][c] == "Q":
                screen.blit(queen, (c * SQUARESIZE + BORDER + queenx, r * SQUARESIZE + BORDER + queeny))

    # letters represent the labels of the columns of a chessboard
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]

    # iterates over letters to add labels of rows and columns to the chessboard 
    for i in range(len(letters)):

        # creates text boxes for letter labels on the horizontal
        text, x2, y2 = message(26, letters[i], WHITE)
        x1 = (SQUARESIZE - x2) / 2
        y1 = (BORDER - y2) / 2
        
        # places the text block on the screen display that contains the drawn board
        screen.blit(text, (i * SQUARESIZE + BORDER + x1, ROWS * SQUARESIZE + BORDER + y1, SQUARESIZE - x1, BORDER - y1))

        # creates text boxes for numeric labels on the vertical
        text, x2, y2 = message(26, str(ROWS - i), WHITE)
        x1 = (BORDER - x2) / 2
        y1 = (SQUARESIZE - y2) / 2

        # places the text block on the screen display that contains the drawn board
        screen.blit(text, (x1, i * SQUARESIZE + BORDER + y1, BORDER - x1, SQUARESIZE - y1))

    # simply updates the display of the board
    pygame.display.update()


# converts the pixel x,y location of the mouse click to the index of the board array
def get_cell(x, y):
    # checks if the mouse click was on the board not on the border
    # returns a flipped x,y because pygame has 0,0 at the top left corner
    if BORDER < x < COLUMNS * SQUARESIZE + BORDER and BORDER < y < ROWS * SQUARESIZE + BORDER:
        return int((y - BORDER) / SQUARESIZE), int((x - BORDER) / SQUARESIZE)

    # returns -1,-1 when the click was not on the board
    else:
        return -1, -1


# takes size, text, color of new message to be displayed
# returns configured text block and width,height dimensions
# dimensions so text block can be centered in desired location of the screen
def message(size, word, color):
    # sets font with hard coded font type and passed in size 
    set_font = pygame.font.SysFont("Courier New", size, True)

    # creates text block with passed in message and color
    set_color = set_font.render(word, True, color)

    # gets dimension of text block in form [left,top,width,height]
    get_dimension = set_color.get_rect()

    return set_color, get_dimension[2], get_dimension[3]


# makes sure the intended pawn move is a legal chess move 
# first is the current index of the piece 
# next is the intended index 
def valid_pmove(firstx, firsty, nextx, nexty, grid):
    # can not move to a place where another pawn currently is
    # can not move backwards
    # can not move more than 2 squares forward at a time
    # can not move more than one square horizontally 
    if grid[nextx][nexty] == "p" or firstx <= nextx or firstx - nextx > 2 or firsty - nexty > 1:
        return False

    # for pawn moving up the board
    if nextx < firstx:

        # straight forward pawn move
        if nexty == firsty:

            # can only move forward more than one square if in starting position
            if firstx - nextx > 1 and firstx != ROWS - 2 or grid[nextx][nexty] == "Q":
                return False

            # valid move forward
            else:
                return True

        # diagonal pawn move
        else:
            # can only move one sqaure diagonally to capture a piece
            if grid[nextx][nexty] == "" or firstx - nextx > 1:
                return False

            # valid pawn capture
            else:
                return True


# makes sure the intended queen move is a legal chess move 
# first is the current index of the piece 
# next is the intended index 
def valid_Qmove(firstx, firsty, nextx, nexty, grid):
    # pressing its own square is not a movement 
    if grid[nextx][nexty] == "Q":
        return False

    # for down, down right, down left, right, left movements 
    if nextx >= firstx:

        # for a down movement
        if nexty == firsty:

            # queen can not jump over a pawn 
            for i in range(nextx - firstx):
                if grid[firstx + i][firsty] == "p":
                    return False

            # valid move down 
            return True

        # for down right and right movements
        elif nexty > firsty:
            
            # for a right movement
            if nextx == firstx:

                # queen can not jump over a pawn
                for i in range(nexty - firsty):
                    if grid[firstx][firsty + i] == "p":
                        return False

                # valid move to the right
                return True
        
            # for a down right movement
            elif abs(nextx - firstx) == abs(nexty - firsty):

                # queen can not jump over a pawn
                for i in range(abs(nextx - firstx)):
                    if grid[firstx + i][firsty + i] == "p":
                        return False

                # valid move down right 
                return True

            # invalid move
            # intended path was not perfectly diagonal or horizontal
            else:
                return False

        # for a left movement
        elif nextx == firstx:

            # queen can not jump over a pawn
            for i in range(firsty - nexty):
                if grid[firstx][firsty - i] == "p":
                    return False

            # valid move to the left
            return True

        # for a down left
        elif abs(nextx - firstx) == abs(nexty - firsty):

            # queen can not jump over a pawn
            for i in range(abs(nextx - firstx)):
                if grid[firstx + i][firsty - i] == "p":
                    return False

            # valid move down left
            return True

        # invalid move
        # intended path was not perfectly diagonal or horizontal
        else:
            return False

    # for an up movement
    elif nexty == firsty:
        # queen can not jump over a pawn
        for i in range(firstx - nextx):
            if grid[firstx - i][firsty] == "p":
                return False

        # valid move up
        return True
        
    # for up right and up left movements
    elif abs(nextx - firstx) == abs(nexty - firsty):

        # for an up right movement 
        if nexty > firsty:

            # queen can not jump over a pawn
            for i in range(abs(nextx - firstx)):
                if grid[firstx - i][firsty + i] == "p":
                    return False

            # valid move up right
            return True

        # for an up left movement
        else:

            # queen can not jump over a pawn
            for i in range(abs(nextx - firstx)):
                if grid[firstx - i][firsty - i] == "p":
                    return False

            # valid move up left
            return True

    # invalid move
    # intended path was not perfectly diagonal or horizontal
    else:
        return False


# checks if a player has won 
# passes in the board and player's turn
def check_end(grid, player):
    # checks if pawn has reached the top of the board
    if "p" in grid[0]:
        return True

    # needs to count pawns for edge case where a pawn is still on the board
    # but has no valid move
    pawn_count = 0

    # bool for piece to check if it is still on the board
    queen = False

    # when queen is front of a pawn blocking its path forward
    # used for edge case when only one pawn left
    trapped = False

    # iterates through board to find pieces 
    for r in range(ROWS):
        for c in range(COLUMNS):
            if grid[r][c] == "p":
                pawn_count += 1
            if grid[r][c] == "Q":
                queen = True

                # try block for when queen is on first rank can not check lower row
                try:

                    # checks if queen is blocking path of a pawn
                    if grid[r + 1][c] == "p":
                        trapped = True
                    else:
                        trapped = False

                # queen on first rank means is not in front of any pawn
                except IndexError:
                    trapped = False

            # when more than one pawn queen can not trap both moves
            if queen and pawn_count > 1:
                return False

    # when one piece is no longer on the board game is over
    if not queen or pawn_count == 0:
        return True

    # edge case when it is pawns move but queen blocks only move forward
    if player == 2 and trapped:
        return True
    else: 
        return False
        

# runs at the end of game 
# passed in value is the turn that it ended on to figure out winner
# asks user if wants to play again
def game_over(player):
    # pauses for one second
    # gives user time to see final position 
    pygame.time.wait(1000)

    # draws colored rectangles on screen to hold game over message
    pygame.draw.rect(screen, GRAY, (SQUARESIZE * 2.5 + BORDER, SQUARESIZE * 2.5 + BORDER, SQUARESIZE * 3, SQUARESIZE * 1.5))
    pygame.draw.rect(screen, RED, (SQUARESIZE * 2.5 + BORDER, SQUARESIZE * 4 + BORDER, SQUARESIZE * 1.5, SQUARESIZE * 1.5))
    pygame.draw.rect(screen, GREEN, (SQUARESIZE * 4 + BORDER, SQUARESIZE * 4 + BORDER, SQUARESIZE * 1.5, SQUARESIZE * 1.5))

    # player being 0 means it is whites move
    # check_end() runs after a move which means black made the winning/last move
    if player % 2 == 0:
        winner = "BLACK WINS"
    else:
        winner = "WHITE WINS"

    # configures winner text block 
    text, x1, y1 = message(28, winner, BLACK)
    x = (SQUARESIZE * 3 - x1) / 2
    y = (SQUARESIZE * 1.5 / 2 - y1) / 2

    # centers text block on its colored rectangle 
    screen.blit(text, (SQUARESIZE * 2.5 + BORDER + x, SQUARESIZE * 2.5 + BORDER + y, SQUARESIZE * 3 - x, SQUARESIZE * 1.5 / 2 - y))

    # configures play again text block
    text, x1, y1 = message(24, "PLAY AGAIN?", BLACK)
    x = (SQUARESIZE * 3 - x1) / 2
    y = (SQUARESIZE * 1.5 / 2 - y1) / 2

    # centers text block on its colored rectangle
    screen.blit(text, (SQUARESIZE * 2.5 + BORDER + x, SQUARESIZE * 2.5 + (SQUARESIZE * 1.5 / 2) + BORDER + y, SQUARESIZE * 3 - x, SQUARESIZE * 1.5 / 2 - y))

    # configures choice of NO text block
    text, x1, y1 = message(26, "NO", BLACK)
    x = (SQUARESIZE * 1.5 - x1) / 2
    y = (SQUARESIZE * 1.5 - y1) / 2

    # centers text block on its colored rectangle
    screen.blit(text, (SQUARESIZE * 2.5 + BORDER + x, SQUARESIZE * 4 + BORDER + y, SQUARESIZE * 1.5 - x, SQUARESIZE * 1.5 - y))

    # configures choice of YES text block
    text, x1, y1 = message(26, "YES", BLACK)
    x = (SQUARESIZE * 1.5 - x1) / 2
    y = (SQUARESIZE * 1.5 - y1) / 2

    # centers text block on its colored rectangle
    screen.blit(text, (SQUARESIZE * 4 + BORDER + x, SQUARESIZE * 4 + BORDER + y, SQUARESIZE * 1.5 - x, SQUARESIZE * 1.5 - y))

    # simply updates the display of the board
    pygame.display.update()

    # repeat used to store what choice user made 
    repeat = None

    # loops until user chooses to play again or not
    while True:

        # constantly gets user events such as mouse clicks
        for event2 in pygame.event.get():

            # if user closes the window the system terminates the code
            if event2.type == pygame.QUIT:
                sys.exit()

            # gets users mouse clicks
            if event2.type == pygame.MOUSEBUTTONDOWN:

                # x,y stores the pixel value of the users mouse click
                x = event2.pos[0]
                y = event2.pos[1]

                # checks if the mouse click was one of the choices rectangles 
                # YES block repeat is true, NO block repeat is False
                if SQUARESIZE * 4 + BORDER <= x <= SQUARESIZE * 5.5 + BORDER and SQUARESIZE * 4 + BORDER <= y <= SQUARESIZE * 5.5 + BORDER:
                    repeat = True
                elif SQUARESIZE * 2.5 + BORDER <= x <= SQUARESIZE * 4 + BORDER and SQUARESIZE * 4 + BORDER <= y <= SQUARESIZE * 5.5 + BORDER:
                    repeat = False

        # if repeat was updated from its initial value user made a choice
        if repeat is not None:
            break

    return repeat

