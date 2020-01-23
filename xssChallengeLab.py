#!/usr/bin/python3

# Script to help deploy and destroy my XSS challenge network
#
# Drew Kirkpatrick
# drew.kirkpatrick@gmail.com
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
USERNAME_BASE          = "potato"
USERNAME_NUMDIGITS     = 5







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



users = []
def getNewUsername():
	username = USERNAME_BASE + genRandomNumber(USERNAME_NUMDIGITS)
	while username in users:
		username = USERNAME_BASE + genRandomNumber(USERNAME_NUMDIGITS)
		# print("Reruning user generation due to: " + username)

	users.append(username)
	return username



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
parser.add_argument("--mapusers", help="Generate and map users to challenge droplets, generate guac user mapping file", action="store_true")
parser.add_argument("--genuserlist", type=int, help="Pre-generate a user/password list for distribution. Requires number to generate")
parser.add_argument("--mapuserlist", help="Map existing user/password list to droplets, generate guac user mapping file. Requires filename with user/password list")
parser.add_argument("--destroy", help="Destroy the challenge lab", action="store_true")

args = parser.parse_args()


if len(sys.argv) < 2:
	print("\nNeed at least one action\n")
	parser.print_help()
	exit()

counter = 0

if args.mapusers:
	counter += 1

if args.genuserlist:
	counter += 1

if args.mapuserlist:
	counter += 1

if args.destroy:
	counter += 1

if counter > 1:
	print("\nToo many arguments, only one action at a time please\n")
	parser.print_help()
	exit()




# Don't need a digital ocean connection for this
# Randomly generate users and password ahead of time,
# and they can be distributed. Save this to a file, 
# you can read it back in later at lab time to map
# to droplets
usersList     = []
passwordsList = []
if args.genuserlist:
	numUsers = args.genuserlist

	for x in range(numUsers):
		usersList.append(getNewUsername())
		passwordsList.append(genRandomString(14))

	for count in range(len(users)):
		print(str(count) + ", " + usersList[count] + ", " + passwordsList[count])
	exit()




# For the rest of these, we need a digital ocean API connection
print("Connecting to digital ocean to retrieve droplets...")
manager      = digitalocean.Manager(token=TOKEN)
my_droplets  = manager.get_all_droplets()
print("Done.\n\n")








# Read in user and passwords from a pre-generated file,
# then map these to droplets and create the guac user mapping file
if args.mapuserlist:
	print("Reading in user list from file: " + args.mapuserlist)
	fileHandle = open(args.mapuserlist, "r")
	usersFileRows = fileHandle.readlines()
	fileHandle.close()

	#print(usersFileRows)
	lineCounter = 0
	for line in usersFileRows:
		data = line.split(", ")
		usersList.append(data[1])
		passwordsList.append(data[2])
		# print("Line: " + str(lineCounter) + ", line: " + line)
		# lineCounter += 1


	for count in range(len(usersList)):
		print(str(count) + ", " + usersList[count] + ", " + passwordsList[count])


	# Ok, now need to pull droplets and do the mapping like the original func
	# And create the guac config
	exit()







if args.destroy:
	print("Oh boy, let's burn this shit down\n\n")
	if confirmDestroy():
		print("Confirmed, destroying the lab!\n")

		for droplet in my_droplets:
			if droplet.name == GUAC_DROPLET_NAME:
				print ("Destroying Guac Server...")
				droplet.destroy()

			if CHALLENGE_DROPLET_BASE in droplet.name:
				print ("Destroying " + droplet.name + "...")
				droplet.destroy()

		print("Lab is toast, don't forget to clean up DNS and API key at")
		exit()

	else:
		print("Wimp")
		exit()






# And the rest...
if args.mapusers:
	print("Mapping users to droplets...\n")



USERMAPPING = "<user-mapping>\n"
USERMAPPING += '	<authorize username="drew" password="' + genRandomString(14) +'">\n'
USERMAPPING += '''		<protocol>vnc</protocol>
        	<param name="hostname">10.130.126.197</param>
        	<param name="port">5901</param>
        	<param name="password">sa#k%%Gg88adKen</param>
    	</authorize>

'''

challengeUsers      = []
challengePasswords  = []
challengeServers    = []
challengePrivateIps = []

challengeCsvData = []


for droplet in my_droplets:
	if droplet.name == GUAC_DROPLET_NAME:
		print ("Guac Server private ip: " + droplet.private_ip_address)
		print("\n")

	if CHALLENGE_DROPLET_BASE in droplet.name:
		print (droplet.name + " has private ip: " + droplet.private_ip_address)
		print("\n")	
		username = getNewUsername()
		password = genRandomString(14)
		USERMAPPING += '\n 	<authorize username="' + username + '" password="' + password +'">\n'
		USERMAPPING += '''		<protocol>vnc</protocol>
        	<param name="hostname">''' + droplet.private_ip_address + '</param>\n'
		USERMAPPING += '''    		<param name="port">5901</param>
        	<param name="password">sa#k%%Gg88adKen</param>
    	</authorize>

		'''

		csvEntry = username + "," + password + "," + droplet.name + "," + droplet.private_ip_address
		challengeCsvData.append(csvEntry)


		# challengeUsers.append(username)
		# challengePasswords.append(password)
		# challengeServers.append(droplet.name)
		# challengePrivateIps.append(droplet.private_ip_address)



USERMAPPING += "\n</user-mapping>\n"

print("\n\n")
print (USERMAPPING)

print("\n\n")
print("\n\n")
print("CSV Data:")

for line in challengeCsvData:
	print(line)

