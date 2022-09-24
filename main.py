from __future__ import annotations

import colorsys
import http.client as httplib
import json
import random
import socket
import time
from collections import deque
from dataclasses import dataclass
from enum import Enum


def hex_to_rgb(hex: str):
    hex = hex.replace("#", "")
    return tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: tuple[int, int, int]):
    r = max(min(rgb[0], 255), 0)
    g = max(min(rgb[1], 255), 0)
    b = max(min(rgb[2], 255), 0)
    return "#%02x%02x%02x" % (r, g, b)


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


positions: list[tuple[int, int]] = []
for panels in panel_positions:
    positions.extend(panels)

letter_G = [
    (3, 7),
    (2, 7),
    (2, 6),
    (2, 5),
    (2, 4),
    (2, 3),
    (3, 3),
    (3, 2),
    (4, 2),
    (4, 1),
    (5, 1),
    (5, 0),
    (6, 0),
    (6, 1),
    (6, 2),
    (6, 3),
    (6, 4),
    (6, 5),
    (6, 6),
    (5, 6),
    (5, 7),
    (4, 7),
    (4, 6),
    (4, 5),
    (4, 4),
]
letter_A = [
    (6, 7),
    (6, 8),
    (5, 8),
    (5, 9),
    (4, 9),
    (4, 10),
    (3, 10),
    (4, 11),
    (5, 11),
    (5, 12),
    (6, 12),
    (6, 13),
]
letter_M = [
    (6, 10),
    (5, 10),
    (4, 12),
    (3, 12),
    (3, 13),
    (3, 14),
    (4, 14),
    (4, 15),
    (4, 16),
    (3, 16),
    (3, 17),
    (3, 18),
    (4, 18),
    (4, 19),
    (5, 19),
    (5, 20),
    (6, 20),
]
letter_E = [
    (7, 17),
    (7, 16),
    (7, 15),
    (7, 14),
    (6, 15),
    (6, 16),
    (5, 16),
    (5, 17),
    (5, 18),
    (4, 17),
    (3, 19),
    (3, 20),
]
letter_O = [
    (5, 4),
    (5, 5),
    (4, 5),
    (4, 6),
    (4, 7),
    (4, 8),
    (4, 9),
    (5, 9),
    (5, 10),
    (6, 10),
    (6, 9),
    (7, 9),
    (7, 8),
    (7, 7),
    (7, 6),
    (7, 5),
    (6, 5),
    (6, 4),
]
letter_F = [
    (7, 12),
    (7, 13),
    (6, 13),
    (6, 14),
    (6, 15),
    (6, 16),
    (5, 14),
    (5, 15),
    (4, 15),
    (4, 16),
    (4, 17),
    (4, 18),
]
letter_L = [
    (3, 5),
    (3, 4),
    (4, 4),
    (4, 3),
    (5, 3),
    (5, 2),
    (6, 2),
    (6, 1),
    (7, 1),
    (7, 2),
    (7, 3),
    (7, 4),
    (7, 5),
]
letter_I = [
    (4, 7),
    (4, 8),
    (4, 9),
    (4, 10),
    (4, 11),
    (4, 12),
    (5, 9),
    (5, 8),
    (6, 8),
    (6, 7),
    (7, 7),
    (7, 6),
    (8, 8),
    (8, 7),
    (8, 6),
    (8, 5),
    (8, 4),
    (8, 3),
]
letter_F2 = [
    (7, 10),
    (7, 11),
    (6, 11),
    (6, 12),
    (5, 12),
    (5, 13),
    (5, 14),
    (5, 15),
    (4, 13),
    (4, 14),
    (3, 14),
    (3, 15),
    (3, 16),
    (3, 17),
]
letter_E2 = [
    (8, 18),
    (8, 17),
    (8, 16),
    (8, 15),
    (8, 14),
    (8, 13),
    (7, 14),
    (7, 15),
    (6, 15),
    (6, 16),
    (6, 17),
    (6, 18),
    (6, 19),
    (6, 20),
    (5, 16),
    (5, 17),
    (4, 17),
    (4, 18),
    (4, 19),
    (4, 20),
    (4, 21),
]

