import random
import time

import data
from nanoleaf import Nanoleaf, PanelUpdate

nl = Nanoleaf()

# random hex colors
colors = ["#92ac1d", "#58f982", "#bf6070", "#0eff1f", "#8d2b5d", "#db684c"]


while True:
    updates = [
        PanelUpdate(row, col, random.choice(colors), 10) for row, col in data.panel_positions[3]
    ]
    nl.update(updates)
    time.sleep(1)
