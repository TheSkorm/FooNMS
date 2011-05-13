#!/usr/bin/python
import getmacs
import getarps
macs = getmacs.getmacs("172.27.2.1","public") #contains macs - port name
arps = getarps.getarps("172.27.2.1","public") #contains mac - ip

for mac in macs:
	if mac in arps: # do this if we have an IP address
		print mac + " - " + macs[mac] + " - " +  arps[mac] 
	else: #else we'll just add in the mac address
		print mac + " - " + macs[mac]
