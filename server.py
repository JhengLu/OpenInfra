import random

class NormalServer:
    def __init__(self, server_id, connected_pdu_id, CPU_util, GPU_util, power_usage):
        self.server_id = server_id
        self.connected_pdu_id = connected_pdu_id
        self.CPU_util = CPU_util
        self.GPU_util = GPU_util
        self.power_usage = power_usage

    def simulate_load(self, power_dict):
        target_loads = list(power_dict.keys())
        simulated_load = random.choices(target_loads, k=1)[0]
        self.power_usage = power_dict[simulated_load]
        return self.power_usage

class WirelessServer:
    def __init__(self, server_id, connected_pdu_id, CPU_util, power_usage, connected_gnb_id):
        self.server_id = server_id
        self.connected_pdu_id = connected_pdu_id
        self.CPU_util = CPU_util
        self.power_usage = power_usage
        self.connected_gnb_id = connected_gnb_id

    def simulate_load(self, power_dict):
        target_loads = list(power_dict.keys())
        simulated_load = random.choices(target_loads, k=1)[0]
        self.power_usage = power_dict[simulated_load]
        return self.power_usage
