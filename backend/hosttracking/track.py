#!/usr/bin/python
import getmacs
import getarps
import datetime 

#http://code.activestate.com/recipes/66517-ip-address-conversion-functions-with-the-builtin-s/
import socket, struct


# "convert decimal dotted quad string to long integer"
def dottedQuadToNum(ip):
    return struct.unpack('!L',socket.inet_aton(ip))[0]

# "convert long int to dotted quad string"
def numToDottedQuad(n):
    return socket.inet_ntoa(struct.pack('L',n))



from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
engine = create_engine('mysql://foonms:foonms@localhost/foonms', echo=False)
from sqlalchemy import Table, Column, BigInteger, Integer, String, MetaData, ForeignKey, DateTime
metadata = MetaData()

mac_table = Table('macs', metadata,
Column('macaddress', String(50),primary_key=True),
Column('portname', String(50),primary_key=True),
Column('switch', BigInteger(unsigned=True),primary_key=True),
Column('time', DateTime)
)

arp_table = Table('arps', metadata,
Column('macaddress', String(50),primary_key=True),
Column('ipaddress', BigInteger(unsigned=True),primary_key=True),
Column('hostname', String(50),primary_key=True),
Column('router', BigInteger(unsigned=True),primary_key=True),
Column('time', DateTime)
)


metadata.create_all(engine) 

class macdata(object):
	def __init__(self, macaddress,portname,switch,time):
		self.macaddress = macaddress
		self.portname = portname
		self.switch = switch
		self.time = time

	def __repr__(self):
		return "<User('%s','%s', '%s')>" % ( self.macaddress, self.portname, self.switch, self.time)

class arpdata(object):
	def __init__(self, macaddress, ipaddress, hostname,router,time):
		self.macaddress = macaddress
		self.ipaddress = ipaddress
		self.hostname = hostname
		self.router = router
		self.time = time

	def __repr__(self):
		return "<User('%s','%s', '%s')>" % ( self.macaddress, self.ipaddress, self.hostname, self.router, self.time)


mapper(arpdata, arp_table) 
mapper(macdata, mac_table) 

Session = sessionmaker(bind=engine)

def getdata(switch,community):
	macs = getmacs.getmacs(switch,community) #contains macs - port name
	arps = getarps.getarps(switch,community) #contains mac - ip

	for mac in macs:
		session = Session()
		for instance in session.query(macdata).filter_by(macaddress = mac): 
			session.delete(instance)
		session.commit()
		addmac = macdata(None,None,None,None)
		print mac
		addmac.macaddress = mac
		addmac.portname = str(macs[mac])
		addmac.time = datetime.datetime.utcnow()
		addmac.switch = dottedQuadToNum(switch)
		session.add(addmac)
		session.commit()

	for mac in arps:
		session = Session()
		ip = dottedQuadToNum(arps[mac])
		for instance in session.query(arpdata).filter_by(ipaddress = ip): 
			session.delete(instance)
		session.commit()
		addarp = arpdata(None,None,None,None, None)
		addarp.ipaddress = ip
		print ip
		addarp.macaddress = mac
		addarp.hostname = "TBA"
		addarp.time = datetime.datetime.utcnow()
		addarp.router = dottedQuadToNum(switch)
		session.add(addarp)
		session.commit()

getdata("172.27.2.1","public")
getdata("172.27.2.43","public")
#getdata("172.19.64.254","public")
#getdata("172.19.65.2","public")
