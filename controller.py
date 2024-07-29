import json
import time
from power import PowerGenerator, UPS, PDU
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

        ups_list = [UPS(**ups_config) for ups_config in config['UPS']]
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

    def start_simulation(self, duration=10):
        print(f"Initial Cooling System Power Usage: {self.cool_sys.cool_load} W")

        for _ in range(duration):
            self.receive_power()
            server_power_usage = self.simulate_server_power_usage()
            cool_power_usage = self.cool_sys.simulate_coolsys_power_usage(server_power_usage)
            other_power_usage = self.simulate_trivial_power_usage(server_power_usage)

            total_power_usage = server_power_usage + cool_power_usage + other_power_usage
            print(f"Total Power Usage: {total_power_usage:.2f} W")
            time.sleep(1)
