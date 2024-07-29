import random

class Server:
    def __init__(self, server_id):
        self.server_id = server_id
        self.CPU_util = random.uniform(0.1, 0.9)  # Initialize with random utilization
        self.GPU_util = random.uniform(0.1, 0.9)  # Initialize with random utilization
        self.power_usage = 0

    def simulate_load(self, power_dict):
        target_loads = list(power_dict.keys())
        simulated_load = random.choices(target_loads, k=1)[0]
        self.power_usage = power_dict[simulated_load]
        return self.power_usage

class Rack:
    def __init__(self, rack_id, connected_pdu_id):
        self.rack_id = rack_id
        self.connected_pdu_id = connected_pdu_id
        self.server_list = []

    def add_server(self, server):
        self.server_list.append(server)
