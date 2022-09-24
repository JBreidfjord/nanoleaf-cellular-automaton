from __future__ import annotations

import http.client as httplib
import json
import random
import socket
import time
from dataclasses import dataclass
from enum import Enum


def hex_to_rgb(hex: str):
    hex = hex.replace("#", "")
    return tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))


panel_positions: list[list[tuple[int, int]]] = [
    [
        # Controller 0
        (1, 4),
        (1, 5),
        (1, 6),
        (1, 7),
        (1, 8),
        (1, 9),
        (1, 10),
        (1, 11),
        (1, 12),
        (1, 13),
        (1, 14),
        (1, 15),
        (1, 16),
        (1, 17),
        (0, 17),
        (0, 16),
        (0, 15),
        (0, 14),
        (0, 13),
        (0, 12),
        (0, 11),
        (0, 10),
        (0, 9),
        (0, 8),
        (0, 7),
        (0, 6),
        (0, 5),
        (1, 18),
    ],
    [
        # Controller 1
        (2, 3),
        (2, 4),
        (2, 5),
        (2, 6),
        (2, 7),
        (2, 8),
        (2, 9),
        (2, 10),
        (2, 11),
        (2, 12),
        (2, 13),
        (2, 14),
        (2, 15),
        (2, 16),
        (2, 17),
        (2, 18),
        (2, 19),
    ],
    [
        # Controller 2
        (3, 2),
        (3, 3),
        (3, 4),
        (3, 5),
        (3, 6),
        (3, 7),
        (3, 8),
        (3, 9),
        (3, 10),
        (3, 11),
        (3, 12),
        (3, 13),
        (3, 14),
        (3, 15),
        (3, 16),
        (3, 17),
        (3, 18),
        (3, 19),
        (3, 20),
    ],
    [
        # Controller 3
        (4, 1),
        (4, 2),
        (4, 3),
        (4, 4),
        (4, 5),
        (4, 6),
        (4, 7),
        (4, 8),
        (4, 9),
        (4, 10),
        (4, 11),
        (4, 12),
        (4, 13),
        (4, 14),
        (4, 15),
        (4, 16),
        (4, 17),
        (4, 18),
        (4, 19),
        (4, 20),
        (4, 21),
    ],
    [
        # Controller 4
        (5, 0),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5),
        (5, 6),
        (5, 7),
        (5, 8),
        (5, 9),
        (5, 10),
        (5, 11),
        (5, 12),
        (5, 13),
        (5, 14),
        (5, 15),
        (5, 16),
        (5, 17),
        (5, 18),
        (5, 19),
        (5, 20),
        (5, 21),
        (5, 22),
    ],
    [
        # Controller 5
        (6, 0),
        (6, 1),
        (6, 2),
        (6, 3),
        (6, 4),
        (6, 5),
        (6, 6),
        (6, 7),
        (6, 8),
        (6, 9),
        (6, 10),
        (6, 11),
        (6, 12),
        (6, 13),
        (6, 14),
        (6, 15),
        (6, 16),
        (6, 17),
        (6, 18),
        (6, 19),
        (6, 20),
        (6, 21),
        (6, 22),
    ],
    [
        # Controller 6
        (7, 1),
        (7, 2),
        (7, 3),
        (7, 4),
        (7, 5),
        (7, 6),
        (7, 7),
        (7, 8),
        (7, 9),
        (7, 10),
        (7, 11),
        (7, 12),
        (7, 13),
        (7, 14),
        (7, 15),
        (7, 16),
        (7, 17),
        (7, 18),
        (7, 19),
        (7, 20),
        (7, 21),
    ],
    [
        # Controller 7
        (8, 2),
        (8, 3),
        (8, 4),
        (8, 5),
        (8, 6),
        (8, 7),
        (8, 8),
        (8, 9),
        (8, 10),
        (8, 11),
        (8, 12),
        (8, 13),
        (8, 14),
        (8, 15),
        (8, 16),
        (8, 17),
        (8, 18),
        (8, 19),
        (8, 20),
    ],
    [
        # Controller 8
        (9, 3),
        (9, 4),
        (9, 5),
        (9, 6),
        (9, 7),
        (9, 8),
        (9, 9),
        (9, 10),
        (9, 11),
        (9, 12),
        (9, 13),
        (9, 14),
        (9, 15),
        (9, 16),
        (9, 17),
        (9, 18),
        (9, 19),
    ],
    [
        # Controller 9
        (10, 4),
        (10, 5),
        (10, 6),
        (10, 7),
        (10, 8),
        (10, 9),
        (10, 10),
        (10, 11),
        (10, 12),
        (10, 13),
        (10, 14),
        (10, 15),
        (10, 16),
        (10, 17),
        (11, 17),
        (11, 16),
        (11, 15),
        (11, 14),
        (11, 13),
        (11, 12),
        (11, 11),
        (11, 10),
        (11, 9),
        (11, 8),
        (11, 7),
        (11, 6),
        (11, 5),
        (10, 18),
    ],
]


