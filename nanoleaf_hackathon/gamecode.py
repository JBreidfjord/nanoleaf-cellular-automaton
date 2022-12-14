import random
import time
#from nanoleaf_hackathon.nanoleaf import Nanoleaf, PanelUpdate

dead_gameboard = [
    [
        "x",
        "x",
        "x",
        "x",
        "x",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "x",
        "x",
        "x",
        "x",
        "x",
    ],
    [
        "x",
        "x",
        "x",
        "x",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "x",
        "x",
        "x",
        "x",
    ],
    [
        "x",
        "x",
        "x",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "x",
        "x",
        "x",
    ],
    [
        "x",
        "x",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "x",
        "x",
    ],
    [
        "x",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "x",
    ],
    [
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
    ],
    [
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
    ],
    [
        "x",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "x",
    ],
    [
        "x",
        "x",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "x",
        "x",
    ],
    [
        "x",
        "x",
        "x",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "x",
        "x",
        "x",
    ],
    [
        "x",
        "x",
        "x",
        "x",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "x",
        "x",
        "x",
        "x",
    ],
    [
        "x",
        "x",
        "x",
        "x",
        "x",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "dead",
        "x",
        "x",
        "x",
        "x",
        "x",
    ],
]

#nl = Nanoleaf(demo_mode=False)
#
#
#def update_panels(gameboard):
#    updates = []
#    for i, row in enumerate(gameboard):
#        for j, value in enumerate(row):
#            if value == "x":
#                continue
#            update = PanelUpdate(i, j, "#FFFFFF" if value == "alive" else "#000000")
#            updates.append(update)
#
#    nl.update(updates)


def update_game_panel(row, col, state, gameboard):
    # updates a single panel to the game logic
    gameboard[row][col] = state
    return gameboard


def grab_vert_states(row, col, gameboard):
    print(f"testing row: {row} and column {col}")
    print
    num_alive = 0
    if row == 5 or row == 6:
        if col == 22:
            max_right = 0
        if col == 21:
            max_right = 1
        if col == 0:
            max_left = 0
        if col == 1:
            max_left = -1
    else:
        max_right = 2
        max_left = -2
    for y in [max_left, 0, max_right]:  # looks at cells at the cells vertices
        for x in [-1, 0, 1]:
            if y != 0 and x != 0:  # checks that we arn't looking at the original cell
                if gameboard[row + x][col + y] == "alive":
                    num_alive += 1
    return num_alive  # returns how many cells are alive around that cell

    # fix it so it dosnt look past the variable values with x and y


def update_game_12(gameboard):
    for row_num in range(len(gameboard)):
        for col_num in range(
            len(gameboard[row_num])
        ):  # looks at every element in the rows and colums
            num_alive = grab_vert_states(row_num, col_num, gameboard)
            if gameboard[row_num][col_num] == "dead":
                if num_alive == 4:
                    gameboard[row_num][col_num] = "alive"
            if gameboard[row_num][col_num] == "alive":
                if num_alive <= 3:
                    gameboard[row_num][col_num] == "dead"
                if num_alive >= 6:
                    gameboard[row_num][col_num == "dead"]
    return gameboard


def create_rand_board(gameboard):
    cells_to_turn = random.randrange(100, 131)
    for i in range(0, cells_to_turn):
        good_cell = False
        while good_cell == False:
            turning_cell_row = random.randrange(0, 12)
            turning_cell_col = random.randrange(0, 23)
            if (
                gameboard[turning_cell_row][turning_cell_col] == "x"
                or gameboard[turning_cell_row][turning_cell_col] == "alive"
            ):
                good_cell = False
            else:
                good_cell = True
        update_game_panel(turning_cell_row, turning_cell_col, "alive", gameboard)
    return gameboard


def test_board(current_game):
    is_dead = False
    x = 0  # initialise the counter
    while x < 100 and is_dead == False:
        current_game = update_game_12(current_game)
        for row_num in range(len(current_game)):
            for col_num in range(len(current_game[row_num])):
                if current_game[row_num][col_num] == "alive":
                    is_dead = False
                    break
            if is_dead == False:
                break
        x += 1    
    if is_dead:
        return is_dead
    else:
        return True


test_gameboard = create_rand_board(dead_gameboard)
if test_board(test_gameboard):
    print("survived")
else:
    print("died")

#while test_board(current_board):
#    update_game_12(current_board)
#    update_panels(current_board)
#    print(current_board)
#    time.sleep(0.5)
