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
    
    def simulate_chiller_power_usage(self, server_temperature, energy_grid_temperature):
        server_temp_diff = server_temperature - self.safe_temperature
        energy_grid_temp_diff = energy_grid_temperature - self.safe_temperature
        datacenter_cooling_energy = (self.number_of_servers * self.flow_rate * self.water_density * self.water_specific_heat_capacity * server_temp_diff) / self.COP
        energy_grid_cooling_energy = (self.flow_rate * self.water_density * self.water_specific_heat_capacity * energy_grid_temp_diff) / self.COP
        return datacenter_cooling_energy + energy_grid_cooling_energy

class Pump:
    def __init__(self, pressure_head, pump_efficiency) -> None:
        self.pressure_head = pressure_head
        self.gravity = 9.81
        self.fluid_density = 0.9998395
        self.flow_rate = 34
        self.pump_efficiency = pump_efficiency

    def simulate_pump_power_usage(self, number_of_chillers):
        return (number_of_chillers * self.gravity * self.flow_rate * self.fluid_density * self.pressure_head) / self.pump_efficiency