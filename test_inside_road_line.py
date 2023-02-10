import pandas as pd
import numpy as np
from matplotlib import path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from time import sleep
import airsim

road_line = pd.read_csv('roads\\train\\2023-02-10-18-57-33.csv')
xl, yl, xr, yr = road_line['xl'], road_line['yl'], road_line['xr'], road_line['yr']

x_upper_limit = max(max(xl), max(xr)) + 5
x_lower_limit = min(min(xl), min(xr)) - 5
y_upper_limit = max(max(yl), max(yr)) + 5
y_lower_limit = min(min(yl), min(yr)) - 5

p = path.Path(list(zip(xl, yl))+list(zip(xr,yr))[::-1])

car = airsim.CarClient(ip='127.0.0.1')
i = 0
tr_x_in = []
tr_y_in = []
tr_x_out = []
tr_y_out = []

while i < 100:
    i += 1

    car_state = car.getCarState()
    x, y, _ = car_state.kinematics_estimated.position
    is_inside = p.contains_point((x,y))
    if is_inside:
        tr_x_in.append(x)
        tr_y_in.append(y)
    else:
        tr_x_out.append(x)
        tr_y_out.append(y)
    print(is_inside)
    sleep(0.1)

fig, ax = plt.subplots()
patch = patches.PathPatch(p,color=None)
ax.add_patch(patch)
ax.scatter(tr_x_in, tr_y_in,color='red')
ax.scatter(tr_x_out, tr_y_out,color='black')

ax.set_xlim(x_lower_limit, x_upper_limit)
ax.set_ylim(y_lower_limit, y_upper_limit)
# print(p.contains_points([(125,-45)]))
plt.show()