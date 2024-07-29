import random

class PowerGenerator:
    def __init__(self, min_power=10, max_power=100):
        self.min_power = min_power
        self.max_power = max_power
        self.generated_power = 0

    def generate_power(self):
        self.generated_power = 27000
        return self.generated_power

class Battery:
    def __init__(self, capacity, initial_soc=1, min_soc=0, charge_rate=100):
        self.capacity = capacity
        assert 0 <= initial_soc <= 1
        self.charge_level = capacity * initial_soc
        self._soc = initial_soc
        assert 0 <= min_soc <= self._soc
        self.min_soc = min_soc
        self.charge_rate = charge_rate

    @property
    def soc(self):
        return self.charge_level / self.capacity

    def discharge(self, amount):
        self.charge_level -= amount
        if self.charge_level < self.min_soc * self.capacity:
            self.charge_level = self.min_soc * self.capacity
        return amount

class UPS:
    def __init__(self, ups_id, power_capacity, power_limit, connected_pdu_list, battery):
        self.ups_id = ups_id
        self.power_capacity = power_capacity
        self.power_limit = power_limit
        self.connected_pdu_list = connected_pdu_list
        self.battery = battery

class PDU:
    def __init__(self, pdu_id, connected_ups_id, connected_device_type, connected_device_id):
        self.pdu_id = pdu_id
        self.connected_ups_id = connected_ups_id
        self.connected_device_type = connected_device_type
        self.connected_device_id = connected_device_id
