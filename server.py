import random
import csv

class Server:
    def __init__(self, server_id, p_idle, p_max):
        self.server_id = server_id
        self.p_idle = p_idle
        self.p_max = p_max
        self.power_usage = 0
        self.load_percentage = -1

    def simulate_random_load(self, power_dict):
        target_loads = list(power_dict.keys())
        simulated_load = random.choices(target_loads, k=1)[0]
        self.power_usage = power_dict[simulated_load]
        return self.power_usage

# TODO add more trace patterns
    def simulate_google_cpu_util(self, cpu_usage_data, time_step):
        if time_step < len(cpu_usage_data):
            cpu_utilization = cpu_usage_data[time_step]
            return cpu_utilization
        else:
            return 0



    def simulate_server_power_usage(self):
        self.power_usage = self.p_idle + (self.p_max - self.p_idle) * self.load_percentage
        return self.power_usage

def load_cpu_usage(csv_file):
    cpu_usage_data = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cpu_usage_data.append(float(row['total_cpu_usage']))
    return cpu_usage_data


class Rack:
    def __init__(self, rack_id, connected_pdu_id, priority):
        self.rack_id = rack_id
        self.connected_pdu_id = connected_pdu_id
        self.priority = priority
        self.server_list = []
        self.max_power_load_percentage = 100

    def add_server(self, server):
        self.server_list.append(server)
