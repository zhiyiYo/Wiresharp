from scapy.all import srp, ARP, show_interfaces
from scapy.layers.l2 import Ether

wlan = 'Intel(R) Wireless-AC 9462'

request = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst='192.168.43.0/24')
answer, unAnswer = srp(request, iface=wlan, timeout=2, verbose=False)

for send, resv in answer:
    print(resv.psrc)