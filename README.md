# Get endpoint info from CloudVision

A python script which queries a CloudVision instance for historical information regarding endpoints. The endpoints are specified using an input text file containing MAC addresses. The output is returned in a CSV with fields showing the device, interface, and time the MAC was last seen.

## Requirements

- Python 3.11+ recommended
- Access to an Arista CloudVision instance
- A CloudVision API token with permission to read inventory

## Install

From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install cloudvision
```

## Quick Start

The script expects all configuration to be supplied in command-line arguments:

- `--apiserver`
- `--auth`
- `--input-file`
- `--output-file`

Login to your CloudVision instance and look at your browser URL. The FQDN will be used along with ':443' appended to create the --apiserver string.

Create a file to store the token for your CloudVision service account. The file should contain only one line with the token string. This file will be referenced by --auth and will be in the format token,filename.

Create a file with one MAC address per line and with each MAC address in the format XX:XX:XX:XX:XX:XX. This will be referenced by --input-file.

For the --output-file specification, supply a file name with .csv extension as the output will be CSV format.

Example:
```bash
python3 get_endpoint_info.py --apiserver www.cv-prod-us-4.arista.io:443 --auth token,cv.tok --input-file inputmacs.txt --output-file endpoints.csv
```

## File Formats
Input file should have one MAC address per line...
```bash
ae:8c:6f:6d:84:23
64:16:66:d2:d8:e0
54:b2:03:05:de:a0
f0:78:16:fa:27:c2
2c:cf:67:95:14:8b
14:b3:1f:1e:01:ca
00:c0:b7:c9:7b:99
```

Output file will be CSV format with the first line containing column headers...
```bash
MAC,Device,Interface,VlanID,Timestamp
ae:8c:6f:6d:84:23,NQ-Wireless,Ethernet12,1069,2026-05-04T10:31:03.428586959Z
64:16:66:d2:d8:e0,MB-ED,Ethernet13,669,2026-04-28T13:03:54.901779890Z
54:b2:03:05:de:a0,MB-C1,Ethernet49/1,668,2026-04-13T23:53:51.319759130Z
f0:78:16:fa:27:c2,MB-C1,Vlan2546,2546,2026-04-13T21:09:05.400429929Z
2c:cf:67:95:14:8b,CANTON-HQ-DC,Vlan8,8,2026-04-08T17:31:06.367619486Z
14:b3:1f:1e:01:ca,MB-EL,Ethernet2,669,2026-05-02T11:40:59.907750368Z
00:c0:b7:c9:7b:99,MB-C1,Ethernet48,2546,2026-04-07T23:26:27.220101594Z
```

## Current Limitations

- There is minimal input validation and error handling.
- No environment-variable configuration for token management (CV token is contained in file)
