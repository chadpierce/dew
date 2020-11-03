# dew
simple digital ocean droplet creator, destroyer, and lister

 - intented for simplifying manangement of temporary throwaway boxes
 - create and destroy droplets on the fly
 - safe delete - add list of droplets you don't want to accidentally destroy
 - list existing droplets
 - list available droplet images 
 - includes optional automation script to kick off apt installations, etc at droplet creation

## Usage:  
 - update vars in script wish api key, etc
 - create droplet: python3 dew.py -c (some options hardcoded - edit varialbes in script to modify)                                                                                       
 - destroy droplet: python3 dew.py -d dropletID                                                                                                      
 - list droplets: python3 dew.py -l
 - list available images: python3 dew.py -i
 - show help: python3 dew.py -h

## how to get token, ssh keys, etc:
 In Digital Ocean console:
 - api_token - accounts > api > generate new token                                                                                                   
 - sh_keys - settings > security > SSH Keys                                                                                                         
 - tags - assign tags to machines to automatically assign firewalls, etc
