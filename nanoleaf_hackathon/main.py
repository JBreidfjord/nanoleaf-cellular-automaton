import random
import time

import data
from nanoleaf import Nanoleaf, PanelUpdate

nl = Nanoleaf(demo_mode=False)

# random hex colors
colors = ["#92ac1d", "#58f982", "#bf6070", "#0eff1f", "#8d2b5d", "#db684c", "#FFFFFF"]


updates = [PanelUpdate(row, col, "#000000") for row, col in data.panel_positions[3]]
nl.update(updates)

while True:
    color = random.choice(colors)
    nl.update([PanelUpdate(4, 1, color)])
    for i in range(21):
        original = updates[i]
        updates[i] = PanelUpdate(original.row, original.col, color)
        nl.update(updates)
        updates[i] = original
        time.sleep(0.2)

    color = random.choice(colors)
    nl.update([PanelUpdate(4, 21, color)])
    for i in range(21, 0, -1):
        i -= 1
        original = updates[i]
        updates[i] = PanelUpdate(original.row, original.col, color)
        nl.update(updates)
        updates[i] = original
        time.sleep(0.2)
