#!/usr/bin/python

# Script to help deploy my XSS challenge network
#
# Drew Kirkpatrick
# drew.kirkpatrick@gmail.com
# @hoodoer

import digitalocean
import json
import requests

TOKEN      = ""
GUAC_IMAGE = "Guacamole-Dip Server"
DEV_IMAGE  = "SecTalks-WP-XSS-ChallengeBox"
REGION     = "sgp1"

GUAC_SIZE  = "s-2vcpu-2gb"
DEV_SIZE   = "s-2vcpu-4gb"


API_URL    = "https://api.digitalocean.com/v2/"
headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(TOKEN)}


# How many participants to support
NUM_DEVBOXES = "1"



def local_get_all_tags():
	api_url = '{0}tags'.format(API_URL)

	response = requests.get(api_url, headers=headers)
	if response.status_code >= 500:
		print('[!] [{0}] Server Error'.format(response.status_code))
		return None
	elif response.status_code == 404:
		print('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url))
		return None  
	elif response.status_code == 401:
		print('[!] [{0}] Authentication Failed'.format(response.status_code))
		return None
	elif response.status_code == 400:
		print('[!] [{0}] Bad Request'.format(response.status_code))
		return None
	elif response.status_code >= 300:
		print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
		return None
	elif response.status_code == 200:
		tags = json.loads(response.content.decode('utf-8'))
		return tags
	else:
		print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
	return None

# curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer " -d '{"name":"example.com","region":"nyc3","size":"s-1vcpu-1gb","image":"ubuntu-16-04-x64","ssh_keys":[107149],"backups":false,"ipv6":true,"user_data":null,"private_networking":null,"volumes": null,"tags":["web"]}' "https://api.digitalocean.com/v2/droplets" 



manager      = digitalocean.Manager(token=TOKEN)
my_droplets  = manager.get_all_droplets()
my_snapshots = manager.get_all_snapshots()
my_keys      = manager.get_all_sshkeys()
#my_tags      = manager.get_all_tags()


print(my_keys)


my_tags = local_get_all_tags()


print(my_tags)

#print(my_tags)



# Parse out image IDs
for snapshot in my_snapshots:
	if snapshot.name == GUAC_IMAGE:
		GUAC_SNAPSHOT = snapshot.id

	if snapshot.name == DEV_IMAGE:
		DEV_SNAPSHOT = snapshot.id


# Parse out ssh key
#counter = 0
#for key in my_keys:
#	if key.name == "Macbook":
#		print ("Macbook key index is: " + str(counter))
#		SSH_KEY_INDEX = counter
#		break
#	counter += 1


exit()


# Deploy droplets
# Needs tag needs ssh keys
guacDroplet = digitalocean.Droplet(token=TOKEN,
                               name='GuacServer',
                               region=REGION,
                               image=GUAC_SNAPSHOT,
                               size_slug=GUAC_SIZE,
                               backups=False,
                               private_networking=True,
                               monitoring=True,
                               ssh_keys=my_keys,
                               tags=my_tags)
guacDroplet.create()



actions = guacDroplet.get_actions()

print(actions)

for action in actions:
    action.load()
    # Once it shows complete, droplet is up and running
    print action.status


# DNS Setup


# Firewalls


# Droplet Config (ssh)

