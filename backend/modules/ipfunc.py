class ip:
	def __init__(self, ipaddr):
		if ipaddr.__class__ == str:
			print "Is string"
			#detect if ipv4 or ipv6 and convert to long which becomes self.ip
			# this is the hard part... -_-
		if ipaddr.__class__ == long or ipaddr.__class__ == int:
			#if it's a long, don't change anything unless it's a v4 address, if it is add 0xffff00000000
			#this most likely breaks a thousand RFCs but I think this will be handy. The only exception being loop back (1). I presume the rest will just be people mistakening it for a v4 input.
			if (ipaddr < 0xFFFFFFFF) and (ipaddr > 1):
				self.ip = ipaddr + 0xffff00000000
			else:
				self.ip = ipaddr
	def prettyprint(self):
		if self.ip > 0xffff00000000 and self.ip < 0xffffffffffff:
			hexd = hex(self.ip)[2:]
			if hexd[-1] == "L":
				hexd = hexd[:-1]
			parts = [hexd[sections:sections+4] for sections in range(0,len(hexd),4)]
			return "::ffff:" + str(int(parts[-2][:2], 16)) + "." + str(int(parts[-2][2:4], 16)) + "." + str(int(parts[-1][:2], 16)) + "." + str(int(parts[-1][2:4], 16))
		else:
			hexd = hex(self.ip)[2:].strip("L")
			parts = [hexd[sections:sections+4] for sections in range(0,len(hexd),4)]
			if len(parts)==8:
				return ":".join(parts)
			else:
				return "::" + ":".join(parts)
		#detect if IPv6 or IPv4 and print nicely
	def bprint(self):
		return 0
		#return string of 1/0's for debugging
	def network(self,mask):
		return 0
		#given a mask print the network


print ip(0b1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111000000000000000000).prettyprint()

print ip(3671509009).prettyprint()