class Color(Enum):
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    ORANGE = (255, 127, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


@dataclass
class PanelUpdate:
    row: int
    col: int
    color: str
    transition_time: int = 1


@dataclass
class Position:
    row: int
    col: int
    controller_id: int
    panel_id: int


@dataclass
class PhysicalPosition:
    panelId: int
    x: int
    y: int
    o: int  # 0, 180, or 360


@dataclass
class Frame:
    panel_id: int
    red: int
    green: int
    blue: int
    transition_time: int


class Nanoleaf:
    _API_PORT = 16021
    _API_BASE = "api/v1"
    _SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _SOCK_PORT = 60221
    IPS = [
        "192.168.1.14",
        "192.168.1.13",
        "192.168.1.12",
        "192.168.1.10",
        "192.168.1.11",
        "192.168.1.9",
        "192.168.1.4",
        "192.168.1.5",
        "192.168.1.3",
        "192.168.1.2",
    ]
    AUTH_CODES = [
        "4xjvV9IJAQDq83SFaROVVzvble3vHwV8",
        "LlBI3Odz7EOHR3v5TPwh4fDbGrFuKSq7",
        "WKiepsgP7vhnfI4zGBmxVH26Rq6KNFgg",
        "28vOnfDhQZXeShXjGKWocxHZJUe9NCwn",
        "vioLVKiV1IgfsAA94JFFBTFy0vEUG48K",
        "UY3DEDumg19xCnwrNV4Btm2FPF0CAhdO",
        "0AJgQMml89aa12iAYpAqEoWKrKW18JZa",
        "5EpekYkcVupgIjXM37bRsNG0pE38NfGC",
        "cSTCTsuAgBRC7i8F3ug1cc1Z1smDyPQH",
        "kAbYywuZWBWsMrFsOluxbnqAXEQqyMKr",
    ]

    def __init__(self, demo_mode: bool = True):
        if demo_mode:
            panels = self._initialize_controller(self.IPS[3], self.AUTH_CODES[3])
            self._panel_position_map: dict[tuple[int, int], Position] = {}
            for j, panel in enumerate(panels):
                row, col = panel_positions[3][j]
                self._panel_position_map[(row, col)] = Position(
                    row=row,
                    col=col,
                    controller_id=3,
                    panel_id=panel["panelId"],
                )
        else:
            controller_data = [
                self._initialize_controller(ip, auth) for ip, auth in zip(self.IPS, self.AUTH_CODES)
            ]
            self._map_panel_positions(controller_data)

    def _request(self, mode: str, ip: str, auth: str, endpoint: str, data: dict = None):
        LISTENER = ip + ":" + str(self._API_PORT)
        try:
            conn = httplib.HTTPConnection(LISTENER)
            if data is not None:
                conn.request(
                    mode,
                    "/api/v1/" + auth + "/" + endpoint,
                    json.dumps(data),
                    {"Content-Type": "application/json"},
                )
            else:
                conn.request(mode, "/api/v1/" + auth + "/" + endpoint)
            response = conn.getresponse()
            body = response.read()
            if len(body) != 0:
                body = json.loads(body)
            return body

        except (httplib.HTTPException, socket.error) as ex:
            print(f"Error: {ex}")

    def _format_api_url(self, ip: str, auth: str, endpoint: str) -> str:
        return f"https://{ip}:{self._API_PORT}/{self._API_BASE}/{auth}/{endpoint}"

    def _initialize_controller(self, ip: str, auth: str) -> list[PhysicalPosition]:
        """
        Initializes the controller and returns the position data.
        """
        self._set_stream_control_mode(ip, auth)
        return self._get_device_data(ip, auth)["panelLayout"]["layout"]["positionData"]

    def _set_stream_control_mode(self, ip: str, auth: str, version: int = 1):
        """
        Set the stream control mode to external control.
        """
        body = {
            "write": {
                "command": "display",
                "animType": "extControl",
                "extControlVersion": "v" + str(version),
            }
        }
        self._request("PUT", ip, auth, "effects", body)

    def _get_device_data(self, ip: str, auth: str) -> dict:
        """
        Gets panel info from the Nanoleaf controller.
        """
        return self._request("GET", ip, auth, "")

    def _send_stream_control_frames(self, frames: list[Frame], ip: str):
        """
        Sends a list of frames to the Nanoleaf controller.
        """
        stream = bytearray()
        # & 0xFF is used to convert the int to a byte
        stream.append(len(frames) & 0xFF)
        for frame in frames:
            stream.append(frame.panel_id & 0xFF)
            stream.append(1 & 0xFF)
            stream.append(frame.red & 0xFF)
            stream.append(frame.green & 0xFF)
            stream.append(frame.blue & 0xFF)
            stream.append(0 & 0xFF)
            stream.append(frame.transition_time & 0xFF)

        self._SOCK.sendto(stream, (ip, self._SOCK_PORT))

    def _map_panel_positions(self, controller_data: list[list[PhysicalPosition]]):
        """
        Creates a map of (row, col) values to Position objects based on the PhysicalPosition data.
        """
        self._panel_position_map: dict[tuple[int, int], Position] = {}
        for i, panels in enumerate(controller_data):
            for j, panel in enumerate(panels):
                row, col = panel_positions[i][j]
                self._panel_position_map[(row, col)] = Position(
                    row=row,
                    col=col,
                    controller_id=i,
                    panel_id=panel["panelId"],
                )

    def update(self, updates: list[PanelUpdate]):
        """
        Updates the display based on a list of updates.
        Panels not included will remain unchanged.
        """
        controller_frames = {i: [] for i in range(len(self.IPS))}
        for update in updates:
            position = self._panel_position_map[(update.row, update.col)]
            red, green, blue = hex_to_rgb(update.color)
            frame = Frame(
                panel_id=position.panel_id,
                red=red,
                green=green,
                blue=blue,
                transition_time=update.transition_time,
            )
            controller_frames[position.controller_id].append(frame)

        for controller_id, frames in controller_frames.items():
            self._send_stream_control_frames(frames, self.IPS[controller_id])


# nl = Nanoleaf(demo_mode=False)


# # random hex colors
# colors = ["#92ac1d", "#58f982", "#bf6070", "#0eff1f", "#8d2b5d", "#db684c", "#FFFFFF"]


positions: list[tuple[int, int]] = []
for panels in panel_positions:
    positions.extend(panels)
# updates = [PanelUpdate(row, col, "#000000") for row, col in positions]
# nl.update(updates)

# while True:
#     color = random.choice(colors)
#     panel = random.choice(positions)
#     nl.update([PanelUpdate(panel[0], panel[1], color)])
#     time.sleep(0.1)
#     nl.update([PanelUpdate(panel[0], panel[1], "#000000")])


class Adjacent(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


neighbour_map = {}
for position in positions:
    possible_moves = []
    row, col = position
    upright = (row + col) % 2 != 0
    for adjacent in Adjacent:
        if (upright and adjacent.name == "UP") or (not upright and adjacent.name == "DOWN"):
            continue
        x, y = adjacent.value
        new_position = (row + y, col + x)
        if new_position in positions:
            possible_moves.append(new_position)
    neighbour_map[position] = possible_moves


@dataclass
class Cell:
    row: int
    col: int
    alive: bool
    gen: int = 0


class Game:
    dead_board = {(row, col): Cell(row, col, alive=False) for row, col in positions}

    def __init__(self):
        self.nl = Nanoleaf(demo_mode=False)
        self.nl.update([PanelUpdate(row, col, "#000000") for row, col in positions])
        self.board = self.initialize_board()

        # self.run_board()

        # if loop:
        #     while True:
        #         self.board = self.initialize_board()
        #         self.run_board()

    def run_board(self):
        while not self._is_dead_board(self.board):
            self.board = self.update()
            # self.update_panels()
            print(self.board)
            time.sleep(0.5)

    def initialize_board(self):
        while True:
            board = self._random_board()
            for _ in range(100):
                board = self.update(board)
                if self._is_dead_board(board):
                    break
            if not self._is_dead_board(board):
                return board  # Made it at least 100 generations

    def _is_dead_board(self, board: dict[tuple[int, int], Cell]):
        return self.dead_board == board

    def _random_board(self):
        living_cells = random.randrange(100, 131)
        living_cell_positions = random.sample(positions, living_cells)
        board = self.dead_board.copy()
        for position in living_cell_positions:
            board[position] = Cell(*position, alive=True)
        return board

    def update(self, board: dict[tuple[int, int], Cell] = None):
        board = board if board is not None else self.board

        for (row, col), cell in board.items():
            num_alive_neighbours = len(
                [neighbour for neighbour in neighbour_map[(row, col)] if board[neighbour].alive]
            )
            if cell.alive:
                # Under / Overpopulation
                if num_alive_neighbours == 0 or num_alive_neighbours == 3:
                    board[(row, col)] = Cell(row, col, alive=False, gen=cell.gen + 1)
                elif num_alive_neighbours == 2:
                    board[(row, col)] = Cell(row, col, alive=True, gen=cell.gen + 1)
            # Cell comes alive with exactly 2 neighbours
            elif num_alive_neighbours == 2:
                board[(row, col)] = Cell(row, col, alive=True, gen=cell.gen + 1)

        return board

    def update_panels(self):
        updates = []
        for (row, col), cell in self.board.items():
            if cell.alive:
                updates.append(PanelUpdate(row, col, "#FFFFFF", 5))
            else:
                updates.append(PanelUpdate(row, col, "#000000", 5))

        self.nl.update(updates)


if __name__ == "__main__":
    game = Game()
    game.run_board()
