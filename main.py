import matplotlib.pyplot as plt
import networkx as nx
from controller import Controller

def draw_structure(controller):
    print("UPS to PDU Connections:")
    for ups in controller.ups_list:
        print(f"UPS {ups.ups_id} -> PDUs: {', '.join(map(str, ups.connected_pdu_list))}")

    print("\nPDU to Device Connections:")
    for pdu in controller.pdu_list:
        print(
            f"PDU {pdu.pdu_id} (UPS: {', '.join(map(str, pdu.connected_ups_id))}) -> Device Types: {', '.join(pdu.connected_device_type)}, Device IDs: {', '.join(map(str, pdu.connected_device_id))}")

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

    # Add rack nodes and edges from PDU to rack
    for pdu in controller.pdu_list:
        for device_type, device_id in zip(pdu.connected_device_type, pdu.connected_device_id):
            if device_type == "normal_rack":
                rack_label = f"NormalRack {device_id}"
            elif device_type == "wireless_rack":
                rack_label = f"WirelessRack {device_id}"
            G.add_node(rack_label, type=device_type, layer=2)
            G.add_edge(f"PDU {pdu.pdu_id}", rack_label)

    # Add gNB nodes and edges from wireless rack to gNB
    for gnb in controller.gnb_list:
        gnb_label = f"gNB {gnb.gNB_id}"
        G.add_node(gnb_label, type='gNB', layer=3)
        for rack in controller.wireless_racks:
            if rack.rack_id == gnb.connected_rack_id:
                G.add_edge(f"WirelessRack {rack.rack_id}", gnb_label)

        # Add UE nodes and edges from gNB to UE
        for ue_id in gnb.connected_ue_list:
            ue_label = f"UE {ue_id}"
            G.add_node(ue_label, type='UE', layer=4)
            G.add_edge(gnb_label, ue_label)

    # Define a layout for hierarchical structure
    pos = nx.multipartite_layout(G, subset_key="layer")

    # Sort the nodes by their numeric identifier within each layer
    layer_nodes = {layer: [] for layer in set(nx.get_node_attributes(G, 'layer').values())}
    for node, data in G.nodes(data=True):
        layer_nodes[data['layer']].append(node)

    for layer in layer_nodes:
        layer_nodes[layer].sort(key=lambda x: int(x.split()[-1]))

    # Assign positions from left to right for each layer
    for layer, nodes in layer_nodes.items():
        for i, node in enumerate(nodes):
            pos[node] = (i, -layer)

    # Draw the graph
    plt.figure(figsize=(14, 12))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold',
            edge_color='gray')
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'UPS'], node_color='green',
                           node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'PDU'],
                           node_color='lightgreen', node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'normal_rack'], node_color='orange',
                           node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'wireless_rack'], node_color='purple',
                           node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'gNB'], node_color='red',
                           node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'UE'], node_color='blue',
                           node_size=3000)

    plt.title("Datacenter Topology")
    plt.savefig('topology.png')
    # plt.show()

def main():
    controller = Controller.from_config('config.json')
    draw_structure(controller)
    draw_topology(controller)
    controller.start_simulation(duration=1000)

if __name__ == "__main__":
    main()
