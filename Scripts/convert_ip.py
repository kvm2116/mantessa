"""
This is a python script to convert a whitelist with each row having a range of
IP addresses to CIDR notation. At the same time, it counts and prints out the 
number of legal IP addresses within the file

Author: Niloofar Bayat
        (nb2776@columbia.edu)
"""
from netaddr import *
import csv
import socket

def ip2int(addr1, addr2):                                                               
    #return struct.unpack("!I", socket.inet_aton(addr))[0]    
    ip1 = long(0) 
    ip2 = long(0)                  
    try:
    	ip1 = long(IPAddress(unicode(addr1, "utf-8")))
    	ip2 = long(IPAddress(unicode(addr2, "utf-8")))
    except core.AddrFormatError:
    	return 0	
    return ip2 - ip1

def int2ip(addr):                                                               
    return socket.inet_ntoa(struct.pack("!I", addr)) 

result = 0

with open('CCCS_ranges.csv', 'rU') as f1:# open ('non_comcast_converted.csv', 'w') as f2:
    reader = csv.reader(f1, delimiter=',')
    #csv_static = csv.writer(f2)

    for row in reader:
        #print row
        cidrs = iprange_to_cidrs(row[0].strip(),row[1].strip())
        
        k = ip2int(row[0].strip(), row[1].strip())
        result += k
     #   if k != 0:
      #      csv_static.writerow([str(cidrs[0])])

print result
