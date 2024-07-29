import matplotlib.pyplot as plt
import networkx as nx
from controller import Controller

def draw_structure(controller):
    print("UPS to PDU Connections:")
    for ups in controller.ups_list:
        print(f"UPS {ups.ups_id} -> PDUs: {', '.join(map(str, ups.connected_pdu_list))}")

    print("\nPDU to Rack Connections:")
    for pdu in controller.pdu_list:
        print(f"PDU {pdu.pdu_id} (UPS: {', '.join(map(str, pdu.connected_ups_id))}) -> Device Type: {pdu.connected_device_type}, Device ID: {pdu.connected_device_id}")

    print("\nRack to Server Connections:")
    for rack in controller.normal_racks + controller.wireless_racks:
        print(f"Rack {rack.rack_id} -> Servers: {', '.join([server.server_id for server in rack.server_list])}")

    print("\ngNB to WirelessRack Connections:")
    for gnb in controller.gnb_list:
        print(f"gNB {gnb.gNB_id} -> Rack {gnb.connected_rack_id}, UEs: {', '.join(map(str, gnb.connected_ue_list))}")

    print("\nUE to gNB Connections:")
    for ue in controller.ue_list:
        print(f"UE {ue.ue_id} -> gNB {ue.connected_gnb_id}")

    print("\nCooling System Info:")
    print(f"CoolSys -> env_temperature: {controller.cool_sys.env_temperature}")

def extract_numeric_part(identifier):
    # Extract numeric parts from the identifier
    parts = identifier.split('-')
    numeric_parts = [int(part) for part in parts if part.isdigit()]
    return numeric_parts[0] if numeric_parts else 0

def draw_topology(controller):
    G = nx.DiGraph()

    # Add UPS nodes
    for ups in controller.ups_list:
        G.add_node(f"UPS {ups.ups_id}", type='UPS', layer=0)

    # Add PDU nodes and edges from UPS to PDU
    for pdu in controller.pdu_list:
        G.add_node(f"PDU {pdu.pdu_id}", type='PDU', layer=1)
        for ups_id in pdu.connected_ups_id:
            G.add_edge(f"UPS {ups_id}", f"PDU {pdu.pdu_id}")

    # Add Rack nodes and edges from PDU to Rack
    for rack in controller.normal_racks:
        G.add_node(f"NormalRack {rack.rack_id}", type='NormalRack', layer=2)
        G.add_edge(f"PDU {rack.connected_pdu_id}", f"NormalRack {rack.rack_id}")

    for rack in controller.wireless_racks:
        G.add_node(f"WirelessRack {rack.rack_id}", type='WirelessRack', layer=2)
        G.add_edge(f"PDU {rack.connected_pdu_id}", f"WirelessRack {rack.rack_id}")

    # Add gNB nodes and edges from WirelessRack to gNB
    for gnb in controller.gnb_list:
        G.add_node(f"gNB {gnb.gNB_id}", type='gNB', layer=3)
        G.add_edge(f"WirelessRack {gnb.connected_rack_id}", f"gNB {gnb.gNB_id}")

    # Add UE nodes and edges from gNB to UE
    for ue in controller.ue_list:
        G.add_node(f"UE {ue.ue_id}", type='UE', layer=4)
        G.add_edge(f"gNB {ue.connected_gnb_id}", f"UE {ue.ue_id}")

    # Define a layout for hierarchical structure
    pos = nx.multipartite_layout(G, subset_key="layer")

    # Sort nodes within each layer to ensure the small numbers start from the left
    layers = {0: [], 1: [], 2: [], 3: [], 4: []}
    for node, (x, y) in pos.items():
        layer = int(G.nodes[node]['type'] == 'UPS') * 0 + int(G.nodes[node]['type'] == 'PDU') * 1 + int(G.nodes[node]['type'] == 'NormalRack') * 2 + int(G.nodes[node]['type'] == 'WirelessRack') * 2 + int(G.nodes[node]['type'] == 'gNB') * 3 + int(G.nodes[node]['type'] == 'UE') * 4
        layers[layer].append((node, x, y))

    for layer in layers.values():
        layer.sort(key=lambda x: extract_numeric_part(x[0]))  # Sort by the numeric part of the identifier

    new_pos = {}
    for i, layer in enumerate(layers.values()):
        for j, (node, x, y) in enumerate(layer):
            new_pos[node] = (j, -i)

    # Draw the graph
    plt.figure(figsize=(10, 8))
    nx.draw(G, new_pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
    nx.draw_networkx_nodes(G, new_pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'UPS'], node_color='green', node_size=3000)
    nx.draw_networkx_nodes(G, new_pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'PDU'], node_color='lightgreen', node_size=3000)
    nx.draw_networkx_nodes(G, new_pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'NormalRack'], node_color='orange', node_size=3000)
    nx.draw_networkx_nodes(G, new_pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'WirelessRack'], node_color='blue', node_size=3000)
    nx.draw_networkx_nodes(G, new_pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'gNB'], node_color='purple', node_size=3000)
    nx.draw_networkx_nodes(G, new_pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'UE'], node_color='red', node_size=3000)

    plt.title("Datacenter Topology")
    plt.show()

def main():
    controller = Controller.from_config('config.json')
    draw_structure(controller)
    draw_topology(controller)
    controller.start_simulation(duration=5)

if __name__ == "__main__":
    main()
