import glob
import os
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from scipy import interpolate
def dist(x, y):
    x = np.array(x)
    y = np.array(y)
    return np.norm(y-x)

# def extend(xs): 
#     # extends x in the following sense (only for integers):
#     # [1,2,5] -> [1,2,3,4,5]
#     # [-1,2,3,6,5,4,1,-1] -> [-1,0,1,2,3,4,5,6,5,4,3,2,1,0,-1]
#     extended = []
#     m = xs[0]
#     for x in xs:
#         if x == m:
#             extended.append(x)
#             continue
#         while x >= m + 1:
#             m+=1
#             extended.append(m)
#         while x < m:
#             m-=1
#             extended.append(m)
#         m = x
#     return extended

list_of_files = glob.glob('C:\\Users\\stepa\\Documents\\AirSim\\*')
latest_record = max(list_of_files, key=os.path.getctime) + '\\airsim_rec.txt'

route_record = pd.read_csv(latest_record, sep='\t')[['POS_X','POS_Y']].rename(columns={'POS_X':'x', 'POS_Y':'y'})
route_record = route_record.round(2).drop_duplicates()

# psint(new_record)
print(route_record)

# """
# route_record['y'] = np.interp(np.linspace(-5,80,100),route_record['x'],route_record['y'])
# route_record['x'] = np.linspace()
# route_record['prev_x'] = route_record['x'].shift(1)
# route_record['prev_y'] = route_record['y'].shift(1)
# route_record = route_record.drop(0)
line_width = 3
# route_record['left_road_line'] = ...
# route_record['right_road_line'] = ...

def calc_road_lines(a, b,h=line_width):
    x1, y1 = a
    x2, y2 = b

    alpha = np.arctan(abs(y2-y1)/abs(x2-x1))
    if x2 - x1 > 0:
        if y2 - y1 > 0:
            xl = x2 - (h/2)*np.sin(alpha)
            yl = y2 + (h/2)*np.cos(alpha)
            
            xr = x2 + (h/2)*np.sin(alpha)
            yr = y2 - (h/2)*np.cos(alpha)
        else:
            xl = x2 + (h/2)*np.sin(alpha)
            yl = y2 + (h/2)*np.cos(alpha)
            
            xr = x2 - (h/2)*np.sin(alpha)
            yr = y2 - (h/2)*np.cos(alpha)
    else:
        if y2 - y1 > 0:
            xl = x2 - (h/2)*np.sin(alpha)
            yl = y2 - (h/2)*np.cos(alpha)
            
            xr = x2 + (h/2)*np.sin(alpha)
            yr = y2 + (h/2)*np.cos(alpha)
        else:
            xl = x2 + (h/2)*np.sin(alpha)
            yl = y2 - (h/2)*np.cos(alpha)
            
            xr = x2 - (h/2)*np.sin(alpha)
            yr = y2 + (h/2)*np.cos(alpha)

    
    return (xl, yl), (xr, yr)


def get_lanes(x,y,h=3,show=False):
    dots = list(zip(x,y))
    road_left = []
    road_right = []
    for i in range(1,len(dots)):
        left, right = calc_road_lines(dots[i-1], dots[i],h=h)
        road_left.append(left)
        road_right.append(right)

    get_line = lambda road_line,i : np.array(list(map(lambda x: x[i],road_line)))

    xr = get_line(road_right,0)
    yr = get_line(road_right,1)

    xl = get_line(road_left,0)
    yl = get_line(road_left,1)
    if show:
        plt.plot(xr,yr,'.-',label='right_lane')
        plt.plot(xl,yl,'.-',label='left_lane')
        plt.plot(x,y,'.-',label='center')
        plt.legend()
        plt.show()
    return xl,yl,xr,yr


x = np.array(route_record['x'])
y = np.array(route_record['y'])

xl,yl,xr,yr = get_lanes(x,y, show=False)
x_upper_limit = max(max(xl), max(xr)) + 5
x_lower_limit = min(min(xl), min(xr)) - 5
y_upper_limit = max(max(yl), max(yr)) + 5
y_lower_limit = min(min(yl), min(yr)) - 5

x_space = np.linspace(x_lower_limit, x_upper_limit, 50)
y_space = np.linspace(y_lower_limit, y_upper_limit, 50)
xv, yv = np.meshgrid(x_space, y_space)


from matplotlib import path
import matplotlib.patches as patches
p = path.Path(list(zip(xl, yl))+list(zip(xr,yr))[::-1])


xv_in, yv_in = [], []
xv_out, yv_out = [], []
for x_, y_ in zip(xv, yv):
    for x, y in zip(x_, y_):
        if p.contains_points([(x,y)]):
            xv_in.append(x)
            yv_in.append(y)
        else:
            xv_out.append(x)
            yv_out.append(y)

fig, ax = plt.subplots()
patch = patches.PathPatch(p,color=None)
ax.add_patch(patch)
ax.scatter(xv_in, yv_in,color='red')
ax.scatter(xv_out, yv_out,color='yellow')

ax.set_xlim(x_lower_limit, x_upper_limit)
ax.set_ylim(y_lower_limit, y_upper_limit)
# print(p.contains_points([(125,-45)]))
plt.show()
# """