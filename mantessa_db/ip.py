import socket, struct

def ip2long(ip):
    """
    Convert an IP string to long
    """
    try:
        packedIP = socket.inet_aton(ip)
        val = struct.unpack("!L", packedIP)[0]
    except Exception as e:
        val = -1
    return val

def long2ip(ip):
	return socket.inet_ntoa(struct.pack('!L', ip))

