#!/usr/bin/python
#http://pysnmp.sourceforge.net/docs/4.x/index.html#SYNCH-ONELINER-APPS

#includes
from pysnmp.entity.rfc3413.oneliner import cmdgen

# functions
def hexify( octets ):
	return ":".join( [ '%x'%(ord(c)) for c in octets ]) #http://www.velocityreviews.com/forums/t320222-octet-string-conversion.html

def grabmacs (host,community):
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().nextCmd(
	cmdgen.CommunityData('my-agent', community, 0),
	cmdgen.UdpTransportTarget((host, 161)),
	(1,3,6,1,2,1,17,4,3,1,1))
	#http://www.cisco.com/en/US/tech/tk648/tk362/technologies_tech_note09186a00801c9199.shtml
	for varBind in varBinds:
		macid, mac = varBind[0]
		print "macid - " + macid.prettyPrint().split(".")[-1] + ", mac - " + hexify( mac)

def grabbridgeports (host, community):
        errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().nextCmd(
        cmdgen.CommunityData('my-agent', community, 0),
        cmdgen.UdpTransportTarget((host, 161)),
        (1,3,6,1,2,1,17,4,3,1,2))
        #http://www.cisco.com/en/US/tech/tk648/tk362/technologies_tech_note09186a00801c9199.shtml
        for varBind in varBinds:
                macid, portid = varBind[0]
                print "macid - " + macid.prettyPrint().split(".")[-1] + ", portid - " + str(portid)

def grabportnames (host,community):
	errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().nextCmd(
        cmdgen.CommunityData('my-agent', community, 0),
        cmdgen.UdpTransportTarget((host, 161)),
        (1,3,6,1,2,1,31,1,1,1,1))
        #http://www.cisco.com/en/US/tech/tk648/tk362/technologies_tech_note09186a00801c9199.shtml
        for varBind in varBinds:
                portid, portname = varBind[0]
		print "portid - " + portid.prettyPrint().split(".")[-1] + ", portname - " + portname


#testing
grabmacs("172.27.2.1","public")
grabbridgeports("172.27.2.1","public")
grabportnames("172.27.2.1","public")
