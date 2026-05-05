# Get endpoint info from CloudVision

A python script which queries a CloudVision instance for historical information regarding endpoints. The endpoints are specified using an input text file containing MAC addresses. The output is returned in a CSV with fields showing the device, interface, and time the MAC was last seen.

## Requirements

- Python 3.11+ recommended
- Access to an Arista CloudVision instance
- A CloudVision API token with permission to read inventory/configlets and write workspaces or Studio inputs

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

## Current Limitations

- There is minimal input validation and error handling.
- No environment-variable configuration for token management (CV token is contained in file)