letter_gradients = {
    "G": [
        "#0006f8",
        "#381ef9",
        "#502efa",
        "#623cfb",
        "#7249fb",
        "#8055fc",
        "#8c61fd",
        "#976dfd",
        "#a279fe",
        "#ac85ff",
        "#b691ff",
        "#bf9dff",
        "#c8a9ff",
        "#d1b5ff",
        "#d9c1ff",
        "#e1ceff",
        "#e9daff",
        "#f0e6ff",
        "#f8f3ff",
        "#ffffff",
    ],
    "A": [
        "#f35742",
        "#f6614b",
        "#f86b54",
        "#fa755e",
        "#fd7e67",
        "#fe8771",
        "#ff907a",
        "#ff9984",
        "#ffa28e",
        "#ffaa98",
        "#ffb3a2",
        "#ffbbac",
        "#ffc4b6",
        "#ffccc0",
        "#ffd5ca",
        "#ffddd5",
        "#ffe6df",
        "#ffeeea",
        "#fff7f4",
        "#ffffff",
    ],
    "M": [
        "#22d751"
        "#3dda5b"
        "#4fdc64"
        "#5ede6e"
        "#6ce177"
        "#78e380"
        "#84e589"
        "#8fe892"
        "#99ea9b"
        "#a3eca4"
        "#adeead"
        "#b7f0b6"
        "#c0f2bf"
        "#c9f4c8"
        "#d3f6d1"
        "#dcf8da"
        "#e5fae4"
        "#edfced"
        "#f6fdf6"
        "#ffffff"
    ],
    "E": [
        "#fffb00",
        "#fffb2a",
        "#fffb3f",
        "#fffb4f",
        "#fffc5d",
        "#fffc6a",
        "#fffc76",
        "#fffc81",
        "#fffc8d",
        "#fffc98",
        "#fffda2",
        "#fffdad",
        "#fffdb7",
        "#fffdc2",
        "#fffecc",
        "#fffed6",
        "#fffee0",
        "#fffeeb",
        "#fffff5",
        "#ffffff",
    ],
    "O": [
        "#a200ff",
        "#a926ff",
        "#b03aff",
        "#b649ff",
        "#bd57ff",
        "#c264ff",
        "#c870ff",
        "#ce7cff",
        "#d387ff",
        "#d893ff",
        "#dc9eff",
        "#e1a9ff",
        "#e5b4ff",
        "#eabeff",
        "#eec9ff",
        "#f1d4ff",
        "#f5dfff",
        "#f9e9ff",
        "#fcf4ff",
        "#ffffff",
    ],
    "F": [
        "#a200ff",
        "#a926ff",
        "#b03aff",
        "#b649ff",
        "#bd57ff",
        "#c264ff",
        "#c870ff",
        "#ce7cff",
        "#d387ff",
        "#d893ff",
        "#dc9eff",
        "#e1a9ff",
        "#e5b4ff",
        "#eabeff",
        "#eec9ff",
        "#f1d4ff",
        "#f5dfff",
        "#f9e9ff",
        "#fcf4ff",
        "#ffffff",
    ],
    "I": [
        "#1200ff",
        "#3d1cff",
        "#552dff",
        "#663bff",
        "#7648ff",
        "#8355ff",
        "#8f61ff",
        "#9a6dff",
        "#a579ff",
        "#af85ff",
        "#b891ff",
        "#c19dff",
        "#caa9ff",
        "#d2b6ff",
        "#dac2ff",
        "#e2ceff",
        "#eadaff",
        "#f1e6ff",
        "#f8f3ff",
        "#ffffff",
    ],
    "E2": [
        "#1200ff",
        "#3d1cff",
        "#552dff",
        "#663bff",
        "#7648ff",
        "#8355ff",
        "#8f61ff",
        "#9a6dff",
        "#a579ff",
        "#af85ff",
        "#b891ff",
        "#c19dff",
        "#caa9ff",
        "#d2b6ff",
        "#dac2ff",
        "#e2ceff",
        "#eadaff",
        "#f1e6ff",
        "#f8f3ff",
        "#ffffff",
    ],
    "L": [
        "#ff0000",
        "#ff2b14",
        "#ff3f23",
        "#ff5030",
        "#ff5e3d",
        "#ff6b49",
        "#ff7756",
        "#ff8262",
        "#ff8e6e",
        "#ff997b",
        "#ffa388",
        "#ffae94",
        "#ffb8a1",
        "#ffc2ae",
        "#ffcdbb",
        "#ffd7c9",
        "#ffe1d6",
        "#ffebe4",
        "#fff5f1",
        "#ffffff",
    ],
    "F2": [
        "#ff0000",
        "#ff2b14",
        "#ff3f23",
        "#ff5030",
        "#ff5e3d",
        "#ff6b49",
        "#ff7756",
        "#ff8262",
        "#ff8e6e",
        "#ff997b",
        "#ffa388",
        "#ffae94",
        "#ffb8a1",
        "#ffc2ae",
        "#ffcdbb",
        "#ffd7c9",
        "#ffe1d6",
        "#ffebe4",
        "#fff5f1",
        "#ffffff",
    ],
}


