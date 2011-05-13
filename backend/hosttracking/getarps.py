#!/usr/bin/python
#snmpwalk -v2c -c public 172.27.2.1 .1.3.6.1.2.1.4.22.1.2
#http://www.cisco.com/en/US/tech/tk648/tk362/technologies_q_and_a_item09186a0080094bc0.shtml#q14b

#http://pysnmp.sourceforge.net/docs/4.x/index.html#SYNCH-ONELINER-APPS

#includes
from pysnmp.entity.rfc3413.oneliner import cmdgen

# functions
def hexify( octets ):
        return ":".join( [ '%x'%(ord(c)) for c in octets ]) #http://www.velocityreviews.com/forums/t320222-octet-string-conversion.html

def getarps (host,community):  #gets a list of mac addresses, returns a dict of macid and mac address
        errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().nextCmd(
        cmdgen.CommunityData('my-agent', community, 0),
        cmdgen.UdpTransportTarget((host, 161)),
        (1,3,6,1,2,1,4,22,1,2))
        table = {}
        #http://www.cisco.com/en/US/tech/tk648/tk362/technologies_tech_note09186a00801c9199.shtml
        for varBind in varBinds:
		ip, mac = varBind[0]
		ip = '.'.join(ip.prettyPrint().split(".")[-4:]) #this grabs the four last legits from the oid, which is reconstructed into the IP address
                table[hexify(mac)] = ip
        return(table)
