import matplotlib.pyplot as plt
import networkx as nx
from controller import Controller


def draw_structure(controller):
    print("Data Center Structure")
    print("======================")

    for pdu in controller.pdu_list:
        ups_id = pdu.connected_ups_id
        connected_device_type_str = ', '.join(pdu.connected_device_type)
        connected_device_id_str = ', '.join(map(str, pdu.connected_device_id))
        print(
            f"PDU {pdu.pdu_id} (UPS: {ups_id}) -> Device Types: {connected_device_type_str}, Device IDs: {connected_device_id_str}")

    print("======================")


def draw_topology(controller):
    G = nx.DiGraph()

    # Add UPS nodes
    for ups in controller.ups_list:
        G.add_node(f"UPS {ups.ups_id}", type='UPS', layer=0)

    # Add PDU nodes and edges from UPS to PDU
    for pdu in controller.pdu_list:
        G.add_node(f"PDU {pdu.pdu_id}", type='PDU', layer=1)
        G.add_edge(f"UPS {pdu.connected_ups_id}", f"PDU {pdu.pdu_id}")

    # Add grouped rack nodes and edges from PDU to rack group
    rack_ranges = {}
    for pdu in controller.pdu_list:
        if pdu.connected_device_type and pdu.connected_device_id:
            min_rack_id = min(pdu.connected_device_id)
            max_rack_id = max(pdu.connected_device_id)
            rack_range = f"Racks {min_rack_id}-{max_rack_id}"
            rack_ranges[(min_rack_id, max_rack_id)] = rack_range
            G.add_node(rack_range, type='rack_group', layer=2)
            G.add_edge(f"PDU {pdu.pdu_id}", rack_range)

    # Add gNB nodes and edges from wireless rack group to gNB
    for gnb in controller.gnb_list:
        gnb_label = f"gNB {gnb.gNB_id}"
        G.add_node(gnb_label, type='gNB', layer=3)

        # Find the rack range to which this gNB is connected
        for (min_rack_id, max_rack_id), rack_range in rack_ranges.items():
            if min_rack_id <= gnb.connected_rack_id <= max_rack_id:
                G.add_edge(rack_range, gnb_label)
                break
        else:
            raise ValueError(f"No rack range found for gNB {gnb.gNB_id} connected to rack {gnb.connected_rack_id}")

        # Add UE nodes and edges from gNB to UE
        for ue_id in gnb.connected_ue_list:
            ue_label = f"UE {ue_id}"
            G.add_node(ue_label, type='UE', layer=4)
            G.add_edge(gnb_label, ue_label)

    # Check if all nodes have the 'layer' attribute
    for node, data in G.nodes(data=True):
        if 'layer' not in data:
            raise ValueError(f"Node {node} does not have the 'layer' attribute.")

    # Define a layout for hierarchical structure
    pos = nx.multipartite_layout(G, subset_key="layer")

    # Draw the graph
    plt.figure(figsize=(14, 12))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold',
            edge_color='gray')
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'UPS'], node_color='green',
                           node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'PDU'],
                           node_color='lightgreen', node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'rack_group'],
                           node_color='orange', node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'gNB'], node_color='red',
                           node_size=3000)
    nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if G.nodes[n]['type'] == 'UE'], node_color='blue',
                           node_size=3000)

    plt.title("Datacenter Topology")
    plt.savefig('topology.png')
    plt.show()







def main():
    controller = Controller.from_config('simple_config.json')
    draw_structure(controller)
    draw_topology(controller)
    controller.start_simulation(duration=101)  # max is 744


if __name__ == "__main__":
    main()
