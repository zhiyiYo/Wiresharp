import sys
import socket

from halo import Halo
from scapy.all import sniff, Packet, IP
from scapy.contrib.mqtt import MQTTPublish


def on_wireshark(packet: Packet):
    """ 抓包回调函数 """
    if not packet.haslayer(MQTTPublish):
        return

    global packet_info
    # 约定使用 utf-8 编码
    packet_info['topic'] = packet.topic.decode('gbk')
    packet_info['msg'] = packet.value.decode('gbk')
    packet_info['src host'] = str(packet[IP].src)
    packet_info['dst host'] = str(packet[IP].dst)
    print('抓到宝了：',packet_info)


sniff_port = 1883
packet_info = {'topic': '', 'msg': ''}

spinner = Halo('正在抓包...', spinner='dots')
spinner.start()
# 开始抓包
sniff(filter=f'dst port {sniff_port}', prn=on_wireshark,
      stop_filter=lambda x: x.haslayer(MQTTPublish))
