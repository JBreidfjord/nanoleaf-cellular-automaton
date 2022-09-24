from dataclasses import dataclass


@dataclass
class Cell:
    row: int
    col: int
    alive: bool
    generation: int
