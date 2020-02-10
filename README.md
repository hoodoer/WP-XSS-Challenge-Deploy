# WP-XSS-Challenge-Deploy
Python script to help automate deployment of XSS challenge infrastructure

You can easily setup the guac server and the number of desired challenge boxes. Then setup guac DNS.

Then use this script to generate the guac usermapping. 

This script will also destroy the lab when your done (but not clean up the DNS)

You can also generate users ahead of time, and then map those users to a droplet later.

This script assumes you've setup DNS for the guac server seperately, you created the 
the droplets manually, with appropriate tags to set the desired firewall. 
You also need private networking enabled for challenge boxes and the guacamole server. 

It also ssh's into the challenge boxes to add the needed hosts file entries to make the
local application work. 
