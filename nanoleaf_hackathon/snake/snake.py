from collections import deque
from random import choice

from moves import Move, positions, valid_move_map


class Snake:
    def __init__(self):
        center = (5, 11)

        # Create queue representing snake's path and append starting tile
        self.snake: deque[tuple(int, int)] = deque(maxlen=216)
        self.snake.append(center)

        # Place starting food
        self._place_food()

    def make_move(self, move: Move):
        x, y = move.value
        head = self.snake[-1]
        new_head = (head[0] + y, head[1] + x)

        # Check if next move would move snake into walls
        if new_head not in valid_move_map[head]:
            self._game_over()
            return

        self.snake.append(new_head)  # Move head

        self._next_frame()

    def _next_frame(self):
        head = self.snake[-1]

        # Check if snake moved into itself
        if self.snake.count(head) > 1:
            self._game_over()
            return

        # Check if snake found food
        if head == self.food:
            self._place_food()
        elif len(self.snake) > 2:
            # Move tail if no food found and minimum length has been reached
            self.snake.popleft()

        self.display()

    def _place_food(self):
        # Get list of empty squares
        valid_squares = set(self.snake) ^ set(positions)

        # Select random square from list of empty squares
        self.food = choice(list(valid_squares))

    def _game_over(self):
        print(f"Game over! Your score was {len(self.snake) - 1}.")

    # def display(self):
    #     head = self.snake[-1]
    #     out = "|"
    #     out += "---" * self.size
    #     for y in range(0, self.size**2, self.size):
    #         out += "|\n|"
    #         for x in range(self.size):
    #             i = y + x
    #             if i == head:
    #                 out += " \u25A1 "
    #             elif i == self.food:
    #                 out += " \u2022 "
    #             elif i in self.snake:
    #                 out += " \u25A0 "
    #             else:
    #                 out += "   "
    #     out += "|\n|"
    #     out += "---" * self.size
    #     out += "|"
    #     print(out)
