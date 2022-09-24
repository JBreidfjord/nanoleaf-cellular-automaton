from gamecode import update_game12

def test_board(current_game):
    x=0 #initialise the counter
    while x < 100 and is_dead == False:
        current_game = update_game12(current_game)
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