import re #regex

class ip:
	def __init__(self, ipaddr):
		#TODO add in cidr mask as an optional extra variable
		if ipaddr.__class__ == str:
			#TODO if a /cidr is included, set that automatically
			if ipaddr[:7] == '::ffff:':
				ipaddr = ipaddr[7:]
			if re.match("^0*([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.0*([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.0*([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.0*([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])$",ipaddr): #regexp to find v4 address
				ocets = ipaddr.split(".")
				self.ip = (int(ocets[0])*16777216)+(int(ocets[1])*65536)+(int(ocets[2])*256)+(int(ocets[3])) + 0xffff00000000 # converts array of strings to ints and calculators int, along with adding the rfc part to make it an IPv6 encoded IPv4 address
				print self.ip
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
		if ipaddr.__class__ == long or ipaddr.__class__ == int:
			#if it's a long, don't change anything unless it's a v4 address, if it is add 0xffff00000000
			#this most likely breaks a thousand RFCs but I think this will be handy. The only exception being loop back (1). I presume the rest will just be people mistakening it for a v4 input.

			#TODO check is it's a IPv4 mask, and if so automatically set cidr
			if (ipaddr < 0xFFFFFFFF) and (ipaddr > 1):
				self.ip = ipaddr + 0xffff00000000
			else:
				self.ip = ipaddr
	def prettyprint(self):
		hexd = '%x' % (self.ip,)
		if self.ip > 0xffff00000000 and self.ip < 0xffffffffffff:
			parts = [hexd[sections:sections+4] for sections in range(0,len(hexd),4)] #TODO this could be cleaned up rather than using the hex could use real numbers and shiz....
			return "::ffff:" + str(int(parts[-2][:2], 16)) + "." + str(int(parts[-2][2:4], 16)) + "." + str(int(parts[-1][:2], 16)) + "." + str(int(parts[-1][2:4], 16))
		else:
			parts = [hexd[sections:sections+4] for sections in range(0,len(hexd),4)]
			if len(parts)==8:
				return ":".join(parts)
			else:
				return "::" + ":".join(parts)
	def network(self,mask):
		return 0
		#TODO given a mask return the network, and set the cidr
		#TODO detect if it's a cidr or net mask



print ip(0b1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111000000000000000000).prettyprint()

print ip(3671509009).prettyprint()
print ip("2001::1").prettyprint()
print ip("2001::abc:1").prettyprint()
print ip("2001:123::").prettyprint()
print ip("::1").prettyprint()
print ip("2001:0db8:85a3:0000:0000:8a2e:0370:7334").prettyprint()
print ip("10.1.1.1").prettyprint()
print ip("::ffff:10.1.1.1").prettyprint() #TODO fix this
