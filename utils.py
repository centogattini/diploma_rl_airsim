import os
import json
def start_simulator():
    with open('metadata.json', 'r') as f:
        simulator_path = json.load(f)['SimulatorPath']
    assert os.path.exists(simulator_path), "Given wrong path to the simulator. Change it in /metadata.json"
    os.startfile(simulator_path)