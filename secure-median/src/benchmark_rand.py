import federatedsecure.client

import random
import time 
import sys
import json
import configparser
import math

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


def input_data(high, size):
    data = [random.randint(1, high) for _ in range(size- 2)]
    # make sure lower and upper bounds are present
    data.append(1)
    data.append(high)
    return data


if __name__ == "__main__":
    
    # init
    INDEX = int(sys.argv[1])
    HIGH = int(sys.argv[2])
    SIZE = int(sys.argv[3])
    DATA = input_data(HIGH, SIZE) 
    CONFIG = get_config('./src/servers.cfg')
    
    # benchmark 
    start = time.time()
    result = secure_median(INDEX, DATA, CONFIG)
    stop = time.time()

    # store output
    result['duration'] = stop-start
    result['server'] = CONFIG['nodes'][int(sys.argv[1])]
    result['size'] = SIZE
    result['range'] = HIGH 
    print(json.dumps(result))
