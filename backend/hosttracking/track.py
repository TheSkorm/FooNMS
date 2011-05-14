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
engine = create_engine('mysql://foonms:foonms@localhost/foonms', echo=True)
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime
metadata = MetaData()

users_table = Table('tracking', metadata,
Column('ipaddress', Integer(unsigned=True),primary_key=True),
Column('hostname', String(50),primary_key=True),
Column('macaddress', String(50),primary_key=True),
Column('portname', String(50),primary_key=True),
Column('switch', Integer(unsigned=True),primary_key=True),
Column('time', DateTime)
)

metadata.create_all(engine) 

class trackdata(object):
	def __init__(self, ipaddress, hostname, macaddress,portname,switch,time):
		self.ipaddress = ipaddress
		self.hostname = hostname
		self.macaddress = macaddress
		self.portname = portname
		self.switch = switch
		self.time = time

	def __repr__(self):
		return "<User('%s','%s', '%s')>" % (self.ipaddress, self.hostname, self.macaddress, self.portname, self.switch, self.time)

mapper(trackdata, users_table) 

Session = sessionmaker(bind=engine)

def getdata(switch,community):
	macs = getmacs.getmacs(switch,community) #contains macs - port name
	arps = getarps.getarps(switch,community) #contains mac - ip

	for mac in macs:
		session = Session()
		for instance in session.query(trackdata).filter_by(macaddress = mac): 
			session.delete(instance)
		session.commit()
		addtrack = trackdata(None,None,None,None,None,None)
		if mac in arps: # do this if we have an IP address
			addtrack.ipaddress = dottedQuadToNum(arps[mac])
		else: #else we'll just add in the mac address
			addtrack.ipaddress = 0
		addtrack.hostname = "TBA"
		addtrack.macaddress = mac
		addtrack.portname = str(macs[mac])
		addtrack.time = datetime.datetime.utcnow()
		addtrack.switch = dottedQuadToNum(switch)
		#addtrack = trackdata(dottedQuadToNum(arps[mac]), "hostname",mac,macs[mac],time.time())
		session.add(addtrack)
		session.commit()

getdata("172.27.2.1","public")
#getdata("172.19.64.254","public")
#getdata("172.19.65.2","public")
