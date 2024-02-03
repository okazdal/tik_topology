from pydantic import BaseModel
import routeros_api
import argparse
import io
import os


class Neighbor(BaseModel):
    id: str
    address: str
    cost: str
    hops: str
    path: str
    l2mtu: str
    identity: str
    version: str
    board: str
    

def get_romon_discovery(router_ip, router_user, router_pass, router_port):
    connection = routeros_api.RouterOsApiPool(router_ip, username=router_user, port=int(router_port),
                                          password=router_pass, use_ssl=True, ssl_verify=False,
                                          plaintext_login=True)
    api = connection.get_api()
    resp = api.get_binary_resource('/').call('tool/romon/discover', {'duration': '20'})

    devices = []
    for l in resp:
        # print(l['path'], type(l['path']))
        path = l['path'].decode('utf-8').replace(',', '===')
        # print(path, type(path))
        neighbor = Neighbor(
            id=l['address'],
            # flags=l['flags'],
            address=l['address'],
            cost=l['cost'],
            hops=l['hops'],
            path=path,
            l2mtu=l['l2mtu'],
            identity=l['identity'].decode('utf-8', errors='ignore'),
            version=l['version'],
            board=l['board']
        )
        devices.append(neighbor)
    resp = api.get_binary_resource('/').call('system/identity/print')
    root_identity = resp[0]['name']
    root_neighbor = Neighbor(
        id="00:00:00:00:00:00",
        address="00:00:00:00:00:00",
        cost="0",
        hops="0",
        path="",
        l2mtu="0",
        identity=root_identity,
        version="6",
        board="RouterBoard"
    )
    devices.append(root_neighbor)
    connection.disconnect()
    return unique_neighbors(devices)


def unique_neighbors(neighbors):
    unique = []
    unique_neighbors = []
    for n in neighbors:
        if n.address not in unique:
            unique.append(n.address)
            unique_neighbors.append(n)
    return unique_neighbors


def create_csv_file(neighbors, filename):
    with open(filename, 'w') as f:
        f.write('address,identity,board,version,cost,hops,path,l2mtu\n')
        for n in neighbors:
            f.write(f'{n.address},{n.identity},{n.board},{n.version},{n.cost},{n.hops},{n.path},{n.l2mtu}\n')
            

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--isp_name', type=str, required=True)
    parser.add_argument('--router_ip', type=str, required=True)
    parser.add_argument('--router_port', type=str, required=True, default='8729')
    parser.add_argument('--router_user', type=str, required=True, default='admin')
    parser.add_argument('--router_pass', type=str, required=True, default='')
    args = parser.parse_args()

    ISP_NAME = args.isp_name
    router_ip = args.router_ip
    router_user = args.router_user
    router_pass = args.router_pass
    router_port = args.router_port
    
    neighbors = get_romon_discovery(router_ip, router_user, router_pass, router_port)

    # Create 'topos' directory if it doesn't exist
    if not os.path.exists('topos'):
        os.makedirs('topos')
        
    create_csv_file(neighbors, f'topos/{ISP_NAME}.csv')
    

if __name__ == '__main__':
    main()