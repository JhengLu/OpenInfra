![OpenInfra Icon](figures/openinfra-icon.svg)

# OpenInfra

## Features

### Datacenter:
- Manage UPS status (online/offline), power limits, and capacity
- Simulate UPS battery charge/discharge
- Control datacenter power and rack loads
- Design custom datacenter topology (UPS, PDU, racks, cooling, gNB, user equipment)
- Simulate water usage for cooling

### Power Plant:
- Simulate 8 power generation types
- Simulate water usage for cooling



## How to Run
```sh
python main.py
```
This will generate the topology figure as `topology.pdf`.

## Draw the Result
```sh
python visualize.py
```
This will generate the result figure as `power_usage_and_battery_charge_level_plot.pdf`.

