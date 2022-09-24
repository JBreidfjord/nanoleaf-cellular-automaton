import random
dead_gameboard=[ #x means the tile does not exit, dead means the cell is dead and alive means it's fucking alive dibshit
    ['x','x','x','x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x','x','x','x'],
    ['x','x','x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x','x','x'],
    ['x','x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x','x'],
    ['x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x'],
    ['x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x'],
    ['dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead'],
    ['dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead'],
    ['x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x'],
    ['x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x'],
    ['x','x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x','x'],
    ['x','x','x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x','x','x'],
    ['x','x','x','x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x','x','x','x'],
]

def update_game_panel(row, col, state, gameboard):
    #updates a single panel to the game logic
    gameboard[row][col]=state
    return gameboard

def grab_vert_states(row,col,gameboard):
    num_alive = 0
    for y in [-2,0,2]: #looks at cells at the cells vertices
        for x in [-1,0,1]:
            if y != 0 and x != 0: #checks that we arn't looking at the original cell
                if gameboard[row+x][col+y] == 'alive': 
                    num_alive += 1
    return num_alive #returns how many cells are alive around that cell

    #fix it so it dosnt look past the vailable values with x and y


def update_game_12(gameboard):
    for row_num in range(len(gameboard)):
        for col_num in range(len(gameboard[row_num])):#looks at every element in the rows and colums 
            num_alive = grab_vert_states(row_num,col_num,gameboard)
            if gameboard[row_num][col_num] == 'dead':
                if num_alive == 4:
                    gameboard[row_num][col_num] = 'alive'
            if gameboard[row_num][col_num] == 'alive':
                if num_alive <= 3:
                    gameboard[row_num][col_num] == 'dead'
                if num_alive >= 6:
                    gameboard[row_num][col_num == 'dead']
    return gameboard


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
    return gameboard


def test_board(current_game):
    is_dead=False
    x=0 #initialise the counter
    while x < 100 and is_dead == False:
        current_game = update_game_12(current_game)
        for row_num in range(len(current_game)):
            for col_num in range(len(current_game[row_num])):
                if current_game[row_num][col_num] == 'alive':
                    is_dead = False
                    break
            if is_dead == False:
                break
    if is_dead:
        return is_dead
    else:
        return True

current_board = create_rand_board(dead_gameboard)
while test_board(current_board) != True:
    current_board = create_rand_board(dead_gameboard)

while test_board(current_board):
    update_game_12(current_board)
    print(current_board)
    input('')
