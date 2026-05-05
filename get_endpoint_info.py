### Get endpoint MAC address info from CloudVision
### Mike Baker mbaker@arista.com
### 
### python3 scripts/get_endpoint_info.py --apiserver www.cv-staging.corp.arista.io:443 --auth token,nr.tok --input-file inputmacs.txt --output-file endpoints.csv
### 
### Based on examples from https://github.com/aristanetworks/cloudvision-python
###

from cloudvision.Connector.grpc_client import GRPCClient, create_query
from concurrent.futures import ThreadPoolExecutor
from parser import base
from pprint import pprint
import copy
import requests
import csv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

debug = False
emptyEndpoint = {'device': '',
                 'interface': '',
                 'vlanId': None,
                 'timestamp': ''}
endpointDict = {}


def get(client, dataset, pathElts):
    ''' Returns a query on a path element'''
    result = {}
    query = [
        create_query([(pathElts, [])], dataset)
    ]

    for batch in client.get(query):
        for notif in batch["notifications"]:
            if debug:
                pprint(notif["updates"])
            result.update(notif["updates"])
    return result


def getSwitchesInfo(client):
    ''' Get the inventory (actively streaming devices)
    '''
    pathElts = [
        "DatasetInfo",
        "Devices"
    ]
    dataset = "analytics"
    return get(client, dataset, pathElts)


def get_endpointlocation(macAddr, server, inventory, tokenFile):
    ''' Get the endpoint location for a MAC address
    '''
    endpoint_url = "/api/resources/endpointlocation/v1/EndpointLocation"
    queryParam = "?key.searchTerm={}".format(macAddr)
    head = {'Authorization': 'Bearer {}'.format(tokenFile)}
    url = "https://" + server + endpoint_url + queryParam
    r = requests.get(url, headers=head, verify=False)
    response = [r.json()]
    if len(response) == 1:
        deviceMap = response[0]['value']['deviceMap']['values']
        if len(deviceMap) == 1:
            for deviceKey, deviceVal in deviceMap.items():
                if 'locationList' in deviceVal:
                    locationList = deviceVal['locationList']['values']
                    if len(locationList) > 0:
                        topLocation = locationList[0]
                        device = topLocation['deviceId']
                        endpointDict[macAddr]['device'] = inventory[device]['hostname']
                        endpointDict[macAddr]['interface'] = topLocation['interface']
                        endpointDict[macAddr]['vlanId'] = topLocation['vlanId']
                        endpointDict[macAddr]['timestamp'] = topLocation['learnedTime']


def main(apiserverAddr, output_file, token=None, certs=None, key=None, ca=None):

    with GRPCClient(apiserverAddr, token=token, key=key,
                    ca=ca, certs=certs) as client:
        switches_info = getSwitchesInfo(client)
        switches = list(switches_info.keys())

    # Get location for each endpoint
    futures_list = []
    with ThreadPoolExecutor(max_workers=40) as executor:
        for macAddr, _ in endpointDict.items():
            futures = executor.submit(get_endpointlocation, macAddr, server, switches_info,
                                      tokenFile)
            futures_list.append(futures)

    # Build the CSV
    csv_columns = ['MAC', 'Device', 'Interface', 'VlanID', 'Timestamp']
    csv_file = args.output_file
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(csv_columns)
            for macAddr, endpointVals in endpointDict.items():
                writer.writerow([macAddr,
                                 endpointVals['device'],
                                 endpointVals['interface'],
                                 str(endpointVals['vlanId']),
                                 endpointVals['timestamp']])
    except IOError:
        print('I/O error')
        print(endpointDict)

    return 0


if __name__ == "__main__":
    base.add_argument("--input-file", required=True, type=str,
                      help="input file for endpoint list")
    base.add_argument("--output-file", required=True, type=str,
                      help="output file for endpoint list")
    args = base.parse_args()
    with open(args.input_file) as f:
        for line in f:
            macAddr = line.strip()
            if macAddr:
                endpointDict[macAddr] = copy.deepcopy(emptyEndpoint)
    server = args.apiserver.split(":")[0]
    with open(args.tokenFile) as f:
        tokenFile = f.read().strip("\n")
    exit(main(args.apiserver, args.output_file, certs=args.certFile, key=args.keyFile,
              ca=args.caFile, token=args.tokenFile))
