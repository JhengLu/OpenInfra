<p align="center">
  <img src="figures/openinfra-icon.png" alt="OpenInfra Icon" width="400">
</p>


Critical infrastructures like datacenters, power grids, and water systems are deeply interdependent, forming a complex “infrastructure nexus” that requires co-optimization for efficiency, resilience, and sustainability. 
OpenInfra is a co-simulation framework designed to model these interdependencies by integrating domain-specific simulators for datacenters, power plants, and cooling systems. 

**This project is under active development. If you want to reproduce the results from [OpenInfra 2024 paper](https://hotinfra24.github.io/papers/hotinfra24-final1.pdf), please refer to the ``openinfra-2024`` branch.**

[//]: # (# OpenInfra)

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

## Setup
```shell
pip install -r requirements.txt
```

---

## Quick Start
```sh
python main.py
```
This will generate the topology figure as `topology.pdf`. The output of the simulation results will be stored in `power_usage.csv`.

## Draw the Results
```sh
python visualize.py
```
This will generate a figure showing the results in `power_usage_and_battery_charge_level_plot.pdf`.

## Customize the Simulation Scenario
Open the `simple_config.json` file to update the simulation attributes.

## References

Please read and/or cite the following if you use OpenInfra code or data, or if you would like to learn more about OpenInfra.

```bibtex
@inproceedings{openinfra-hotinfra22,
  title={OpenInfra: A Co-simulation Framework for the Infrastructure Nexus},
  author={Jiaheng Lu, Yunming Xiao, Shmeelok Chakraborty, Silvery Fu, Yoon Sung Ji, Ang Chen, Mosharaf Chowdhury, Nalini Rao, Sylvia Ratnasamy, Xinyu Wang},
  booktitle={HotInfra},
  year={2024}
}
```
