#Simple device manager

#Purpose:
# - Stores list of devices
# - Stores authincation methods
# - Stores wether the device is enabled or disabled

#Presumptions:
# - One device per IP address
# - Hostname not recorded as this can be found out using DNS at any stage. If DNS is incorrect and cannot be fixed, user can edit their host file to match requirements
# - MySQL backend
# - Test code to always return "True" on tests, to make it easy to find problems.
# - testing with sqlite for database design, will beed to adapt for MySQl support (varchar length)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///:memory:', echo=False) #change echo to true to enable SQL debugging
Session = sessionmaker(bind=engine)                    
Base = declarative_base()
class Device(Base):
    __tablename__ = 'devices'
    ip = Column(Integer, primary_key=True)
    auth = Column(String) # I unno about this yet (Maybe make another table)
    enabled = Column(Boolean)
    def __init__(self): #Either look up a device based on IP and load it's data, or create a new one
        Base.metadata.create_all(engine) #if the tables don't exist, create them
        self.ip = 0 #TODO actually look up a device, rather than creating one
        self.auth = "" #list of auth methods or something...
        self.enabled = True #Is this device active?

def edit(ip, session): #use this function to create / edit switch as it'll detect if a device is already in the database. An IP address for prim key has to be passed, along with a SQL Alc Session to do the look up and creation if not already added. Should be the same session that will later edit it.
    device = Device() #prep the tables
    our_device = session.query(Device).filter_by(ip=ip).first()
    session.commit()
    if (our_device.__class__ == None.__class__):
        device.ip = ip
        session.add(device)
        return device
    else:
        return our_device        
        
# Tests (add device, change from enabled to disabled - should be all True)
session = Session()

device = edit(5, session)
print device.enabled == True
device.enabled = False
print device.enabled == False
session.flush()
session.commit()


device2 = edit(5, session)
print device2.enabled == False
device2.enabled =True
print device2.enabled == True
session.flush()
session.commit()

device2 = edit(5, session)
print device2.enabled == True
device2.enabled =False
print device2.enabled == False
session.flush()
session.commit()

session.close()
session = Session()

device3 = edit(5, session)
print device3.enabled == False
device3.enabled =True
print device3.enabled == True
session.flush()
session.commit()

device3 = edit(5, session)
print device3.enabled == True
device3.enabled =False
print device3.enabled == False
session.flush()
session.commit()

