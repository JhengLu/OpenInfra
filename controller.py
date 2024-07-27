import json
import time
from power import PowerGenerator, UPS, PDU
from server import NormalServer, WirelessServer
from wireless import gNB, UE

class Controller:
    def __init__(self, generator, ups_list, pdu_list, normal_servers, wireless_servers, gnb_list, ue_list):
        self.generator = generator
        self.ups_list = ups_list
        self.pdu_list = pdu_list
        self.normal_servers = normal_servers
        self.wireless_servers = wireless_servers
        self.gnb_list = gnb_list
        self.ue_list = ue_list
        self.received_power = 0

    @classmethod
    def from_config(cls, config_path):
        # Read config.json file
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Create UPS objects from config
        ups_list = [UPS(**ups_config) for ups_config in config['UPS']]

        # Create PDU objects from config
        pdu_list = [PDU(**pdu_config) for pdu_config in config['PDU']]

        # Create NormalServer objects from config
        normal_servers = [NormalServer(**server_config) for server_config in config['NormalServer']]

        # Create WirelessServer objects from config
        wireless_servers = [WirelessServer(**server_config) for server_config in config['WirelessServer']]

        # Create gNB objects from config
        gnb_list = [gNB(**gnb_config) for gnb_config in config['gNB']]

        # Create UE objects from config
        ue_list = [UE(**ue_config) for ue_config in config['UE']]

        # Create PowerGenerator object
        generator = PowerGenerator(min_power=50, max_power=150)

        return cls(generator, ups_list, pdu_list, normal_servers, wireless_servers, gnb_list, ue_list)

    def receive_power(self):
        # Receive the generated power from the generator
        self.received_power = self.generator.generate_power()
        print(f"Controller received power: {self.received_power:.2f} units")

    def start_simulation(self, duration=10):
        # Simulate receiving power every second for the given duration
        for _ in range(duration):
            self.receive_power()
            time.sleep(1)
