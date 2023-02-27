# test car env

from air_gym.envs.car_env import AirSimCarEnv
import time
env = AirSimCarEnv(path_to_sim_binary='C:\\Users\\stepa\\dev\\diploma\\simulator\\Blocks.exe',
                   road_path='C:\\Users\\stepa\\dev\\diploma\\roads\\train\\2023-02-10-18-57-33.csv',
                   target_speed=10)

for i in range(1000):
    env.step([1,0,0])