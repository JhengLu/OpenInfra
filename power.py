import time
import random

class PowerGenerator:
    def __init__(self, min_power=10, max_power=100):
        self.min_power = min_power
        self.max_power = max_power
        self.generated_power = 0

    def generate_power(self):
        self.generated_power = random.uniform(self.min_power, self.max_power)
        return self.generated_power

class UPS:
    def __init__(self, ups_id, power_capacity, power_limit, connected_pdu_list, connected_normal_racks, connected_wireless_racks):
        self.ups_id = ups_id
        self.power_capacity = power_capacity
        self.power_limit = power_limit
        self.connected_pdu_list = connected_pdu_list
        self.connected_normal_racks = connected_normal_racks
        self.connected_wireless_racks = connected_wireless_racks

class PDU:
    def __init__(self, pdu_id, connected_ups_id, connected_device_type, connected_device_id):
        self.pdu_id = pdu_id
        self.connected_ups_id = connected_ups_id
        self.connected_device_type = connected_device_type
        self.connected_device_id = connected_device_id




