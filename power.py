import random
import pandas as pd

class PowerGenerator:
    def __init__(self, min_power=10, max_power=100):
        self.min_power = min_power
        self.max_power = max_power
        self.generated_power = 0
        self.location = "cal"
        self.time_zone = "pacific-time"
        self.power_raw_trace_df = pd.read_csv(f"data/{self.location}-{self.time_zone}.csv", index_col=0)
        self.power_projected_trace_df = self.project_power_trace()
        self.power_projected_trace_df.to_csv(f"data/{self.location}-{self.time_zone}-processed.csv")




    def generate_power(self, time_step):
        return (self.power_projected_trace_df.loc[time_step, 'WND'] + self.power_projected_trace_df.loc[time_step, 'SUN']) * 1000000, self.power_projected_trace_df.loc[time_step, 'WND'] * 1000000, self.power_projected_trace_df.loc[time_step, 'SUN'] * 1000000 # translate MW to W


    def project_power_trace(self):
        # Define the investment values (these should be defined according to your context)
        WND_PPA_MW = 3  # Example investment value for wind, replace with actual value
        SUN_PPA_MW = 1.9  # Example investment value for solar, replace with actual value

        # Load the data from a CSV file
        filename = "data/cal-pacific-time"
        data = pd.read_csv(filename + ".csv")

        # Convert negative values to zero
        data['Wind Generation (MWh)'] = data['Wind Generation (MWh)'].clip(lower=0)
        data['Solar Generation (MWh)'] = data['Solar Generation (MWh)'].clip(lower=0)

        # Calculate the maximum capacities
        max_wnd_cap = data['Wind Generation (MWh)'].max()
        max_sun_cap = data['Solar Generation (MWh)'].max()

        # Normalize the wind and solar generation based on the investments and maximum capacities
        data['WND'] = data['Wind Generation (MWh)'] / max_wnd_cap * WND_PPA_MW
        data['SUN'] = data['Solar Generation (MWh)'] / max_sun_cap * SUN_PPA_MW

        # Create the hour index
        data['hour_index'] = range(len(data))

        # Select only the required columns
        result = data[['hour_index', 'WND', 'SUN']]

        return result



    def loadDB(self, path):
        dfa = pd.read_csv(path, index_col=0, parse_dates=True)
        print(f"Data loaded from {path}")
        return dfa


class PowerGenerator_carbon_explorer:
    def __init__(self, min_power=10, max_power=100):
        self.min_power = min_power
        self.max_power = max_power
        self.generated_power = 0
        self.dc_ba_map = {
        # "OR": "BPAT",
        # "NC": "DUK",
        "UT": "PACE",
        }
        # <dc_power_map>: map of average DC power capacity in MW
        self.dc_power_map = {
        "OR": 70,
        "NC": 50,
        "UT": 20,
        }
        # <ba_ppa_map>: map of renewable [wind, solar] investment amounts (in MW) you want to make for each grid (BA)
        self.ba_ppa_map = {
            "BPAT": [100, 0],  # 500 MW wind farm, no solar farm
            "DUK": [0, 410],  # no wind farm, 410 MW solar farm
            "PACE": [1.5, 1.6],  # 239 MW wind, 694 MW solar farm
            # "PACE": [0, 6.94],
            # "PACE": [3.39, 1.94],
        }
        self.location = "UT"
        self.power_raw_trace_df = pd.read_csv(f"data/power_gen_{self.location}_with_hour_index.csv", index_col=0)
        self.power_projected_trace_df = self.project_power_trace()
        self.power_projected_trace_df.to_csv(f"data/power_projected_gen_{self.location}_with_hour_index.csv")




    def generate_power(self, time_step):
        return (self.power_projected_trace_df.loc[time_step, 'WND'] + self.power_projected_trace_df.loc[time_step, 'SUN']) * 1000000, self.power_projected_trace_df.loc[time_step, 'WND'] * 1000000, self.power_projected_trace_df.loc[time_step, 'SUN'] * 1000000 # translate MW to W


    def project_power_trace(self):
        # Simulate each datacenter in our map
        for dc in self.dc_ba_map:
            db = self.power_raw_trace_df
            db[db < 0] = 0
            wnd_db = db['WND'].fillna(0)
            sun_db = db['SUN'].fillna(0)
            max_wnd_cap = wnd_db.max()
            max_sun_cap = sun_db.max()
            SUN_PPA_MW = self.ba_ppa_map[self.dc_ba_map[dc]][1]
            WND_PPA_MW = self.ba_ppa_map[self.dc_ba_map[dc]][0]
            print("Renewable Investment Amount --  SUN: ", SUN_PPA_MW, "WND: ", WND_PPA_MW)
            # Project the renewable generation amount from your ren. investments
            # based on the maximum generation in the grid during the corresponding data range
            if (max_wnd_cap != 0):
                wnd_db = wnd_db / max_wnd_cap * WND_PPA_MW
            if (max_sun_cap != 0):
                sun_db = sun_db / max_sun_cap * SUN_PPA_MW
            projected_db = pd.concat([wnd_db, sun_db], axis=1)
            return projected_db



    def loadDB(self, path):
        dfa = pd.read_csv(path, index_col=0, parse_dates=True)
        print(f"Data loaded from {path}")
        return dfa















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
        old_charge_level = self.charge_level
        self.charge_level -= power_amount * time_step
        if self.charge_level < self.min_soc * self.capacity:
            self.charge_level = self.min_soc * self.capacity
        discharged_energy = old_charge_level - self.charge_level
        return discharged_energy

    def charge(self, power_amount, time_step):
        self.charge_level += power_amount * time_step
        if self.charge_level > self.capacity:
            self.charge_level = self.capacity
        return power_amount * time_step

    def max_power_support(self, time_step):
        return (self.charge_level - self.capacity * self.min_soc) / time_step




