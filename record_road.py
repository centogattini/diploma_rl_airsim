# This is the script for the road generation
# The Road generation can be implemented in 2 ways
# -------------------------------------------
# First approach
# A user itself controls the car and his trajectory is recorded. His
# trajectory is used to define the road.
# -------------------------------------------
# Second approach
# A road can be generated using the random road generator with the given parameters
# of curvity and length of the road.
#
# Here is an implementation of the first approach
if __name__ == '__main__':

    import utils
    import time
    import keyboard
    import airsim
    import glob
    import os
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from datetime import datetime

    simulator = utils.Simulator()

    print("This is a road generator.")
    print("Do you want to record train or test road?")

    test = bool(int(input("Type [0] for train and [1] for test road: ")))
    save_path = 'roads\\test\\' if test else 'roads\\train\\'

    print("Press the key `u` to start (recording will start automaticly). \nPress the key `u` again to finish the ride")
    while not keyboard.is_pressed('u'):
        pass

    simulator.start_simulator()
    print("Starting the simulator ...")
    time.sleep(3)
    car = airsim.client.CarClient(ip='127.0.0.1')
    car.startRecording()
    print("Recording has started ...")

    while not keyboard.is_pressed('u'):
        pass
    car.stopRecording()
    print("Recording is finished")

    list_of_files = glob.glob('C:\\Users\\stepa\\Documents\\AirSim\\*')
    latest_record = max(
        list_of_files, key=os.path.getctime) + '\\airsim_rec.txt'

    route_record = pd.read_csv(latest_record, sep='\t')[['POS_X', 'POS_Y']].rename(
        columns={'POS_X': 'x', 'POS_Y': 'y'})
    route_record = route_record.round(2).drop_duplicates()

    line_width = 3

    def calc_road_lines(a, b, h=line_width):
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

    def get_lanes(x, y, h=3, show=False):
        dots = list(zip(x, y))
        road_left = []
        road_right = []
        for i in range(1, len(dots)):
            left, right = calc_road_lines(dots[i-1], dots[i], h=h)
            road_left.append(left)
            road_right.append(right)

        def get_line(road_line, i): return np.array(
            list(map(lambda x: x[i], road_line)))

        xr = get_line(road_right, 0)
        yr = get_line(road_right, 1)

        xl = get_line(road_left, 0)
        yl = get_line(road_left, 1)
        if show:
            x_space = np.array(np.arange(-5, 80, 1))
            y_space = np.array(np.arange(5, -60, -1))
            xv, yv = np.meshgrid(x_space, y_space)

            plt.plot(xr, yr, '.-', label='right_lane')
            plt.plot(xl, yl, '.-', label='left_lane')
            plt.plot(x, y, '.-', label='center')
            plt.legend()
            plt.show()
        return xl, yl, xr, yr
    x, y = np.array(route_record['x']), np.array(route_record['y'])
    xl, yl, xr, yr = get_lanes(x, y, show=True)
    print('Do you agree to record this road?')
    confirmation = bool(int(input("Type [0] for delete record and [1] for save it: ")))
    if confirmation:
        df = pd.DataFrame()
        df['xl'] = xl
        df['yl'] = yl
        df['xr'] = xr
        df['yr'] = yr
        save_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        print(save_date)
        df.to_csv(save_path+'\\'+save_date+'.csv')
