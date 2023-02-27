import os
import gym
from gym import spaces 
import airsim
import numpy as np
from shapely import geometry
from matplotlib.path import Path
import math
from utils import rotate
from time import sleep
import pandas as pd

class AirSimCarEnv(gym.Env):
    def __init__(self, 
                path_to_sim_binary,
                road_path,
                target_velocity):
        os.startfile(path_to_sim_binary)
        sleep(10)
        self.car = airsim.CarClient(ip='127.0.0.1')
        # action is a continuous vector 
        # action = [steering, throttle, break]
        self.action_space = spaces.Box(low=np.array([-1,-1,0]),
                                       high=np.array([1,1,1]))
        # observation is a continuous vector
        # state = [speed, some_obs_of_route]
        # The first approach:
        # some_obs_of_route = [distance_to_left_border, distance_to_right_border]
        # We can simulate driving a car in the given road line.
        # One of the disadvanteges of this approach is that agent doesn't have information
        # about nearest turns of the road line. This problem can be solved using some additional 
        # information about road structure, like measuring additional two distances to the road 
        # borders from the point which is N meters in front of the vehicle.   
        # maybe this approach is realised in some cruise-control systems 
        # 
        # The second approach:
        # Road is simulated not as a road line, but as a center of the road. So, the agent
        # is given with the next N points of the following road, so he can control car
        # paying attention to the nearest turns. But this approach isn't so realistic,
        # because we don't have information about the width of the road. (?) This approach
        # was used in the paper 
        # S Kabanov, G Mitiai, H Wu, O Petrosian
        # "Comparison of Reinforcement Learning 
        # Based Control Algorithms for 
        # One Autonomous Driving Problem"
        # 
        # We'll try to implement the first approach 
        # obs = [speed, left_dist_1, right_dist_1, ... left_dist_3, right_dist_3]
        self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0, 0, 0, 0]), 
                                            high=np.array([120, 10, 50, 50, 50, 50, 50]))        
        self.car_controls = airsim.CarControls()

        self.state = {
            "position": np.array([0,0]),
            "prev_position": np.array([0,0]),
            "z_yaw": 0,
            "velocity": 0,
        }
        road_df = pd.read_csv(road_path)
        xl, yl, xr, yr = road_df['xl'], road_df['yl'], road_df['xr'], road_df['yr']

        self.road_polygon = geometry.Polygon(list(zip(xl, yl))+list(zip(xr,yr))[::-1])
        self.target_velocity = target_speed
        # add visualization of learning process (here or in the `render` function)  

    def _get_obs(self, ):
        SCALE = 8.0 # optional, must be > 3.0 in order to work fine (presumably it doesn't have any impact on learning)
        position = self.state['position']
        prev_position = self.state['prev_position']
        direction = (position - prev_position) / np.linalg.norm(prev_position - position)
        # build a center line on position, direction 
        center_line = geometry.LineString([prev_position, prev_position + SCALE*direction])
        l45_1 = geometry.LineString(rotate(list(center_line.coords),angle=math.pi/4))
        l45_2 = geometry.LineString(rotate(list(center_line.coords),angle=-math.pi/4))
        l90_1 = geometry.LineString(rotate(list(center_line.coords),angle=math.pi/2))
        l90_2 = geometry.LineString(rotate(list(center_line.coords),angle=-math.pi/2))
        
        ls = [center_line, l45_1, l45_2, l90_1, l90_2]
        intersections = []
        for l in ls:
            intersection = center_line.intersection(l)
            if not intersection.is_empty:
                intersections.append(intersection[0])
            else:
                x_lim, y_lim  = l.coords[-1]
                intersections.append([x_lim, y_lim])
        obs = self._transform_into_car_coordinates(np.array(intersections)).flatten()
        # SHAPE [10]
        return obs 
        # get lines with angle 90, 30 (for each angle two lines) with the center line 
        # get first intersections of theese lines with the road lines (in the CAR COORDINATE SYSTEM)
        # return intersections (in case of missing intersection return smth like (0, 0) - intersection point)
    
    def _update_state(self, ):
        """
            Updates the state of a vehicle
            angle, position, velocity,
        """
        kinematics = self.car.getCarState().kinematics_estimated
        x = kinematics.orientation.x_val
        y = kinematics.orientation.y_val
        z = kinematics.orientation.z_val
        w = kinematics.orientation.w_val
        velocity = kinematics.linear_velocity
        self.state["z_yaw"] = math.degrees(math.atan2((2.0*(w*z + x*y)), (1.0-2.0*(y**2 + z**2))))
        self.state["prev_position"]  = self.state["position"]
        self.state["position"] = kinematics.position[0:1]
        self.state["velocity"] = velocity

    def _transform_into_car_coordinates(self, points):
        translated = points - self.state["position"]
        rotated = rotate(points=translated,angle=self.state["z_yaw"])
        return rotated

    def _reward(self, ):
        # calculate reward based on a current state 
        x, y = self.state["position"]
        velocity = self.state["velocity"]
        if self.road_polygon.contains((x,y)):
            reward = -np.abs((velocity-self.target_velocity))/self.target_velocity
        else:
            reward = -1
        return reward
    
    def _get_info(self, ):
        return None

    def step(self, ):
        reward = self._reward()
        obs = self._get_obs()
        done = reward <= -1
        info = self._get_info()
        return obs, reward, done, info

    def reset(self, ):
        pass

    def close(self, ):
        pass

