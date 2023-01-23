import os
import gym
from gym import spaces 
import airsim
import numpy as np


class AirSimCarEnv(gym.Env):
    def __init__(self, path_to_sim_binary):
        os.startfile(path_to_sim_binary)
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
        # obs = [speed, left_dist, right_dist, front_left_dist, front_right_dist]
        self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0, 0]), 
                                            high=np.array([120, 50, 50, 50, 50]))
        # agent won't see this information. It's needed for debug purposes
        self.state = {
            "position": np.zeros(3),
            "prev_position": np.zeros(3), 
        }
        self.car_controls = airsim.CarControls()
        # add visualization of learning process (here or in the `render` function)  

    def step(self, ):
        pass

    def reset(self, ):
        pass

    def render(self, ):
        pass

    def close(self, ):
        pass
