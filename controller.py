import json
import csv
import random
from power import PowerGenerator, UPS, PDU, Battery, Battery2, PyBammBattery, charge_batteries, discharge_batteries
from server import *
from wireless import gNB, UE
from cooling import CoolSys
from tqdm import tqdm  # Import tqdm correctly

class Controller:
    def __init__(self, generator, ups_list, pdu_list, normal_racks, wireless_racks, gnb_list, ue_list, cool_sys,
                 minimal_server_load_percentage, server_max_power, server_idle_power, battery_control_limit, battery_recover_signal):
        self.generator = generator
        self.ups_list = ups_list
        self.pdu_list = pdu_list
        self.normal_racks = normal_racks
        self.wireless_racks = wireless_racks
        self.gnb_list = gnb_list
        self.ue_list = ue_list
        self.cool_sys = cool_sys
        self.battery_control_limit = battery_control_limit
        self.battery_recover_signal = battery_recover_signal
        self.minimal_server_load_percentage = minimal_server_load_percentage
        self.server_max_power = server_max_power
        self.server_idle_power = server_idle_power
        self.received_power = 0

    @classmethod
    def from_config(cls, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)

        background = config['background']
        minimal_server_load_percentage = background['minimal_server_load']
        battery_control_limit = background['battery_control_limit']
        battery_recover_signal = background['battery_recover_signal']
        server_max_power = background['server_max_power']
        server_idle_power = background['server_idle_power']

        def create_battery(battery_config):
            if battery_config['battery_type'] == 1:
                return Battery(
                    battery_config['capacity'],
                    battery_config['initial_soc'],
                    battery_config['min_soc'],
                    battery_config['charge_rate']
                )
            elif battery_config['battery_type'] == 2:
                return Battery2(
                    battery_config['capacity'],
                    battery_config['initial_soc'],
                    battery_config['min_soc'],
                    battery_config['charge_rate']
                )
            elif battery_config['battery_type'] == 3:
                return PyBammBattery(
                    battery_config['capacity'],
                    battery_config['initial_soc'],
                    battery_config['min_soc'],
                    battery_config['charge_rate']
                )
            else:
                raise ValueError(f"Unknown battery type: {battery_config['battery_type']}")

        # Create UPS list
        ups_list = [
            UPS(
                ups_config['ups_id'],
                ups_config['ups_power_deliver_capacity'],
                eval(ups_config['ups_init_power_limit']),
                [],  # Connected PDUs will be filled later
                create_battery(ups_config['ups_battery']),
                ups_config['online']
            ) for ups_config in config['UPS']
        ]

        # Create PDU list and associate racks with PDUs
        pdu_list = []
        normal_racks = []
        wireless_racks = []
        added_rack_ids = set()  # Track which racks have been added to avoid duplicates

        for pdu_config in config['PDU']:
            connected_device_type = []
            connected_device_id = []

            # Assign normal racks to this PDU
            rack_range = pdu_config['connected_rack_id_range']
            for rack_id in range(rack_range[0], rack_range[1] + 1):
                if rack_id not in added_rack_ids:
                    connected_device_type.append('normal_rack')
                    connected_device_id.append(rack_id)
                    rack = Rack(rack_id + 1, [pdu_config['id']], rack_id + 1)
                    for _ in range(background['number_of_servers_per_rack']):
                        server = Server(f"Rack-{rack_id + 1}-Server-{_ + 1}", server_idle_power, server_max_power)
                        rack.add_server(server)
                    normal_racks.append(rack)
                    added_rack_ids.add(rack_id)  # Mark the rack as added

            # Assign wireless racks to this PDU
            for gnb in config['gNB']:
                if gnb['connected_rack_id'] in range(rack_range[0], rack_range[1] + 1):
                    if gnb['connected_rack_id'] not in added_rack_ids:
                        connected_device_type.append('wireless_rack')
                        connected_device_id.append(gnb['connected_rack_id'])
                        rack = Rack(gnb['connected_rack_id'] + 1, [pdu_config['id']], gnb['connected_rack_id'] + 1)
                        for _ in range(background['number_of_servers_per_rack']):
                            server = Server(f"Wireless-Rack-{rack.rack_id}-Server-{_ + 1}", server_idle_power,
                                            server_max_power)
                            rack.add_server(server)
                        wireless_racks.append(rack)
                        added_rack_ids.add(gnb['connected_rack_id'])  # Mark the wireless rack as added

            # Create PDU instance
            pdu = PDU(
                pdu_config['id'],
                pdu_config['connected_ups_id'],
                connected_device_type,
                connected_device_id,
                True
            )
            pdu_list.append(pdu)

        # Create gNB and UE list
        gnb_list = [gNB(**gnb_config) for gnb_config in config['gNB']]
        ue_list = [UE(**ue_config) for ue_config in config['UE']]

        # Create cooling system instance
        cool_sys = CoolSys(**config['CoolSys'])

        # Create power generator
        generator = PowerGenerator(min_power=50, max_power=150)

        return cls(generator, ups_list, pdu_list, normal_racks, wireless_racks, gnb_list, ue_list, cool_sys,
                   minimal_server_load_percentage, server_max_power, server_idle_power, battery_control_limit, battery_recover_signal)

    def simulate_server_power_usage(self):
        total_power_usage = 0
        for rack in self.normal_racks + self.wireless_racks:
            for server in rack.server_list:
                server_power_usage = server.simulate_power()
                total_power_usage += server_power_usage
                print(f"Server {server.server_id} power usage: {server_power_usage} W")
        return total_power_usage

    def simulate_trivial_power_usage(self, server_power_usage):
        return 0.1 * server_power_usage

    def get_ups_limit(self):
        for ups in self.ups_list:
            if ups.online:
                return ups.power_limit

    def increase_ups_limit(self):
        for ups in self.ups_list:
            if ups.online:
                ups.power_limit = min(0.1 + ups.power_limit, 1)

    def control_rack_loads(self):
        for rack in sorted(self.normal_racks + self.wireless_racks, key=lambda x: x.priority):
            for server in rack.server_list:
                if server.load_percentage > rack.max_power_load_percentage:
                    server.load_percentage = rack.max_power_load_percentage

        total_battery_soc = sum(ups.battery.soc for ups in self.ups_list if ups.online) / len(
            [ups for ups in self.ups_list if ups.online])

        if total_battery_soc < self.battery_control_limit:
            if self.get_ups_limit() == 1:
                for rack in sorted(self.normal_racks + self.wireless_racks, key=lambda x: x.priority):
                    if rack.max_power_load_percentage > self.minimal_server_load_percentage:
                        rack.max_power_load_percentage -= 10
                        print(f"Reducing max load limit for rack {rack.rack_id} to {rack.max_power_load_percentage}%")
                        return
            else:
                self.increase_ups_limit()

        elif total_battery_soc > self.battery_recover_signal:
            for rack in sorted(self.normal_racks + self.wireless_racks, key=lambda x: x.priority, reverse=True):
                if rack.max_power_load_percentage < 100:
                    rack.max_power_load_percentage += 10
                    print(f"Increasing max load limit for rack {rack.rack_id} to {rack.max_power_load_percentage}%")
                    return

    def start_simulation(self, duration=10):
        print(f"Initial Cooling System Power Usage: {self.cool_sys.cool_load} W")
        google_cpu_usage_trace_csv = load_cpu_usage("data/total_usage.csv")

        with open('power_usage.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['Time', 'Generated Power', 'Wind Power', 'Solar Power'] +
                [f'UPS {ups.ups_id} Battery Charge Level' for ups in self.ups_list] +
                [f'UPS {ups.ups_id} Status' for ups in self.ups_list] +
                [f'UPS {ups.ups_id} Deliverable Power' for ups in self.ups_list] +
                ['Total Power Usage', 'Server Power Usage', 'Cool Power Usage', 'Other Power Usage', 'Online UPS Power'] +
                [f'Normal Rack {rack.rack_id} Max Load %' for rack in self.normal_racks] +
                ['Battery Control Limit', 'Battery Recover Signal']
            )

            for t in tqdm(range(duration)):
                self.received_power, wind_power, solar_power = self.generator.generate_power(t)
                # simulate the server load
                for rack in sorted(self.normal_racks + self.wireless_racks, key=lambda x: x.priority):
                    for server in rack.server_list:
                        load_percentage = server.simulate_google_cpu_util(google_cpu_usage_trace_csv, t)
                        server.load_percentage = load_percentage

                self.control_rack_loads()
                server_power_usage = self.simulate_server_power_usage()
                cool_power_usage = self.cool_sys.simulate_coolsys_power_usage(server_power_usage)
                other_power_usage = self.simulate_trivial_power_usage(server_power_usage)

                total_power_usage = server_power_usage + cool_power_usage + other_power_usage
                print(f"Total Power Usage: {total_power_usage:.2f} W")

                online_ups_power = sum(
                    ups.power_capacity * ups.power_limit for ups in self.ups_list if ups.online)
                print(f"Total UPS capacity limit: {online_ups_power:.2f} W")

                deliverable_ups_power = [
                    ups.power_capacity * ups.power_limit if ups.online else 0 for ups in self.ups_list
                ]

                time_step = 1
                if total_power_usage > self.received_power or server_power_usage > online_ups_power:
                    deficit_power = max(total_power_usage - self.received_power,
                                        server_power_usage - online_ups_power)
                    discharge_batteries(self.ups_list, deficit_power, time_step)
                else:
                    surplus_power = self.received_power - total_power_usage
                    charge_batteries(self.ups_list, surplus_power, time_step)

                writer.writerow(
                    [t, self.received_power, wind_power, solar_power] +
                    [ups.battery.charge_level for ups in self.ups_list] +
                    [ups.online for ups in self.ups_list] +
                    deliverable_ups_power +
                    [total_power_usage, server_power_usage, cool_power_usage, other_power_usage, online_ups_power] +
                    [rack.max_power_load_percentage for rack in self.normal_racks] +
                    [self.battery_control_limit * self.ups_list[0].battery.capacity] +
                    [self.battery_recover_signal * self.ups_list[0].battery.capacity]
                )


if __name__ == "__main__":
    controller = Controller.from_config('simple_config.json')
    controller.start_simulation(duration=744)
