import os
import json
import subprocess
class Simulator:

    def start_simulator(self,):
        with open('metadata.json', 'r') as f:
            simulator_path = json.load(f)['SimulatorPath']
        assert os.path.exists(simulator_path), "Given wrong path to the simulator. Change it in /metadata.json"
        # os.startfile(simulator_path)
        proc = subprocess.run(f"{simulator_path}")
        print(proc)
    def exit_simulator(self,):
        # subprocess.
        pass