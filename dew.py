#!/usr/bin/env python3
# NAME: dew.py
# DESC: creates or deletes a digital ocean droplet
#       or lists all droplets and ids
#       using the DO api
# AUTHOR: https://github.com/chadpierce
# USAGE:
#   create droplet: python3 do.py 
#   delete droplet: python3 do.py -d dropletID
#   list droplets: python3 do.py -l
#
# TODO: user input droplet name instead of hard coded
##################################################
import sys
import time
import requests
import json

# api_token - accounts > api > generate new token
# ssh_keys - settings > security > SSH Keys
# tags - use to automatically assign firewalls, etc

# vvv change this stuff vvv
api_token = 'TOKEN_HERE'
ssh_key_fingerprint = 'FINGERPRINT_HERE'
droplet_name = 'NAME_HERE'
droplet_size = 's-1vcpu-1gb'  #cheapest $5 droplet
droplet_image = 'ubuntu-20-04-x64'  #ubuntu for simplicity 
tag = 'TAG_HERE'
region = 'tor1'
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
    "user_data":null, \
    "private_networking":null, \
    "volumes": null, \
    "tags":["' + tag + '"] \
}'


def add_droplet():
    response = requests.post('https://api.digitalocean.com/v2/droplets', headers=headers, data=data)
    jresp = response.json()
    droplet_id = jresp['droplet']['id']
    print('will generate droplet then sleep before getting IP...')
    print()
    print('droplet id: ' + str(droplet_id))
    time.sleep(10)  # no idea how long this could take so playing it safe
    response = requests.get('https://api.digitalocean.com/v2/droplets/' + str(droplet_id) + '/', headers=headers)
    jresp = response.json()
    # not sure if public is always in the same position
    ip1 = jresp['droplet']['networks']['v4'][0]['ip_address']
    iptype1 = jresp['droplet']['networks']['v4'][0]['type']
    ip2 = jresp['droplet']['networks']['v4'][1]['ip_address']
    iptype2 = jresp['droplet']['networks']['v4'][1]['type']
    if iptype1 == 'public':
        print('public ip: ' + str(ip1))
    elif iptype2 == 'public':
        print('public ip: ' + str(ip2))
    else:
        print('error: no public ip? printing all ip4 info')
        print(jresp['droplet']['networks']['v4'])


def del_droplet(drop_id):
    response = requests.delete('https://api.digitalocean.com/v2/droplets/' + drop_id, headers=headers)
    if response.status_code == 204:
        print('droplet deleted')
    else:
        print('something went wrong!')


def list_droplets():
    response = requests.get('https://api.digitalocean.com/v2/droplets', headers=headers)
    jresp = response.json()
    #print(jresp)
    for d in jresp['droplets']:
        print(d['name'] + ' - ' + str(d['id']))
if len(sys.argv) > 1:
    if sys.argv[1] == '-d':
        if len(sys.argv) == 3:
            if sys.argv[2].isnumeric():
                del_droplet(sys.argv[2])
            else:
                print('bad droplet id!')
        else:
            print('you need a droplet id to delete a droplet')
    elif sys.argv[1] == '-l':
        list_droplets()
    else:
        print('bad switch try again')
else:
    print('creating droplet...')
    add_droplet()
