import os
import json
import subprocess
class Simulator:

    def __init__(self, ):
        self.isRunning = False

    def start_simulator(self,):
        assert self.isRunning == False, "Current simulator is already running"
        with open('metadata.json', 'r') as f:
            simulator_path = json.load(f)['SimulatorPath']
        assert os.path.exists(simulator_path), "Given wrong path to the simulator. Change it in /metadata.json"
        os.startfile(simulator_path)
        

    def exit_simulator(self,):
        # subprocess.
        pass
def rotate(points, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = [0,0]
    rotated_points = []
    for point in points:
        px, py = point
        qx = math.cos(angle) * (px-ox) - math.sin(angle) * (py-oy)
        qy = math.sin(angle) * (px-ox) + math.cos(angle) * (py-oy)
        rotated_points.append([qx,qy])
    return np.array(rotated_points)