import json
import time
from power import PowerGenerator, UPS, PDU

class Controller:
    def __init__(self, generator, ups_list, pdu_list):
        self.generator = generator
        self.ups_list = ups_list
        self.pdu_list = pdu_list
        self.received_power = 0

    @classmethod
    def from_config(cls, config_path):
        # Read config.json file
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Create UPS objects from config
        ups_list = []
        for ups_config in config['UPS']:
            ups = UPS(
                ups_id=ups_config['ups_id'],
                connected_pdu_list=ups_config['connected_pdu_list']
            )
            ups_list.append(ups)

        # Create PDU objects from config
        pdu_list = []
        for pdu_config in config['PDU']:
            pdu = PDU(
                pdu_id=pdu_config['pdu_id'],
                connected_ups_id=pdu_config['connected_ups_id'],
                connected_device_type=pdu_config['connected_device_type'],
                connected_device_id=pdu_config['connected_device_id']
            )
            pdu_list.append(pdu)

        # Create PowerGenerator object
        generator = PowerGenerator(min_power=50, max_power=150)

        return cls(generator, ups_list, pdu_list)

    def receive_power(self):
        # Receive the generated power from the generator
        self.received_power = self.generator.generate_power()
        print(f"Controller received power: {self.received_power:.2f} units")

    def start_simulation(self, duration=10):
        # Simulate receiving power every second for the given duration
        for _ in range(duration):
            self.receive_power()
            time.sleep(1)
