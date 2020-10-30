# dew
simple digital ocean droplet creator, destroyer, and lister

 - intented for simplifying manangement of temporary throwaway boxes
 - create and destroy droplets on the fly
 - safe delete - add list of droplets you don't want to accidentally destroy
 - list existing droplets
 - list available droplet images 
 - note: the automation script is currently broken (i think it needs newlines)

## Usage:                                                                                                                                            
 - create droplet: python3 dew.py -c (some options hardcoded - edit varialbes in script to modify)                                                                                       
 - destroy droplet: python3 dew.py -d dropletID                                                                                                      
 - list droplets: python3 dew.py -l
 - list available images: python3 dew.py -i
 - show help: python3 dew.py -h

## how to get token, ssh keys, etc:
 - api_token - accounts > api > generate new token                                                                                                   
 - sh_keys - settings > security > SSH Keys                                                                                                         
 - tags - assign tags to machines to automatically assign firewalls, etc
