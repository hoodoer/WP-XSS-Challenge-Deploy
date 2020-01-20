#!/usr/bin/python3

# Script to help deploy and destroy my XSS challenge network
#
# Drew Kirkpatrick
# drew.kirapt-get install python-dev libsasl2-dev gcckpatrick@gmail.com
# @hoodoer


import argparse
import sys
import digitalocean
import random
import string
from past.builtins import xrange

TOKEN      = ""

GUAC_DROPLET_NAME      = "guacserver"
CHALLENGE_DROPLET_BASE = "cdb"
USER_BASE              = "potato"







def genRandomString(length):
    password_charset = string.ascii_letters + string.digits + "?!@$%^*"

    if not hasattr(genRandomString, "rng"):
        genRandomString.rng = random.SystemRandom() # Create a static variable
    return ''.join([ genRandomString.rng.choice(password_charset) for _ in xrange(length) ])


def genRandomNumber(length):
	charset = string.digits

	if not hasattr(genRandomNumber, "rng"):
		genRandomNumber.rng = random.SystemRandom() # Create a static variable
	return ''.join([ genRandomNumber.rng.choice(charset) for _ in xrange(length) ])





def confirmDestroy():
	check = str(input("Are you _really_ sure you want to destroy the lab? (Y/N): ")).lower().strip()
	try:
		if check[0] == 'y':
			return True
		elif check[0] == 'n':
			return False
		else:
			print('Invalid Input')
			return confirmDestroy()
	except Exception as error:
		print("Please enter valid inputs you idiot")
		print(error)
		return confirmDestroy()







parser = argparse.ArgumentParser()
parser.add_argument("--mapusers", help="Map users to challenge droplets, generate guac user mapping file", action="store_true")
parser.add_argument("--destroy", help="Destroy the challenge lab", action="store_true")

args = parser.parse_args()


if len(sys.argv) < 2:
	parser.print_help()
	exit()


if args.mapusers and args.destroy:
	print("You cannot mapusers and destroy the lab at the same time idiot")
	parser.print_help()
	exit()



print("Connecting to digital ocean to retrieve droplets...")
manager      = digitalocean.Manager(token=TOKEN)
my_droplets  = manager.get_all_droplets()
print("Done.\n\n")



if args.mapusers:
	print("Mapping users to droplets...\n")

if args.destroy:
	print("Oh boy, let's burn this shit down\n\n")
	if confirmDestroy():
		print("Confirmed, destroying the lab!")

		for droplet in my_droplets:
			if droplet.name == GUAC_DROPLET_NAME:
				print ("Destroying Guac Server...")
				droplet.destroy()
				print("\n")

			if CHALLENGE_DROPLET_BASE in droplet.name:
				print ("Destroying " + droplet.name + "...")
				droplet.destroy()
				print ("\n")

		print("Lab is toast, don't forget to clean up DNS at some point")
		exit()

	else:
		print("You sissy, destroy that network!")
		exit()




USERMAPPING = "<user-mapping>\n"
USERMAPPING += '	<authorize username="drew" password="' + genRandomString(14) +'">\n'
USERMAPPING += '''		<protocol>vnc</protocol>
        	<param name="hostname">10.130.126.197</param>
        	<param name="port">5901</param>
        	<param name="password">sa#k%%Gg88adKen</param>
    	</authorize>

'''



for droplet in my_droplets:
	if droplet.name == GUAC_DROPLET_NAME:
		print ("Guac Server private ip: " + droplet.private_ip_address)
		print("\n")

	if CHALLENGE_DROPLET_BASE in droplet.name:
		print (droplet.name + " has private ip: " + droplet.private_ip_address)
		print("\n")
		USERMAPPING += '\n 	<authorize username="' + USER_BASE + genRandomNumber(5) + '" password="' + genRandomString(14) +'">\n'
		USERMAPPING += '''		<protocol>vnc</protocol>
        	<param name="hostname">''' + droplet.private_ip_address + '</param>\n'
		USERMAPPING += '''    		<param name="port">5901</param>
        	<param name="password">sa#k%%Gg88adKen</param>
    	</authorize>

		'''


USERMAPPING += "\n</user-mapping>\n"

print("\n\n")
print (USERMAPPING)
