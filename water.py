class WaterSys:
    def __init__(self, env_temperature):
        self.env_temperature = env_temperature
        self.wue = 1.6

    def simulate_water_usage(self, server_power_usage, time_step):
        """server power usage unit is watt
            wue unit is L/kWh
            time_step is in hour
        """


        return self.wue * (server_power_usage/1000) *time_step