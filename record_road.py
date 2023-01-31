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
    import keyboard
    import airsim

    simulator = utils.Simulator()
    
    print("This is a road generator. \nPress the key `u` to start. \nPress the key `r` to start recording\nPress the key `u` again to finish the ride ")

    while not keyboard.is_pressed('u'):
        pass

    simulator.start_simulator()
    
    print("Starting the simulator ...")

    while not keyboard.is_pressed('r'):
        pass
    
    car = airsim.client.CarClient(ip='127.0.0.1')

    while not keyboard.is_pressed('u'):
        pass
    car.stopRecording()
    
