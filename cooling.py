class CoolSys:
    def __init__(self, env_temperature):
        self.env_temperature = env_temperature
        self.cool_load = 0

    def simulate_coolsys_power_usage(self, server_power_usage):
        """this is very simple version"""

        return 0.3 * server_power_usage


class Chiller:
    def __init__(self, number_of_servers):
        self.COP = 3.5
        self.flow_rate = 34 # some constant value
        self.water_specific_heat_capacity = 4.2
        self.water_density = 997
        self.safe_temperature = 23 # in celsius
        self.number_of_servers = number_of_servers
    def simulate_chiller_power_usage(self, server_temperature):
        temp_diff = server_temperature - self.safe_temperature
        return (self.number_of_servers * self.flow_rate * self.water_density * self.water_specific_heat_capacity * temp_diff) / self.COP

