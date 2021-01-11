# coding:utf-8
import os
import re
import socket
from typing import List,Tuple
from pprint import pprint

from scapy.all import srp, ARP
from scapy.layers.l2 import Ether
from ifaddr import get_adapters


def getIpWithMask() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('114.114.114.114', 80))
    ip = s.getsockname()[0]

    ipconfig = os.popen("ipconfig /all").read()
    res = re.findall(f'{ip}.*?\n.*?子网掩码.*?: (.*?)\n', ipconfig)
    mask = res[0]

    ipi = [int(i) for i in ip.split(".")]
    maski = [int(i) for i in mask.split(".")]

    maskb = ''.join([bin(i)[2:].zfill(8) for i in maski])
    x = 0
    while maskb[0] == '1':
        maskb = maskb[1:]
        x += 1

    networkSegmenti = [str(ipi[i] & maski[i]) for i in range(4)]
    networkSegment = '.'.join(networkSegmenti)+'/'+str(x)

    return networkSegment


def getHost() -> List[Tuple[str, str]]:
    """ 获取局域网内所有可连接主机的主机名和IP地址 """
    wlan = ''
    # 获取所有适配器名称
    adapters = get_adapters()
    # 获取无线网卡名称
    for adapter in adapters:
        if 'Wireless' in adapter.nice_name:
            wlan = adapter.nice_name
            break
    # 如果没有拿到网卡名称则报错
    if not wlan:
        raise Exception('无法找到无线网卡')
    # 发包以获取ip地址
    request = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=getIpWithMask())
    answers, unAnswers = srp(request, iface=wlan, timeout=5, verbose=False)
    # 根据ip地址获取主机名（不包括网关）
    host_dict = [(socket.getfqdn(recv.psrc), recv.psrc)
                 for send, recv in answers if not recv.psrc.endswith('.1')]
    return host_dict


if __name__ == "__main__":
    print(getHost())