def start_screen(tranz_time: int, wait_time: int, nl: Nanoleaf = None):
    updates = []
    board = {}
    for position in positions:
        color = "#FFFFFF"
        cell = Cell(position[0], position[1], alive=False, color=color)
        if position in letter_G:
            color = "#0006f8"
            cell.alive = True
            cell.start_letter = "G"
        elif position in letter_A:
            color = "#F35742"
            cell.alive = True
            cell.start_letter = "A"
        elif position in letter_M:
            color = "#22D751"
            cell.alive = True
            cell.start_letter = "M"
        elif position in letter_E:
            color = "#FFFB00"
            cell.alive = True
            cell.start_letter = "E"
        cell.color = color
        board[position] = cell
        updates.append(PanelUpdate(position[0], position[1], color, tranz_time))

    if nl is not None:
        nl.update(updates)
    print("waiting")
    time.sleep(wait_time)

    game = Game(nanoleaf=nl, version="12", start_board=board)
    game.run_board(limit=20)

    updates = []
    board = {}
    for position in positions:
        color = "#FFFFFF"
        cell = Cell(position[0], position[1], alive=False, color=color)
        if position in letter_O:
            color = "#A200FF"
            cell.alive = True
            cell.start_letter = "O"
        elif position in letter_F:
            color = "#A200FF"
            cell.alive = True
            cell.start_letter = "F"
        cell.color = color
        board[position] = cell
        updates.append(PanelUpdate(position[0], position[1], color, tranz_time))

    if nl is not None:
        nl.update(updates)
    print("waiting")
    time.sleep(wait_time)

    game = Game(nanoleaf=nl, version="12", start_board=board)
    game.run_board(limit=20)

    updates = []
    board = {}
    for position in positions:
        color = "#FFFFFF"
        cell = Cell(position[0], position[1], alive=False, color=color)
        if position in letter_L:
            color = "#FF0000"
            cell.start_letter = "L"
            cell.alive = True
        elif position in letter_I:
            color = "#1200FF"
            cell.start_letter = "I"
            cell.alive = True
        elif position in letter_F2:
            color = "#FF0000"
            cell.start_letter = "F2"
            cell.alive = True
        elif position in letter_E2:
            color = "#1200FF"
            cell.start_letter = "E2"
            cell.alive = True
        cell.color = color
        board[position] = cell
        updates.append(PanelUpdate(position[0], position[1], color, tranz_time))

    if nl is not None:
        nl.update(updates)
    print("waiting")
    time.sleep(wait_time)

    game = Game(nanoleaf=nl, version="12", start_board=board)
    game.run_board(limit=20)


