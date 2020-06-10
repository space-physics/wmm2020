#!/usr/bin/env python
import numpy as np
from matplotlib.pyplot import show
import argparse

import wmm2020 as wmm
import wmm2020.plots as plt


p = argparse.ArgumentParser()
p.add_argument("yeardec", help="decimal year e.g. 2020.62", type=float)
p.add_argument("alt_km", help="altitude (km) default: 0.", type=float, default=0.0)
P = p.parse_args()

lon, lat = np.meshgrid(np.arange(-180, 180 + 10, 10), np.arange(-90, 90 + 10, 10))

mag = wmm.wmm(lat, lon, P.alt_km, P.yeardec)

plt.plotwmm(mag)

show()
