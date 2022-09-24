import time

import data
from nanoleaf import Color, Nanoleaf, PanelUpdate

nl = Nanoleaf()


while True:
    for _, color in Color._member_map_.items():
        updates = [PanelUpdate(row, col, color, 10) for row, col in data.panel_positions[3]]
        nl.update(updates)
        time.sleep(1)
