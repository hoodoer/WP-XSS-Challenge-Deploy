#!/usr/bin/python


import digitalocean


TOKEN      = ""
GUAC_IMAGE = "Guacamole-Dip Server"
DEV_IMAGE  = "WP-XSS-ChallengeBox"
REGION     = "sgp1"


# How many participants to support
NUM_DEVBOXES = "1"



manager = digitalocean.Manager(token=TOKEN)
my_droplets = manager.get_all_droplets()
my_images = manager.get_my_images()


# Parse out image IDs
for i in my_images:
	print my_images[i]



# Deploy droplets
#droplet = digitalocean.Droplet(token=TOKEN,
 #                              name='GuacServer',
  #                             region=REGION,
   #                            image='ubuntu-14-04-x64', # Ubuntu 14.04 x64
    #                           size_slug='512mb',  # 512MB
     #                          backups=True)


# DNS Setup


# Firewalls


# Droplet Config (ssh)

print(my_droplets)
print(my_images)
