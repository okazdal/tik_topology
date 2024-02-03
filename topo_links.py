import csv
import networkx as nx
from pyvis.network import Network
import argparse

def read_csv_file(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def links_separate(paths):
    links = set()
    for path in paths:
        path = path.split('===')
        for i in range(len(path) - 1):
            link = (path[i], path[i + 1])
            links.add(link)
    return links

def find_device(mac_address, devices):
    for device in devices:
        if device[0] == mac_address:
            return device[1]
    return None


def generate_nx(devices, links, isp_name):
    g = nx.Graph()
    nt = Network(height="1000px", width="100%")
    for n in devices:
        g.add_node(n[1], color='red' if n[0] == '00:00:00:00:00:00' else 'blue')
    for link in links:
        dev1 = find_device(link[0], devices)
        dev2 = find_device(link[1], devices)

        if dev1 is None or dev2 is None:
            continue
        g.add_edge(dev1, dev2)
    nx.draw(g, with_labels=True)
    
    nt.from_nx(g)
    
    nt.toggle_physics(True)
    nt.show_buttons(filter_=['physics'])
    nt.save_graph(f"topos/{isp_name}.html")
    return g


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--isp_name', type=str, required=True)
    args = parser.parse_args()
    
    CSV_FILE = f'topos/{args.isp_name}.csv'
    data = read_csv_file(CSV_FILE)
    
    devices = set()
    paths = []
    for i in data:
        if i[1] == "identity":
            continue
        device = (i[0], i[1].replace('-', '_').replace(' ', '_').replace('(', '_').replace(')', '_'))
        devices.add(device)
        paths.append(i[6])
        
    links = links_separate(paths)
    
    root_dev_identity = find_device("00:00:00:00:00:00", devices)
    main_device = ('00:00:00:00:00:00', root_dev_identity)
    devices.add(main_device)
    # ADD Main device links cost 200, path 1 in csv file
    for i in data:
        if i[5] == "1":
            link = (main_device[0], i[0])
            links.add(link)
    
    generate_nx(devices, links, args.isp_name)


if __name__ == '__main__':
    main()
    