colors = [
    "#0024ff",
    "#4d11f8",
    "#6c00f1",
    "#8300ea",
    "#9600e2",
    "#a500da",
    "#b300d2",
    "#c000c9",
    "#cb00c0",
    "#d400b7",
    "#dd00ae",
    "#e500a5",
    "#ec009c",
    "#f20093",
    "#f7008a",
    "#fb0081",
    "#ff0078",
    "#ff0070",
    "#ff0067",
    "#ff005f",
    "#ff0056",
    "#ff004e",
    "#ff0046",
    "#ff003e",
    "#ff0036",
    "#ff002e",
    "#ff0026",
    "#ff001c",
    "#ff0011",
    "#ff0000",
    "#ff0000",
    "#fc2c00",
    "#f94200",
    "#f55200",
    "#f06100",
    "#ea6e00",
    "#e37900",
    "#dc8400",
    "#d48f00",
    "#cb9800",
    "#c1a200",
    "#b7aa00",
    "#acb300",
    "#a0bb00",
    "#94c200",
    "#85c900",
    "#75d000",
    "#62d700",
    "#48de03",
    "#17e42f",
    "#17e42f",
    "#38e42a",
    "#4be425",
    "#5be520",
    "#68e51a",
    "#74e515",
    "#7ee50f",
    "#88e508",
    "#92e502",
    "#9ae500",
    "#a3e400",
    "#abe400",
    "#b3e400",
    "#bbe400",
    "#c2e400",
    "#c9e300",
    "#d0e304",
    "#d7e30b",
    "#dee211",
    "#e4e217",
    "#e4e217",
    "#efd800",
    "#f9cd00",
    "#ffc100",
    "#ffb600",
    "#ffaa08",
    "#ff9e1a",
    "#ff9128",
    "#ff8434",
    "#ff763f",
    "#ff694a",
    "#ff5b55",
    "#ff4d60",
    "#ff3e6b",
    "#ff3076",
    "#ff2282",
    "#ff168d",
    "#fe0e98",
    "#f20fa3",
    "#e417ad",
    "#e417ad",
    "#dc30ba",
    "#d241c6",
    "#c84ed0",
    "#bd5ada",
    "#b164e2",
    "#a46ee9",
    "#9676ef",
    "#887df3",
    "#7984f7",
    "#6a8bf9",
    "#5a91fa",
    "#4a96fa",
    "#399bf9",
    "#279ff7",
    "#12a4f4",
    "#00a7f1",
    "#00abed",
    "#00aee9",
    "#17b1e4",
    "#17b1e4",
    "#28aeea",
    "#3da9ef",
    "#53a5f3",
    "#699ff4",
    "#7e99f3",
    "#9392f0",
    "#a68aea",
    "#b982e2",
    "#c979d7",
    "#d870ca",
    "#e466bb",
    "#ee5eaa",
    "#f65698",
    "#fa5184",
    "#fb4e70",
    "#fa4f5c",
    "#f55347",
    "#ee5932",
    "#e46017",
]


