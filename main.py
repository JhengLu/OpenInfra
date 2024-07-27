import matplotlib.pyplot as plt
import networkx as nx
from controller import Controller

def draw_structure(controller):
    print("UPS to PDU Connections:")
    for ups in controller.ups_list:
        print(f"UPS {ups.ups_id} -> PDUs: {', '.join(map(str, ups.connected_pdu_list))}")

    print("\nPDU to Device Connections:")
    for pdu in controller.pdu_list:
        print(f"PDU {pdu.pdu_id} (UPS: {', '.join(map(str, pdu.connected_ups_id))}) -> Device Type: {pdu.connected_device_type}, Device ID: {pdu.connected_device_id}")

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

    # Add device nodes and edges from PDU to device
    for pdu in controller.pdu_list:
        device_label = f"{pdu.connected_device_type} {pdu.connected_device_id}"
        G.add_node(device_label, type='Device', layer=2)
        G.add_edge(f"PDU {pdu.pdu_id}", device_label)

    # Define a layout for hierarchical structure
    pos = nx.multipartite_layout(G, subset_key="layer")

    # Sort nodes within each layer to ensure the small numbers start from the left
    layers = {0: [], 1: [], 2: []}
    for node, (x, y) in pos.items():
        layer = int(G.nodes[node]['type'] == 'UPS') + int(G.nodes[node]['type'] == 'PDU') * 2
        layers[layer].append((node, x, y))

    for layer in layers.values():
        layer.sort(key=lambda x: int(x[0].split()[-1]))  # Sort by the numeric part of the identifier

    new_pos = {}
    for i, layer in enumerate(layers.values()):
        for j, (node, x, y) in enumerate(layer):
            new_pos[node] = (j, -i)

    # Draw the graph
    plt.figure(figsize=(10, 8))
    nx.draw(G, new_pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
    nx.draw_networkx_nodes(G, new_pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'UPS'], node_color='green', node_size=3000)
    nx.draw_networkx_nodes(G, new_pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'PDU'], node_color='lightgreen', node_size=3000)
    nx.draw_networkx_nodes(G, new_pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'Device'], node_color='orange', node_size=3000)

    plt.title("Datacenter Topology")
    plt.show()

def main():
    controller = Controller.from_config('config.json')
    draw_structure(controller)
    draw_topology(controller)
    controller.start_simulation(duration=5)

if __name__ == "__main__":
    main()
