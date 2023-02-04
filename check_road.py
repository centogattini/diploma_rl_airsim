import glob
import os
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

def dist(x, y):
    x = np.array(x)
    y = np.array(y)
    return np.norm(y-x)

list_of_files = glob.glob('C:\\Users\\stepa\\Documents\\AirSim\\*')
latest_record = max(list_of_files, key=os.path.getctime) + '\\airsim_rec.txt'

route_record = pd.read_csv(latest_record, sep='\t')[['POS_X','POS_Y']].rename(columns={'POS_X':'x', 'POS_Y':'y'})
route_record = route_record.round(1).drop_duplicates()
route_record['prev_x'] = route_record['x'].shift(1)
route_record['prev_y'] = route_record['y'].shift(1)
route_record = route_record.drop(0)
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


def test_lanes(x,y,h=3):
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

    x_space = np.linspace(-5,80,50).round(1)
    y_space = np.linspace(5,-60,50).round(1)

    xv, yv = np.meshgrid(x_space, y_space)

    def check_if_inside(x, y,h=3):
        
        # many cases
        
        y_xl = yl[np.where(xl == x)]
        y_xl_up = y_xl[y_xl > y]
        y_xl_down = y_xl[y_xl < y]

        y_xr = yr[np.where(xr == x)]
        y_xr_up = y_xr[y_xr > y]
        y_xr_down = y_xr[y_xr < y]
        # moving left?
        # if all arrays are exist
        adv_min = lambda x: x.min() if x.any() else 10000000
        adv_max = lambda x: x.max() if x.any() else -10000000 
        
        debug = lambda i: print(x,y,'case', i)
        if adv_min(y_xl_up) < adv_min(y_xr_up) and adv_max(y_xr_down) > adv_max(y_xl_down):
            return True
        # moving right?
        elif adv_min(y_xl_up) > adv_min(y_xr_up) and adv_max(y_xr_down) < adv_max(y_xl_down):
            return True

        x_yl = xl[np.where(yl == y)]
        x_yl_right = x_yl[x_yl > x]
        x_yl_left = x_yl[x_yl < x]

        x_yr = xr[np.where(yr == y)]
        x_yr_right = x_yr[x_yr > x]
        x_yr_left = x_yr[x_yr < x]
        # moving up
        if adv_min(x_yr_right) < adv_min(x_yl_right) and adv_max(x_yl_left) > adv_max(x_yr_left):
            return True
        # moving down?
        elif adv_min(x_yr_right) > adv_min(x_yl_right) and adv_max(x_yl_left) < adv_max(x_yr_left):
            return True
        
        return False
    
    xv_out = []
    yv_out = []
    xv_in = []
    yv_in = []

    for x__ in xv:
        for y__ in yv:
            for x_, y_ in list(zip(x__,y__)):
                if check_if_inside(x_, y_):
                    xv_in.append(x_)
                    yv_in.append(y_)
                else:
                    xv_out.append(x_)
                    yv_out.append(y_)            

    plt.scatter(xv_out, yv_out,color='yellow')
    plt.scatter(xv_in, yv_in,color='red')

    plt.plot(xr,yr,'.-',label='right_lane')
    plt.plot(xl,yl,'.-',label='left_lane')
    plt.plot(x,y,'.-',label='center')
    plt.legend()
    plt.show()
    return xl,yl,xr,yr

### test sets of road_centers

x = np.array(route_record['x'])
y = np.array(route_record['y'])

xl,yl,xr,yr = test_lanes(x,y)


