import json

def generate_full_config(simple_config_file, full_config_file):
    with open(simple_config_file, "r") as f:
        config = json.load(f)

    background = config["background"]
    pdu_number = background["pdu_number"]
    pdu_connected_rack_number = background["pdu_connected_rack_number"]
    battery_config = background["battery"]

    total_rack_number = pdu_number // 2 * pdu_connected_rack_number

    full_config = {
        "background": {
            "battery_control_limit": background["battery_control_limit"],
            "battery_recover_signal": background["battery_recover_signal"],
            "minimal_server_load": background["minimal_server_load"],
            "battery_type": background["battery_type"],
            "server_idle_power": background["server_idle_power"],
            "server_max_power": background["server_max_power"],
            "env_temperature": background["env_temperature"]
        },
        "UPS": [],
        "PDU": [],
        "NormalRacks": [],
        "gNB": [],
        "UE": [],
        "CoolSys": {
            "env_temperature": background["env_temperature"]
        }
    }

    # Generate UPS configuration
    for i in range(pdu_number // background["ups_connected_pdu_number"]):
        full_config["UPS"].append({
            "ups_id": i + 1,
            "power_capacity": background["ups_power_deliver_capacity"],
            "power_limit": background["ups_init_power_limit"],
            "online": True,
            "connected_pdu_list": [j for j in range(i * background["ups_connected_pdu_number"] + 1, (i + 1) * background["ups_connected_pdu_number"] + 1)],
            "battery": battery_config
        })

    # Generate PDU configuration
    normal_rack_ids = list(range(total_rack_number))
    wireless_rack_ids = normal_rack_ids[:background["number_of_wireless_racks"]]

    for pdu in config["PDU"]:
        rack_range = pdu["connected_rack_id_range"]
        full_config["PDU"].append({
            "pdu_id": pdu["id"],
            "online": True,
            "connected_ups_id": [pdu["connected_ups_id"]],
            "connected_device_type": ["normal_rack" if rack_id not in wireless_rack_ids else "wireless_rack" for rack_id in range(rack_range[0], rack_range[1] + 1)],
            "connected_device_id": [rack_id + 1 for rack_id in range(rack_range[0], rack_range[1] + 1)]
        })

    # Generate Racks configuration
    for i in range(total_rack_number):
        full_config["NormalRacks"].append({
            "rack_id": i + 1,
            "priority": i + 1,
            "connected_pdu_id": [1 + (i // pdu_connected_rack_number) * 2, 2 + (i // pdu_connected_rack_number) * 2],
            "number_of_servers": 40
        })

    # Generate gNB and UE configurations
    for i in range(1, background["number_of_wireless_racks"] + 1):
        full_config["gNB"].append({
            "gNB_id": i,
            "connected_rack_id": wireless_rack_ids[i - 1] + 1,
            "connected_ue_list": [1, 2, 3]
        })
        for j in range(1, 4):
            full_config["UE"].append({
                "ue_id": j,
                "connected_gnb_id": i
            })

    with open(full_config_file, "w") as f:
        json.dump(full_config, f, indent=2)

if __name__ == "__main__":
    generate_full_config("simple_config.json", "full_config.json")
