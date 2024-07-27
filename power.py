import random
import time

class PowerGenerator:
    def __init__(self, min_power=10, max_power=100):
        self.min_power = min_power
        self.max_power = max_power
        self.generated_power = 0

    def generate_power(self):
        # Simulate power generation with a random value within the specified range
        # self.generated_power = random.uniform(self.min_power, self.max_power)
        self.generated_power = 1000
        return self.generated_power

class UPS:
    power_capacity = 500  # Class attribute
    power_limit = 0.8     # Class attribute

    def __init__(self, ups_id, connected_pdu_list):
        self.ups_id = ups_id
        self.connected_pdu_list = connected_pdu_list

class PDU:
    def __init__(self, pdu_id, connected_ups_id, connected_device_type, connected_device_id):
        self.pdu_id = pdu_id
        self.connected_ups_id = connected_ups_id
        self.connected_device_type = connected_device_type
        self.connected_device_id = connected_device_id


