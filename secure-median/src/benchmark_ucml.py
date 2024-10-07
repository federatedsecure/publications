import federatedsecure.client

import time 
import sys
import json
import configparser
import pandas as pd

def get_config(file):

    config = configparser.ConfigParser()
    config.read(file)
    uuid = config['UUID']['uuid']
    nodes =[]
    for section in config.sections():
        if section.startswith('SERVER'):
            nodes.append(f"{config.get(section, 'host')}:{config.get(section, 'port')}")

    return {'uuid':uuid, 'nodes':nodes}

def secure_median(my_index, my_data, config):
    
    my_node = config['nodes'][my_index]
    my_network = {'nodes': config['nodes'],
                  'uuid': config['uuid'],
                  'myself': my_index}
    api = federatedsecure.client.Api(my_node)
    microservice = api.create(protocol="Simon")
    result = microservice.compute(microprotocol="SecureMedian", data=my_data, network=my_network)
    return api.download(result)

def input_data(file, column):
    return pd.read_csv('./data/'+file)[column].to_list()

if __name__ == "__main__":
    INDEX = int(sys.argv[1])
    DATA = input_data(sys.argv[2], sys.argv[3]) 
    CONFIG = get_config('./src/servers.cfg')
    start = time.time()
    result = secure_median(INDEX, DATA, CONFIG)
    stop = time.time()
    result['duration'] = stop-start
    result['server'] = CONFIG['nodes'][int(sys.argv[1])]
    result['file'] = sys.argv[2]
    print(json.dumps(result))
