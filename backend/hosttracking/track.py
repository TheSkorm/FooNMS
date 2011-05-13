#!/usr/bin/python
import getmacs
import getarps
import time 

from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
engine = create_engine('sqlite:///:memory:', echo=True)
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Time
metadata = MetaData()

users_table = Table('tracking', metadata,
Column('ipaddress', Integer,primary_key=True),
Column('hostname', String(50),primary_key=True),
Column('macaddress', String(50),primary_key=True),
Column('portname', String(50),primary_key=True),
Column('time', Time,primary_key=True)
)

metadata.create_all(engine) 

class trackdata(object):
	def __init__(self, ipaddress, hostname, macaddress,portname,time):
		self.ipaddress = ipaddress
		self.hostname = hostname
		self.macaddress = macaddress
		self.portname = portname
		self.time = time

	def __repr__(self):
		return "<User('%s','%s', '%s')>" % (self.ipaddress, self.hostname, self.macaddress, self.portname, self.time)

mapper(trackdata, users_table) 

Session = sessionmaker(bind=engine)
session = Session()
addtrack = trackdata(54, "test","testmac","portnam",time.time())
session.add(addtrack)
session.commit()
#macs = getmacs.getmacs("172.27.2.1","public") #contains macs - port name
#arps = getarps.getarps("172.27.2.1","public") #contains mac - ip

#for mac in macs:
#	if mac in arps: # do this if we have an IP address
#		print mac + " - " + macs[mac] + " - " +  arps[mac] 
#	else: #else we'll just add in the mac address
#		print mac + " - " + macs[mac]
