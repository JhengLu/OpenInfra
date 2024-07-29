import json
import csv
from power import PowerGenerator, UPS, PDU, Battery
from server import Server, Rack
from wireless import gNB, UE
from cooling import CoolSys

class Controller:
    def __init__(self, generator, ups_list, pdu_list, normal_racks, wireless_racks, gnb_list, ue_list, cool_sys):
        self.generator = generator
        self.ups_list = ups_list
        self.pdu_list = pdu_list
        self.normal_racks = normal_racks
        self.wireless_racks = wireless_racks
        self.gnb_list = gnb_list
        self.ue_list = ue_list
        self.cool_sys = cool_sys
        self.received_power = 0
        self.power_dict = {
            100: 222,
            90: 205,
            80: 189,
            70: 170,
            60: 153,
            50: 140,
            40: 128,
            30: 118,
            20: 109,
            10: 98,
            0: 58.4
        }

    @classmethod
    def from_config(cls, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)

        ups_list = [
            UPS(
                ups_config['ups_id'],
                ups_config['power_capacity'],
                eval(ups_config['power_limit']),  # Convert the string "2/3" to a fraction
                ups_config['connected_pdu_list'],
                Battery(
                    ups_config['battery']['capacity'],
                    ups_config['battery']['initial_soc'],
                    ups_config['battery']['min_soc'],
                    ups_config['battery']['charge_rate']
                )
            ) for ups_config in config['UPS']
        ]
        pdu_list = [PDU(**pdu_config) for pdu_config in config['PDU']]

        normal_racks = []
        for rack_config in config['NormalRacks']:
            rack = Rack(rack_config['rack_id'], rack_config['connected_pdu_id'])
            for _ in range(rack_config['number_of_servers']):
                server = Server(f"NS-{rack_config['rack_id']}-{_}")
                rack.add_server(server)
            normal_racks.append(rack)

        wireless_racks = []
        for rack_config in config['WirelessRacks']:
            rack = Rack(rack_config['rack_id'], rack_config['connected_pdu_id'])
            for _ in range(rack_config['number_of_servers']):
                server = Server(f"WS-{rack_config['rack_id']}-{_}")
                rack.add_server(server)
            wireless_racks.append(rack)

        gnb_list = [gNB(**gnb_config) for gnb_config in config['gNB']]
        ue_list = [UE(**ue_config) for ue_config in config['UE']]
        cool_sys = CoolSys(**config['CoolSys'])

        generator = PowerGenerator(min_power=50, max_power=150)

        return cls(generator, ups_list, pdu_list, normal_racks, wireless_racks, gnb_list, ue_list, cool_sys)

    def receive_power(self):
        self.received_power = self.generator.generate_power()
        print(f"Controller received power: {self.received_power:.2f} units")

    def simulate_server_power_usage(self):
        total_power_usage = 0
        for rack in self.normal_racks + self.wireless_racks:
            for server in rack.server_list:
                server_power_usage = server.simulate_load(self.power_dict)
                total_power_usage += server_power_usage
                print(f"Server {server.server_id} power usage: {server_power_usage} W")

        return total_power_usage

    def simulate_trivial_power_usage(self, server_power_usage):
        """
        This simulates the power usage of network equipment, PDU, UPS, etc.
        """
        return 0.1 * server_power_usage

    def discharge_batteries(self, deficit):
        print(f"Total power deficit: {deficit:.2f} units")
        for ups in self.ups_list:
            battery = ups.battery
            discharge_amount = deficit / len(self.ups_list)
            actual_discharge = battery.discharge(discharge_amount)
            print(f"UPS {ups.ups_id} battery discharged by {actual_discharge:.2f} units")

    def start_simulation(self, duration=10):
        print(f"Initial Cooling System Power Usage: {self.cool_sys.cool_load} W")

        with open('power_usage.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'Battery Charge Level', 'Total Power Usage', 'Server Power Usage', 'Cool Power Usage', 'Other Power Usage'])

            for t in range(duration):
                self.receive_power()
                server_power_usage = self.simulate_server_power_usage()
                cool_power_usage = self.cool_sys.simulate_coolsys_power_usage(server_power_usage)
                other_power_usage = self.simulate_trivial_power_usage(server_power_usage)

                total_power_usage = server_power_usage + cool_power_usage + other_power_usage
                print(f"Total Power Usage: {total_power_usage:.2f} W")

                # Calculate the total UPS capacity limit
                total_ups_capacity_limit = sum(ups.power_capacity * ups.power_limit for ups in self.ups_list)
                print(f"Total UPS capacity limit: {total_ups_capacity_limit:.2f} W")

                if total_power_usage > self.received_power or server_power_usage > total_ups_capacity_limit:
                    deficit = max(total_power_usage - self.received_power, server_power_usage - total_ups_capacity_limit)
                    self.discharge_batteries(deficit)

                # Save the current state to CSV
                for ups in self.ups_list:
                    writer.writerow([
                        t,
                        ups.battery.charge_level,
                        total_power_usage,
                        server_power_usage,
                        cool_power_usage,
                        other_power_usage
                    ])
