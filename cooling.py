class CoolSys:
    def __init__(self, env_temperature):
        self.env_temperature = env_temperature
        self.cool_load = 0

    def simulate_coolsys_power_usage(self, server_power_usage):
        """this is very simple version"""

        return 0.3 * server_power_usage
