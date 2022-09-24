from enum import Enum

from nanoleaf_hackathon import data


# Move._member_names_ to get a list of names
class Move(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


positions: tuple[int, int] = []
for panels in data.panel_positions:
    positions.extend(panels)

valid_move_map = {}
for position in positions:
    possible_moves = []
    row, col = position
    upright = (row + col) % 2 != 0
    for move in Move:
        if (upright and move.name == "UP") or (not upright and move.name == "DOWN"):
            continue
        x, y = move.value
        new_position = (row + y, col + x)
        if new_position in positions:
            possible_moves.append(new_position)
    valid_move_map[position] = possible_moves
