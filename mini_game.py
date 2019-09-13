from functions_mini_game import *
import pygame
import sys

selection, turn, selected_piece, prev_x, prev_y, board = start_game()

draw_board(board, [prev_x, prev_y])

play_again = True
while play_again:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0]
            posy = event.pos[1]
            selected_x, selected_y = get_cell(posx, posy)
            if selected_x != -1:
                if not selection and board[selected_x][selected_y] != "":
                    selected_piece = board[selected_x][selected_y]
                    if turn % 2 == 0 and selected_piece == "p" or turn % 2 == 1 and selected_piece == "Q":
                        selection = True
                        prev_x = selected_x
                        prev_y = selected_y
                elif selection:
                    moved = False
                    if turn % 2 == 0:
                        if valid_pmove(prev_x, prev_y, selected_x, selected_y, board):
                            moved = True
                    else:
                        if valid_Qmove(prev_x, prev_y, selected_x, selected_y, board):
                            moved = True
                    if moved:
                        board[selected_x][selected_y] = selected_piece
                        board[prev_x][prev_y] = ""
                        turn = (turn % 2) + 1
                    selected_piece = ""
                    prev_x = ""
                    prev_y = ""
                    selection = False
            draw_board(board, [prev_x, prev_y])
            if check_end(board):
                play_again = game_over(turn)
                if play_again:
                    selection, turn, selected_piece, prev_x, prev_y, board = start_game()
                    draw_board(board, [prev_x, prev_y])
