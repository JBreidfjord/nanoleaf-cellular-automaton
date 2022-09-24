import random


def create_rand_board(gameboard):
    cells_to_turn = random.randrange(100, 131)
    for i in range(0, cells_to_turn):
        good_cell = False
        while good_cell == False:
            turning_cell_row = random.randrange(0, 12)
            turning_cell_col = random.randrange(0, 23)
            if gameboard[turning_cell_row][turning_cell_col] == "x" or gameboard[turning_cell_row][turning_cell_col] == "alive":
                good_cell = False
            else:
                good_cell = True
        update_game_panel(turning_cell_row, turning_cell_col, "alive", gameboard)


