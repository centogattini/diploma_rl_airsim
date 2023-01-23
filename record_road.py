# This is the script for the road generation
# The Road generation can be implemented in 2 ways
# -------------------------------------------
# First approach
# A user itself controls the car and his trajectory is recorded. His 
# trajectory is used to define the road. 
# -------------------------------------------
# Second approach
# A road can be generated using random road generator with given parameters
# of curvity and length of the road.
# 
# Here is an implementation of the first approach
if __name__ == '__main__':
    import utils
    utils.start_simulator()
    
