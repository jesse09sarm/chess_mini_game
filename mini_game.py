from functions_mini_game import *
import pygame
import sys

# sets variables to begin the game such as the board and player's turn
selection, turn, selected_piece, prev_x, prev_y, board = start_game()

# draws the initial game board
draw_board(board, [prev_x, prev_y])

# set to loop at end of game unless user decides to not play again  
play_again = True

# loops game until user does not want to play again
# when loops game restarts to starting board
while play_again:

    # gets user inputs
    for event in pygame.event.get():

        # user exiting the window causes the code to terminate
        if event.type == pygame.QUIT:
            sys.exit()

        # user performs a mouse click somewhere on the display
        if event.type == pygame.MOUSEBUTTONDOWN:

            # stores x,y location of the mouse click in pixels 
            # 0,0 being the top left corner
            posx = event.pos[0]
            posy = event.pos[1]

            # converts mouse click pixels to indexes on the board 
            selected_x, selected_y = get_cell(posx, posy)

            # selected_x is set to -1 when click was not on the board
            if selected_x != -1:

                # not selection means no piece has been selected
                # meaning this click was intended to select a piece to move
                # must not be empty square
                if not selection and board[selected_x][selected_y] != "":
                    selected_piece = board[selected_x][selected_y]

                    # makes sure selected piece was correct for the player's turn
                    if turn % 2 == 0 and selected_piece == "p" or turn % 2 == 1 and selected_piece == "Q":
                        
                        # piece is now selected
                        # indexes are stored in prev to remove piece when moved
                        selection = True
                        prev_x = selected_x
                        prev_y = selected_y

                # piece was already selected so new click is an intended move 
                # checks if move is valid
                elif selection:

                    # bool makes sure of valid move
                    moved = False

                    # checks valid pawn move
                    if turn % 2 == 0:
                        if valid_pmove(prev_x, prev_y, selected_x, selected_y, board):
                            moved = True

                    # checks valid queen move
                    else:
                        if valid_Qmove(prev_x, prev_y, selected_x, selected_y, board):
                            moved = True

                    # moves piece to selected location
                    # changes prev to empty square and changes turns
                    if moved:
                        board[selected_x][selected_y] = selected_piece
                        board[prev_x][prev_y] = ""
                        turn = (turn % 2) + 1

                    # resets selection of piece even after a piece is not moved
                    # intended to give the user a chance to change their choice
                    # simply by selecting an invalid move location or outside the board
                    selected_piece = ""
                    prev_x = ""
                    prev_y = ""
                    selection = False

            # draws game board
            # needs prev to know which square to highlight green if one is selected
            draw_board(board, [prev_x, prev_y])

            # checks if someone has won
            if check_end(board, turn):

                # asks user to play again
                play_again = game_over(turn)

                # users wants to play again
                # resets variables to start game case
                if play_again:
                    selection, turn, selected_piece, prev_x, prev_y, board = start_game()
                    draw_board(board, [prev_x, prev_y])
