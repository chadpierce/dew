#!/usr/bin/env python3
# NAME: dew.py
# DESC: creates or deletes a digital ocean droplet
#       or lists all droplets and ids
#       using the DO api
# AUTHOR: https://github.com/chadpierce
# USAGE:
#   create droplet: python3 dew.py -c
#   delete droplet: python3 dew.py -d dropletID 
#   list droplets: python3 dew.py -l
#   list available images: python3 dew.py -i
#   show help: python3 dew.py -h
#
# TODO user data is iffy and needs testing
##################################################
import sys
import time
import requests
import json

# api_token - accounts > api > generate new token
# ssh_keys - settings > security > SSH Keys
# tags - use to automatically assign firewalls, etc

# vvv change this stuff vvv
api_token = '<YOUR TOKEN>'
ssh_key_fingerprint = '<YOUR FINGERPRINT>'
safe_droplets = [123, 456]  # ids of droplets you dont want to delete
droplet_name = 'pwnbox'  # default if you leave input blank
droplet_size = 's-1vcpu-1gb'  #cheapest $5 droplet
droplet_image = 'debian-10-x64'  # 'ubuntu-20-04-x64'
tag = 'pwn'
region = 'tor1'
user_data = ''  # this is populated in create_droplet()
auto_script = '''#!/bin/bash

apt-get -y update
apt-get -y install nmap wget curl tmux
touch /root/donezo
'''
# ^^^ change that stuff ^^^

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + api_token,
}

data = '{ \
    "name":"' + droplet_name + '", \
    "region":"' + region  + '", \
    "size":"' + droplet_size  + '", \
    "image":"' + droplet_image + '", \
    "ssh_keys":["' + ssh_key_fingerprint + '"], \
    "backups":false, \
    "ipv6":false, \
    "user_data":"' + user_data + '", \
    "private_networking":null, \
    "volumes": null, \
    "tags":["' + tag + '"] \
}'


def create_droplet():
    global droplet_name
    name_drop = input('enter droplet name (default is ' + droplet_name + ') => ')
    if name_drop != '':
        droplet_name = name_drop
    do_auto = input('include automated script (may not work)? (y or n) => ')
    if do_auto == 'n':
        user_data = ''
    elif do_auto == 'y':
        user_data = auto_script
    else:
        print('that was not y or n')
        sys.exit()
    response = requests.post('https://api.digitalocean.com/v2/droplets', headers=headers, data=data)
    jresp = response.json()
    droplet_id = jresp['droplet']['id']
    print('will generate droplet then sleep before getting IP...')
    print()
    print('droplet id: ' + str(droplet_id))
    time.sleep(10)
    response = requests.get('https://api.digitalocean.com/v2/droplets/' + str(droplet_id) + '/', headers=headers)
    jresp = response.json()
    ip1 = jresp['droplet']['networks']['v4'][0]['ip_address']  # TODO make this better
    iptype1 = jresp['droplet']['networks']['v4'][0]['type']
    ip2 = jresp['droplet']['networks']['v4'][1]['ip_address']
    iptype2 = jresp['droplet']['networks']['v4'][1]['type']
    if iptype1 == 'public':
        print('public ip: ' + str(ip1))
    elif iptype2 == 'public':
        print('public ip: ' + str(ip2))
    else:
        print('ERROR: no public ip? printing all ip4 info')
        print(jresp['droplet']['networks']['v4'])


def del_droplet(drop_id):
    if int(drop_id) in safe_droplets:
        print('you dont want to delete that one!')
    else:
        response = requests.delete('https://api.digitalocean.com/v2/droplets/' + drop_id, headers=headers)
        if response.status_code == 204:
            print('droplet deleted')
        else:
            print('ERROR: something went wrong!')


def list_droplets():
    response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)
    jresp = response.json()
    ipaddr = 'error: public ip not found' 
    print('name\t\tid\t\tip\n----------\t----------\t--------------')
    for d in jresp['droplets']:
        for i in range(len(d['networks']['v4'])):
            if d['networks']['v4'][i]['type'] == 'public':
                ipaddr = d['networks']['v4'][i]['ip_address']
        print(d['name'] + '\t\t' + str(d['id']) + '\t' + str(ipaddr))


def list_images():
    response = requests.get('https://api.digitalocean.com/v2/images', headers=headers)
    jresp = response.json()
    image_list = []
    for image in jresp['images']:
        for _ in range(len(image)):
            image_list.append(image['description'] + ' -- ' + image['slug'])
    res = []  # remove duplicates 
    [res.append(x) for x in image_list if x not in res]
    print(*res, sep='\n')


def print_help():
    help_str = '''
    dew.py switches:
      -c        create droplet
      -d id     delete droplet
      -l        list existing droplets
      -i        list available images
      -h        print this help
      '''
    print(help_str)

# start script        
if len(sys.argv) > 1:
    if sys.argv[1] == '-d':
        if len(sys.argv) == 3:
            if sys.argv[2].isnumeric():
                del_droplet(sys.argv[2])
            else:
                print('bad droplet id!')
        else:
            print('you need a droplet id to delete a droplet')
    elif sys.argv[1] == '-l' or sys.argv[1] == 'what':
        list_droplets()
    elif sys.argv[1] == '-c' or sys.argv[1] == 'create':
        create_droplet()
    elif sys.argv[1] == '-i':
        list_images()
    elif sys.argv[1] == '-h':
        print_help()
    else:
        print('bad switch try again')
elif len(sys.argv) == 1:
    print_help()
else:
    add_droplet()