class Adjacent(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


neighbour_map = {}
for position in positions:
    neighbours = []
    row, col = position
    upright = (row + col) % 2 != 0
    for adjacent in Adjacent:
        if (upright and adjacent.name == "UP") or (not upright and adjacent.name == "DOWN"):
            continue
        x, y = adjacent.value
        new_position = (row + y, col + x)
        if new_position in positions:
            neighbours.append(new_position)
    neighbour_map[position] = neighbours


twelve_adjacent_downright = [
    # 5,11
    (0, -1),  # 5,10
    (-1, 0),  # 4,11
    (0, 1),  # 5,12
    (0, 2),  # 5,13
    (0, -2),  # 5,9
    (-1, -1),  # 4,10
    (-1, 1),  # 4,12
    (-1, -2),  # 4,9
    (-1, 2),  # 4,13
    (1, 1),  # 6,12
    (1, 0),  # 6,11
    (1, -1),  # 6,10
]
twelve_adjacent_upright = [
    # 4,11
    (0, -1),  # 4,10
    (0, 1),  # 4,12
    (-1, -1),  # 3,10
    (-1, 0),  # 3,11
    (-1, 1),  # 3,12
    (0, 2),  # 4,13
    (1, 2),  # 5,13
    (1, 1),  # 5,12
    (1, 0),  # 5,11
    (1, -1),  # 5,10
    (1, -2),  # 5,9
    (0, -2),  # 4,9
]
twelve_neighbour_map: dict[tuple[int, int], list[tuple[int, int]]] = {}
# Calculate 12-neighbourhood
for position in positions:
    neighbours = []
    row, col = position
    upright = (row + col) % 2 != 0
    adjacent_array = twelve_adjacent_upright if upright else twelve_adjacent_downright
    for adjacent in adjacent_array:
        x, y = adjacent
        new_position = (row + y, col + x)
        if new_position in positions:
            neighbours.append(new_position)
    twelve_neighbour_map[position] = neighbours


@dataclass
class Cell:
    row: int
    col: int
    alive: bool
    gen: int = 0
    color: str = "#FFFFFF"
    born_gen: int = 0
    start_letter: str = None


class Game:
    dead_board = {(row, col): Cell(row, col, alive=False) for row, col in positions}

    def __init__(
        self,
        version: str = "3",
        start_board: dict[tuple[int, int], Cell] = None,
        initial_cells: int = 100,
        transition_time: int = 5,
        nanoleaf: Nanoleaf = None,
    ):
        self.twelve = version == "12"
        self.initial_cells = initial_cells
        self.nl = nanoleaf
        self.transition_time = transition_time
        if self.nl is not None:
            self.nl = Nanoleaf(demo_mode=False)
            self.nl.update([PanelUpdate(row, col, "#FFFFFF") for row, col in positions])

        self.board = self.initialize_board() if start_board is None else start_board

    def run_board(self, limit: int = 1000):
        i = 0
        while not self._is_dead_board(self.board):
            print(f"Generation {i}")
            self.board = self.update_12(gen=i) if self.twelve else self.update(gen=i)
            self.update_panels()
            if i > limit:
                break
            time.sleep(0.5)
            i += 1

    def initialize_board(self):
        while True:
            board_history = deque(maxlen=15)
            original_board = self._random_board()
            board = original_board.copy()
            for i in range(self.initial_cells):
                board_history.append(board.copy())
                board = self.update_12(board=board) if self.twelve else self.update(board=board)
                for hist_board in board_history:
                    if self.board_eq(board, hist_board):
                        break
                if self._is_dead_board(board):
                    break
            if not self._is_dead_board(board) and not board in board_history:
                return original_board

    def _is_dead_board(self, board: dict[tuple[int, int], Cell]):
        return self.board_eq(board, self.dead_board)

    def board_eq(self, board1: dict[tuple[int, int], Cell], board2: dict[tuple[int, int], Cell]):
        for cell1, cell2 in zip(board1.values(), board2.values()):
            if (
                cell1.alive != cell2.alive
                or cell1.gen != cell2.gen
                or cell1.row != cell2.row
                or cell1.col != cell2.col
            ):
                return False
        return True

    def _random_board(self):
        living_cell_positions = random.sample(positions, 100)
        board = self.dead_board.copy()
        for position in living_cell_positions:
            board[position] = Cell(*position, alive=True)
        return board

    def update(self, gen: int = 0, board: dict[tuple[int, int], Cell] = None):
        board = board if board is not None else self.board
        orig_board = board.copy()

        for (row, col), cell in board.items():
            num_alive_neighbours = len(
                [
                    neighbour
                    for neighbour in neighbour_map[(row, col)]
                    if orig_board[neighbour].alive
                ]
            )
            if cell.alive:
                # Under / Overpopulation
                if num_alive_neighbours == 0 or num_alive_neighbours == 3:
                    board[(row, col)] = Cell(row, col, alive=False, gen=0)
                elif num_alive_neighbours == 2:
                    board[(row, col)] = Cell(row, col, alive=True, gen=cell.gen + 1)
            # Cell comes alive with exactly 2 neighbours
            elif num_alive_neighbours == 2:
                board[(row, col)] = Cell(row, col, alive=True, gen=cell.gen + 1, born_gen=gen)

        return board

    def update_12(self, gen: int = 0, board: dict[tuple[int, int], Cell] = None):
        board = board if board is not None else self.board
        orig_board = board.copy()

        for (row, col), cell in board.items():
            alive_neighbours = [
                neighbour
                for neighbour in twelve_neighbour_map[(row, col)]
                if orig_board[neighbour].alive
            ]
            num_alive_neighbours = len(alive_neighbours)
            if cell.alive:
                # Under / Overpopulation
                if 0 <= num_alive_neighbours <= 3 or 7 <= num_alive_neighbours <= 12:
                    board[(row, col)] = Cell(row, col, alive=False, gen=0)
                elif 4 <= num_alive_neighbours <= 6:
                    board[(row, col)] = Cell(
                        row, col, alive=True, gen=cell.gen + 1, start_letter=cell.start_letter
                    )
            # Cell comes alive with exactly 4/5 neighbours
            elif num_alive_neighbours == 4 or num_alive_neighbours == 5:
                letters = [
                    orig_board[neighbour].start_letter
                    for neighbour in alive_neighbours
                    if orig_board[neighbour].start_letter is not None
                ]
                if len(letters) > 0:
                    start_letter = random.choice(letters)
                else:
                    start_letter = None
                board[(row, col)] = Cell(
                    row, col, alive=True, gen=cell.gen + 1, born_gen=gen, start_letter=start_letter
                )

        return board

    def update_panels(self):
        updates = []
        for (row, col), cell in self.board.items():
            if cell.alive:
                color = colors[min(cell.born_gen + cell.gen, len(colors) - 1)]
                if cell.start_letter is not None:
                    color = letter_gradients[cell.start_letter][
                        min(cell.gen, len(letter_gradients[cell.start_letter]) - 1)
                    ]
                updates.append(PanelUpdate(row, col, color, self.transition_time))
                cell.color = color
                self.board[(row, col)] = cell

        for (row, col), cell in self.board.items():
            if not cell.alive:
                neighbour_colors = [
                    hex_to_rgb(self.board[cell].color)
                    for cell in twelve_neighbour_map[(row, col)]
                    if self.board[cell].alive
                ]
                if len(neighbour_colors) > 0:
                    color = tuple(
                        int(sum([color[i] for color in neighbour_colors]) / len(neighbour_colors))
                        for i in range(3)
                    )
                    color = colorsys.rgb_to_hls(*color)
                    # Increase lightness 50%
                    color = colorsys.hls_to_rgb(color[0], color[1] * 1.5, color[2])
                    color = tuple(int(c) for c in color)
                    color = rgb_to_hex(color)
                else:
                    color = "#FFFFFF"

                cell.color = color
                self.board[(row, col)] = cell
                updates.append(PanelUpdate(row, col, color, self.transition_time))

        # for (row, col), cell in self.board.items():
        #     if cell.color == "#FFFFFF":
        #         neighbour_colors = [
        #             hex_to_rgb(self.board[cell].color) for cell in twelve_neighbour_map[(row, col)]
        #         ]
        #         color = rgb_to_hex(
        #             tuple(
        #                 int(sum([color[i] for color in neighbour_colors]) / len(neighbour_colors))
        #                 for i in range(3)
        #             )
        #         )
        #         cell.color = color
        #         self.board[(row, col)] = cell
        #         updates.append(PanelUpdate(row, col, color, self.transition_time))

        if self.nl is not None:
            self.nl.update(updates)


if __name__ == "__main__":
    nl = None
    # nl = Nanoleaf(demo_mode=False)

    while True:
        start_screen(5, 3, nl)
        game = Game(version="12", nanoleaf=nl, initial_cells=100, transition_time=5)
        game.run_board(limit=100)
