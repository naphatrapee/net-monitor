# GNS3 Network Traffic Monitoring with Cisco OSPF, SNMP and Python

## Overview

This project demonstrates network configuration and traffic monitoring in a GNS3 lab using Cisco routers, OSPF dynamic routing, SNMPv2c, iperf3, and Python.

## Objectives

- Configure IP addressing and loopback interfaces on Cisco routers.
- Establish OSPF Area 0 routing between R1 and R2.
- Enable SNMP read-only monitoring on the routers.
- Generate UDP traffic using iperf3.
- Collect interface traffic counters and calculate throughput in Mbps using Python.

## Lab Topology

- R1 and R2: Cisco routers running OSPF Area 0.
- ipterm-1: iperf3 traffic client.
- ipterm-2: iperf3 traffic server.
- Ubuntu: Python and SNMP monitoring host.

## IP Addressing

| Device / Interface | IP Address |
|---|---|
| R1 Loopback0 | 1.1.1.1/32 |
| R1 FastEthernet1/0 | 10.12.0.1/24 |
| R2 Loopback0 | 2.2.2.2/32 |
| R2 FastEthernet1/0 | 10.12.0.2/24 |
| R1 FastEthernet1/1 | 172.16.0.1/24 |
| R2 FastEthernet1/1 | 172.16.1.1/24 |
| ipterm-1 | 172.16.0.10/24 |
| ipterm-2 | 172.16.1.10/24 |

## Tools

- GNS3
- Cisco IOS router images
- Ubuntu
- SNMP utilities (`snmpwalk`)
- Python 3
- iperf3

## How to Run

### 1. Configure the routers

Apply the configurations in `configs/R1.txt` and `configs/R2.txt`.

Verify OSPF neighbors and routes before starting the traffic test.

### 2. Start the iperf3 server

On ipterm-2:

```bash
iperf3 -s
```

### 3. Generate UDP traffic

On ipterm-1:

```bash
iperf3 -c 172.16.1.10 -u -b 5M -t 60
```

### 4. Install monitoring dependencies

On Ubuntu:

```bash
sudo apt update
sudo apt install snmp python3 -y
```

### 5. Run the monitoring script

Configure the target router IP and correct SNMP interface index in `get_traffic.py`, then run:

```bash
python3 get_traffic.py
```

## Results

During the lab test, the Python script reported approximately 5.23–5.28 Mbps outbound traffic on the monitored R1 interface. The inbound counter reported 0.00 Mbps in the captured output.

These measurements are specific to the recorded test and monitored interface.

## Repository Structure

```text
.
├── get_traffic.py
├── configs/
│   ├── R1.txt
│   └── R2.txt
├── screenshots/
└── README.md
```

## Limitations and Security Notes

- SNMPv2c community strings are not encrypted. Use secure SNMP settings and access controls in production.
- Interface indexes may differ between router models and configurations.
- The lab uses example addressing and a simulated GNS3 environment.
- Results depend on the selected interface, traffic direction, and measurement interval.

## Author

Add your name and GitHub profile here.
