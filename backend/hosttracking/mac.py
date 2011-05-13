#!/usr/bin/python
#http://pysnmp.sourceforge.net/docs/4.x/index.html#SYNCH-ONELINER-APPS

#includes
from pysnmp.entity.rfc3413.oneliner import cmdgen

# functions
def hexify( octets ):
	return ":".join( [ '%x'%(ord(c)) for c in octets ]) #http://www.velocityreviews.com/forums/t320222-octet-string-conversion.html

def grabmacs (host,community):	#gets a list of mac addresses, returns a dict of macid and mac address
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().nextCmd(
	cmdgen.CommunityData('my-agent', community, 0),
	cmdgen.UdpTransportTarget((host, 161)),
	(1,3,6,1,2,1,17,4,3,1,1))
	table = {}
	#http://www.cisco.com/en/US/tech/tk648/tk362/technologies_tech_note09186a00801c9199.shtml
	for varBind in varBinds:
		macid, mac = varBind[0]
		table[macid.prettyPrint().split(".")[-1]] = hexify(mac)
	return(table)

def grabbridgeports (host, community): #grabs a list of macid and port numbers. returns a dict of macid and portid
        errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().nextCmd(
        cmdgen.CommunityData('my-agent', community, 0),
        cmdgen.UdpTransportTarget((host, 161)),
        (1,3,6,1,2,1,17,4,3,1,2))
	table = {}
        #http://www.cisco.com/en/US/tech/tk648/tk362/technologies_tech_note09186a00801c9199.shtml
        for varBind in varBinds:
                macid, portid = varBind[0]
                table[macid.prettyPrint().split(".")[-1]] = portid
	return(table)

def grabportnames (host,community): #grabs a list of portnames. returns a portid and a human name of the port as a dict
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().nextCmd(
        cmdgen.CommunityData('my-agent', community, 0),
        cmdgen.UdpTransportTarget((host, 161)),
        (1,3,6,1,2,1,31,1,1,1,1))
	table = {}
        #http://www.cisco.com/en/US/tech/tk648/tk362/technologies_tech_note09186a00801c9199.shtml
        for varBind in varBinds:
                portid, portname = varBind[0]
		table[portid.prettyPrint().split(".")[-1]] = portname
	return(table)

def getdata(host,community):
	macs = grabmacs(host,community)
	bridgeports = grabbridgeports(host,community)
	portnames = grabportnames(host,community)
	for mac in macs:
		print macs[mac] +" - "+ portnames[str(bridgeports[mac])]
		
#testing
#print grabmacs("172.27.2.1","public")
#print grabbridgeports("172.27.2.1","public")
#print grabportnames("172.27.2.1","public")
getdata("172.27.2.1","public")
