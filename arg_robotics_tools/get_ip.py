# AUTOGENERATED! DO NOT EDIT! File to edit: 04_get_ip.ipynb (unless otherwise specified).

__all__ = ['whoami', 'get_key', 'get_xbee_address', 'get_xbee_address_boat', 'find_duckiepond_devices_yaml',
           'dp_load_config', 'dp_get_devices', 'ssh_ping_nano', 'ssh_ping_rpi', 'test_ssh_intranet', 'ssh_connection',
           'test_ssh', 'ip_connection', 'test_ping', 'ssh_rostopic', 'test_rostopic']

# Cell
import subprocess
import os
import yaml
import re

def whoami(data):

    ret_byte = subprocess.check_output(['ifconfig'])
    ret_str = ret_byte.decode('utf-8')
    # Cut string from 'equal symbol' to 'degree C symbol', then convert to float
    en = ret_str[ret_str.find('eno1:'): ret_str.find('lo')]
    ip = en[en.find('inet')+5: en.find('netmask')-2]
    machine,device = get_key(data,ip)
    return machine,device

def get_key(dict,value):

    for k, v in dict.items():
        for v,v1 in v.items():
            for v1,v2 in v1.items():
                if v2 == value:
                    return k,v

def get_xbee_address(dict,value):
    for k, v in dict.items():
        for v,v1 in v.items():
            for v1,v2 in v1.items():
                if v2 == value:
                    address = dict[k]["rpi"]['xbee_rx']
                    return address

def get_xbee_address_boat(dict,value):
    pair_device = dict[value]["xbee"]["xbee_pair"]
    address = dict[pair_device]["rpi_2"]["xbee_rx"]
    return address

def find_duckiepond_devices_yaml(yaml_filename="duckiepond-devices.yaml"):
    dp_yaml_path = ""
    for root, dirs, files in os.walk(os.path.expanduser('~')):
        for name in files:
            if name == yaml_filename:
                dp_yaml_path = os.path.abspath(os.path.join(root, name))
                break
    return dp_yaml_path

def dp_load_config(dp_yaml_path):
    dp_dict = {}
    with open(dp_yaml_path, 'r') as stream:
        try:
            dp_dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return dp_dict

def dp_get_devices(dp_yaml_path, pattern='boat*'):
    dp_dict = dp_load_config(dp_yaml_path)
    boats = []
    for key in dp_dict.keys():
        match = re.match(pattern, key)
        if match:
            boats.append(key)
    return boats

#ssh functions will not give testing example for now on, since hostname will depend on your running machine

def ssh_ping_nano(hostname):
    response = os.system("ssh $USER@" + hostname + " ping -c 1 192.168.0.100")
    return response

def ssh_ping_rpi(hostname):
    response = os.system("ssh $USER@" + hostname + " ping -c 1 192.168.0.101")
    return response

def test_ssh_intranet():
    error = []
    for ip in hostnames:
        num = ssh_ping_rpi(ip)
        if num!=0:
            error.append("ssh ping rpi error " + ip)
        num = ssh_ping_nano(ip)
        if num!=0:
            error.append("ssh ping nano error " + ip)
    assert not error, "errors occured:\n{}".format("\n".join(error))

def ssh_connection(hostname):
    response = os.system("ssh $USER@" + hostname + " date")
    return response

def test_ssh():
    error = []
    for ip in hostnames:
        num = ssh_connection(ip)
        if num != 0:
            error.append("ssh error " + ip)
    assert not error, "errors occured:\n{}".format("\n".join(error))

def ip_connection(hostname):
    response = os.system("ping -c 1 " + hostname)
    return response

def test_ping():
    error = []
    for ip in hostnames:
        num = ip_connection(ip)
        if num != 0:
            error.append("Network Error " + ip)
    assert not error, "errors occured:\n{}".format("\n".join(error))

def ssh_rostopic(hostname, rosversion="melodic"):
    response = os.system('ssh $USER@' + hostname + ' "source /opt/ros/"' + rosversion + '"/setup.bash && rostopic list"')
    return response

def test_rostopic():
    error = []
    for ip in hostnames:
        num = ssh_rostopic(ip)
        if num != 0:
            error.append("ssh rostopic list error " + ip)
    assert not error, "errors occured:\n{}".format("\n".join(error))
