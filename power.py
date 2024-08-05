import random

class PowerGenerator:
    def __init__(self, min_power=10, max_power=100):
        self.min_power = min_power
        self.max_power = max_power
        self.generated_power = 0

    def generate_power(self):
        self.generated_power = 35000
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

    def discharge(self, power_amount, time_step):
        self.charge_level -= power_amount * time_step
        if self.charge_level < self.min_soc * self.capacity:
            self.charge_level = self.min_soc * self.capacity
        return power_amount * time_step

    def charge(self, power_amount, time_step):
        self.charge_level += power_amount * time_step
        if self.charge_level > self.capacity:
            self.charge_level = self.capacity
        return power_amount * time_step

    @staticmethod
    def discharge_batteries(ups_list, deficit_power, time_step):
        print(f"Total power deficit: {deficit_power:.2f} units")
        for ups in ups_list:
            if ups.online:
                battery = ups.battery
                discharge_power_amount = deficit_power / len(ups_list)
                actual_discharge = battery.discharge(discharge_power_amount, time_step)
                print(f"UPS {ups.ups_id} battery discharged by {actual_discharge:.2f} units")

    @staticmethod
    def charge_batteries(ups_list, surplus_power, time_step):
        print(f"Total power surplus: {surplus_power:.2f} units")
        for ups in ups_list:
            if ups.online:
                battery = ups.battery
                charge_power_amount = surplus_power / len(ups_list)
                actual_charge = battery.charge(charge_power_amount, time_step)
                print(f"UPS {ups.ups_id} battery charged by {actual_charge:.2f} units")

# Battery model that includes efficiency and
# linear charging/discharging rate limits with respect to battery capacity
class Battery2:
    def __init__(self, capacity, initial_soc=0,min_soc=0, charge_rate=100,
                 eff_c=0.5, eff_d=1.04,
                 c_lim=3, d_lim=3,
                 upper_u=-0.04, upper_v=1,
                 lower_u=0.01, lower_v=0):
        self.capacity = capacity
        assert 0 <= initial_soc <= 1
        self.charge_level = capacity * initial_soc
        self.min_soc = min_soc
        self.charge_rate = charge_rate
        self.eff_c = eff_c
        self.eff_d = eff_d
        self.c_lim = c_lim
        self.d_lim = d_lim
        self.upper_lim_u = upper_u
        self.upper_lim_v = upper_v
        self.lower_lim_u = lower_u
        self.lower_lim_v = lower_v

    @property
    def soc(self):
        return self.charge_level / self.capacity

    def calc_max_charge(self, T_u):
        max_charge = min((self.capacity / self.eff_c) * self.c_lim,
                         (self.upper_lim_v * self.capacity - self.charge_level) / (
                                 (self.eff_c * T_u) - self.upper_lim_u))
        return max_charge

    def calc_max_discharge(self, T_u):
        max_discharge = min((self.capacity / self.eff_d) * self.d_lim,
                            (self.charge_level - self.lower_lim_v * self.capacity) / (
                                    self.lower_lim_u + (self.eff_d * T_u)))
        return max_discharge

    def charge(self, input_load, T_u=1):
        max_charge = self.calc_max_charge(T_u)
        self.charge_level = self.charge_level + (min(max_charge, input_load) * self.eff_c * T_u)
        if self.charge_level > self.capacity:
            self.charge_level = self.capacity
        return min(max_charge, input_load) * self.eff_c * T_u

    def discharge(self, output_load, T_u=1):
        max_discharge = self.calc_max_discharge(T_u)
        self.charge_level = self.charge_level - (min(max_discharge, output_load) * self.eff_d * T_u)
        if max_discharge < output_load:
            print("max_discharge < output_load")
            return False
        return min(max_discharge, output_load) * self.eff_d * T_u

    def is_full(self):
        return self.capacity == self.charge_level

    @staticmethod
    def discharge_batteries(ups_list, deficit_power, time_step):
        print(f"Battery 2, Total power deficit: {deficit_power:.2f} units")
        for ups in ups_list:
            if ups.online:
                battery = ups.battery
                discharge_power_amount = deficit_power / len(ups_list)
                actual_discharge = battery.discharge(discharge_power_amount, time_step)
                print(f"UPS {ups.ups_id} battery discharged by {actual_discharge:.2f} units")

    @staticmethod
    def charge_batteries(ups_list, surplus_power, time_step):
        print(f"Battery 2, Total power surplus: {surplus_power:.2f} units")
        for ups in ups_list:
            if ups.online:
                battery = ups.battery
                charge_power_amount = surplus_power / len(ups_list)
                actual_charge = battery.charge(charge_power_amount, time_step)
                print(f"UPS {ups.ups_id} battery charged by {actual_charge:.2f} units")

class UPS:
    def __init__(self, ups_id, power_capacity, power_limit, connected_pdu_list, battery, online=True):
        self.ups_id = ups_id
        self.power_capacity = power_capacity
        self.power_limit = power_limit
        self.connected_pdu_list = connected_pdu_list
        self.battery = battery
        self.online = online

class PDU:
    def __init__(self, pdu_id, connected_ups_id, connected_device_type, connected_device_id, online=True):
        self.pdu_id = pdu_id
        self.connected_ups_id = connected_ups_id
        self.connected_device_type = connected_device_type
        self.connected_device_id = connected_device_id
        self.online = online
