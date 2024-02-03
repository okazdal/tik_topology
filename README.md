# tik_topology
Python tool to draw topology of a MikroTik RoMON enabled network 

## Requirements
- Python 3.6 or later
- RoMON enabled MikroTik devices
- MikroTik API SSL access

## Installation
```bash
git clone https://github.com/okazdal/tik_topology.git
cd tik_topology
pipenv shell
pipenv install
cd RouterOS-api
python setup.py install
```

## Usage
```bash
python topo_discovery.py --isp_name <isp_name> --isp_ip <isp_ip> --router_ip <router_ip> --router_user <router_user> --router_pass <router_pass> --router_port <router_port>

python topo_links --isp_name <isp_name>
``` 

First Command will discover the network topology and store it in a file named `isp_name`.csv. 
Second command will draw the topology and store it in a file named `isp_name`.html.
You can find these files under topos folder.
