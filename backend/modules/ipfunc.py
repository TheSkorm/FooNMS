class ip:
	def __init__(self, ipaddr):
		if ipaddr.__class__ == str:
			print "Is string"
			#detect if ipv4 or ipv6 and convert to long which becomes self.ip
		if ipaddr.__class__ == long or ipaddr.__class__ == int:
			#if it's a long, don't change anything unless it's a v4 address, if it is add 0xffff00000000
			#this most likely breaks a thousand RFCs but I think this will be handy. The only exception being loop back (1). I presume the rest will just be people mistakening it for a v4 input.
			if (ipaddr < 0xFFFFFFFF) and (ipaddr > 1):
				self.ip = ipaddr + 0xffff00000000
			else:
				self.ip = ipaddr
	def prettyprint(self):
		return ":".join([hex(self.ip)[2:][sections:sections+4] for sections in range(0,len(hex(a))-4,4)])
		#detect if IPv6 or IPv4 and print nicely
	def bprint(self):
		return 0
		#return string of 1/0's for debugging
	def network(self,mask):
		return 0
		#given a mask print the network


print ip(800).ip
