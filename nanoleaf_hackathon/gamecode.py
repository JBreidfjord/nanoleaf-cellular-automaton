
gamebord=[ #x means the tile does not exit, dead means the cell is dead and alive means it's fucking alive dibshit
    ['x','x','x','x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x','x','x','x'],
    ['x','x','x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x','x','x'],
    ['x','x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x','x'],
    ['x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x'],
    ['x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x'],
    ['dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead'],
    ['dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead'],
    ['x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x'],
    ['x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x'],
    ['x','x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x','x'],
    ['x','x','x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x','x','x'],
    ['x','x','x','x','x','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','dead','x','x','x','x','x'],
]

def update_game_panel(row, col, state):
    #updates a single panel to the game logic
    gamebord[row][col]=state



def grab_vert_states(row,col):
    num_alive = 0
    for y in [-1,0,1]: #looks at cells at the cells vertices
        for x in [-1,0,1]:
            if y != 0 and x != 0: #checks that we arn't looking at the original cell
                if gamebord[row+x][col+y] == 'alive': 
                    num_alive += 1
    return num_alive #returns how many cells are alive around that cell


def update_game_12():
    for row_num in range(len(gamebord)):
        for col_num in range(len(gamebord[row_num])):#looks at every element in the rows and colums 
            num_alive = grab_vert_states(row_num,col_num)
            if gamebord[row_num][col_num] == 'dead':
                if num_alive == 4:
                    gamebord[row_num][col_num] = 'alive'
            if gamebord[row_num][col_num] == 'alive':
                if num_alive <= 3:
                    gamebord[row_num][col_num] == 'dead'
                if num_alive >= 6:
                    gamebord[row_num][col_num == 'dead']
    return gamebord


