import re #regex

#http://wiki.python.org/moin/BitManipulation

#used for subnetmask calcs
def bitLenCount(int_type):
    length = 0
    count = 0
    while (int_type):
        count += (int_type & 1)
        length += 1
        int_type >>= 1
    return count

# I got lazy, this should not require using a string
def cidr2int(cidr):
	return int("1"*cidr + "0"*(128-cidr),2)

class ip:
	def __init__(self, ipaddr, cidr_or_mask=None):	
		self.wasv4 = False			
		if ipaddr.__class__ == long or ipaddr.__class__ == int:
			#if it's a long, don't change anything unless it's a v4 address, if it is add 0xffff00000000
			#this most likely breaks a thousand RFCs but I think this will be handy. The only exception being loop back (1). I presume the rest will just be people mistakening it for a v4 input.
			#TODO check is it's a IPv4 mask, and if so automatically set cidr
			if (ipaddr < 0xFFFFFFFF) and (ipaddr > 1):
				self.ip = ipaddr + 0xffff00000000
				self.wasv4 = True
			else:
				self.ip = ipaddr
		if ipaddr.__class__ == str:
			#TODO if a /cidr is included, set that automatically
			if ipaddr[:7] == '::ffff:':
				ipaddr = ipaddr[7:]
			if re.match("^0*([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.0*([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.0*([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.0*([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])$",ipaddr): #regexp to find v4 address
				ocets = ipaddr.split(".")
				self.ip = (int(ocets[0])*16777216)+(int(ocets[1])*65536)+(int(ocets[2])*256)+(int(ocets[3])) + 0xffff00000000 # converts array of strings to ints and calculators int, along with adding the rfc part to make it an IPv6 encoded IPv4 address
				self.wasv4 = True
			if re.match("^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$",ipaddr):
				chunks = ipaddr.split(":")
				expanded = False
				hexstr = ""
				for chunk in chunks:
					hexstr += "0"*(4-len(chunk))+ chunk
					if chunk == "" and expanded == False:
						expanded = True
						hexstr += "0000" *(8-len(chunks))
 				self.ip = int(hexstr,16)
		self.cidr=cidr_or_mask
		if cidr_or_mask!=None:
			#TODO make sure it's a vaild mask.
			if re.match("^0*([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.0*([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.0*([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.0*([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])$",str(cidr_or_mask)): #check to see if mask or cidr
				ocets = cidr_or_mask.split(".")
				mask = (int(ocets[0])*16777216)+(int(ocets[1])*65536)+(int(ocets[2])*256)+(int(ocets[3])) # converts array of strings to ints and calculators int, along with adding the rfc part to make it an IPv6 encoded IPv4 address				
				self.cidr = 96 + bitLenCount(mask)
				self.mask = cidr2int(self.cidr)
			else:
				if int(cidr_or_mask) >= 0 or int(cidr_or_mask) <= 128: 
					if self.wasv4 == True:
						self.cidr = 96 + int(cidr_or_mask)
					else:
						self.cidr = int(cidr_or_mask)
					self.mask = cidr2int(self.cidr)
				else:
					print "something went wrong with the subnet supply"
					self.cidr = None
	def prettyprint(self):
		if self.cidr == None:
			pcidr = ""
		else:
			pcidr = "/" + str(self.cidr)
		hexd = '%x' % (self.ip,)
		if self.ip > 0xffff00000000 and self.ip < 0xffffffffffff:
			parts = [hexd[sections:sections+4] for sections in range(0,len(hexd),4)] #TODO this could be cleaned up rather than using the hex could use real numbers and shiz....
			return "::ffff:" + str(int(parts[-2][:2], 16)) + "." + str(int(parts[-2][2:4], 16)) + "." + str(int(parts[-1][:2], 16)) + "." + str(int(parts[-1][2:4], 16)) + pcidr
		else:
			parts = [hexd[sections:sections+4] for sections in range(0,len(hexd),4)]
			if len(parts)==8:
				return ":".join(parts) + pcidr
			else:
				return "::" + ":".join(parts) + pcidr
	def network(self,cidr=None):
		#must be provided as a IPv6 mask/cidr
		if cidr:		
			mask = cidr2int(cidr) 
		else:
			try:
				mask = cidr2int(self.cidr)
			except TypeError:
				return 0
				print "No cidr provided error"
		return self.ip & mask



print ip(0b1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111000000000000000000).prettyprint()

print ip(3671509009).prettyprint()
print ip(3671509009,24).prettyprint()
print ip("2001::1").prettyprint()
print ip("2001::abc:1").prettyprint()
print ip("2001:123::").prettyprint()
print ip("::1").prettyprint()
print ip(281474976710400).prettyprint()
print ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334").prettyprint()
print ip("10.1.1.1").prettyprint()
print ip("::ffff:255.255.255.0").prettyprint()
print ip(340282366920938463463374607431768211200).prettyprint()
print ip("10.0.0.0").ip
print ip("10.1.1.1",8).network()
print ip(ip("10.1.1.1",8).network()).prettyprint() #see what I did here, I put an IP inside an IP
print ip(ip("10.1.1.1",8).network(112)).prettyprint() #so I can address while I'm addressing
print ip(ip("10.1.1.1",8).mask).prettyprint()