import pybamm


class PyBammBattery(Battery):
    def __init__(self, capacity, initial_soc=1, min_soc=0, charge_rate=100):
        super().__init__(capacity, initial_soc, min_soc, charge_rate)
        self.capacity_ah = capacity
        self.model = pybamm.lithium_ion.DFN()
        self.model.options["calculate discharge energy"] = "true"
        parameter_values = self.model.default_parameter_values
        parameter_values.update({"Nominal cell capacity [A.h]": self.capacity_ah})
        # usually the nominal cell capacity is like 5.0 A.h
        parameter_values.update({
            "Nominal cell capacity [A.h]": self.capacity_ah,
            "Lower voltage cut-off [V]": 0,
            "Upper voltage cut-off [V]": 10
        })
        print("nominal capacity is: " + str(self.capacity_ah))
        self.simulation = pybamm.Simulation(self.model, parameter_values=parameter_values)
        self.solution = self.simulation.solve(t_eval=[0, 1])  # Initial solve with a short time interval
        self.min_soc = min_soc
        self.current_soc = initial_soc

    def discharge(self, power_amount, duration_hours):
        """
        Discharge the battery with a given power for a specific duration.

        Args:
            power_amount (float): Power in Watts.
            duration (float): Duration in hours.
        """
        # Convert duration to hours for the experiment string

        # Define the experiment string using the power amount and duration
        experiment_string = f"Discharge at {power_amount} W for {duration_hours} hours"

        # Create an experiment with the string
        experiment = pybamm.Experiment([experiment_string])

        # Run the simulation with the experiment, using the previous solution as the initial state
        self.simulation = pybamm.Simulation(self.model, experiment=experiment,
                                            parameter_values=self.simulation.parameter_values)
        self.solution = self.simulation.solve(initial_soc=self.current_soc)

        # Extract discharge energy and capacity
        discharge_capacity = self.solution["Discharge capacity [A.h]"].data[-1]
        print(f"Discharge capacity: {discharge_capacity:.2f} A.h")
        # Update SOC and charge level
        self.current_soc -= discharge_capacity / self.capacity_ah
        self.current_soc = max(self.current_soc, self.min_soc)
        print(f"current_soc: {self.current_soc} ")

        return self.solution

    def charge(self, power_amount, duration_hours):
        """
        Charge the battery with a given power for a specific duration.

        Args:
            power_amount (float): Power in Watts.
            duration (float): Duration in seconds.
        """

        # Define the experiment string using the power amount and duration
        experiment_string = f"Charge at {power_amount} W for {duration_hours} hours"  # Negative power for charging

        # Create an experiment with the string
        experiment = pybamm.Experiment([experiment_string])

        # Run the simulation with the experiment, using the previous solution as the initial state
        self.simulation = pybamm.Simulation(self.model, experiment=experiment,
                                            parameter_values=self.simulation.parameter_values)
        self.solution = self.simulation.solve(initial_soc=self.current_soc)

        # Extract charge energy and capacity
        charge_capacity = (-1) * self.solution["Discharge capacity [A.h]"].data[-1]
        print(f"Charge capacity: {charge_capacity:.2f} A.h")

        self.current_soc += charge_capacity / self.capacity_ah
        self.current_soc = min(1, self.current_soc)
        print(f"current_soc: {self.current_soc} ")

        return self.solution

# Modify the existing functions to use the new class


def get_batteries_max_power_support(ups_list, time_step):
    # print(f"Total power surplus: {surplus_power:.2f} units")
    batteries_max_power_support = 0
    for ups in ups_list:
        if ups.online:
            battery = ups.battery
            batteries_max_power_support += battery.max_power_support(time_step)

    return batteries_max_power_support






# Modify the existing functions to use the new class
def discharge_batteries(ups_list, deficit_power, time_step):
    # print(f"Total power deficit: {deficit_power:.2f} units")
    total_discharged_energy = 0
    for ups in ups_list:
        if ups.online:
            battery = ups.battery
            discharge_amount = deficit_power / len(ups_list)
            actual_discharge_energy = battery.discharge(discharge_amount, time_step)
            total_discharged_energy += actual_discharge_energy
            # print(f"UPS {ups.ups_id} battery discharged by {actual_discharge_energy:.2f} units")

    return total_discharged_energy

def charge_batteries(ups_list, surplus_power, time_step):
    # print(f"Total power surplus: {surplus_power:.2f} units")
    for ups in ups_list:
        if ups.online:
            battery = ups.battery
            charge_amount = surplus_power / len(ups_list)
            actual_charge = battery.charge(charge_amount, time_step)
            # print(f"UPS {ups.ups_id} battery charged by {actual_charge:.2f} units")



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

    # @staticmethod
    # def discharge_batteries(ups_list, deficit_power, time_step):
    #     print(f"Battery 2, Total power deficit: {deficit_power:.2f} units")
    #     for ups in ups_list:
    #         if ups.online:
    #             battery = ups.battery
    #             discharge_power_amount = deficit_power / len(ups_list)
    #             actual_discharge = battery.discharge(discharge_power_amount, time_step)
    #             print(f"UPS {ups.ups_id} battery discharged by {actual_discharge:.2f} units")
    #
    # @staticmethod
    # def charge_batteries(ups_list, surplus_power, time_step):
    #     print(f"Battery 2, Total power surplus: {surplus_power:.2f} units")
    #     for ups in ups_list:
    #         if ups.online:
    #             battery = ups.battery
    #             charge_power_amount = surplus_power / len(ups_list)
    #             actual_charge = battery.charge(charge_power_amount, time_step)
    #             print(f"UPS {ups.ups_id} battery charged by {actual_charge:.2f} units")




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
