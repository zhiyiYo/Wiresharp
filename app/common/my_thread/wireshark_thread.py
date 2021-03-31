# coding:utf-8
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from scapy.all import sniff, Packet, IP
from scapy.contrib.mqtt import MQTTPublish


class WiresharkThread(QThread):
    """ 抓包线程 """

    catchPacketSignal = pyqtSignal(dict)
    wiresharkStateChangedSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 数据包目标端口
        self.sniffPort = 1883
        # 抓包标志位
        self.isStopWiresharp = True

    def run(self):
        """ 开始抓包 """
        sniff(filter=f'dst port {self.sniffPort}', prn=self.on_wireshark,
              stop_filter=lambda x: x.haslayer(MQTTPublish) or self.isStopWiresharp)

    def on_wireshark(self, packet: Packet):
        """ 抓包回调函数 """
        if not packet.haslayer(MQTTPublish):
            return
        packetInfo = {}
        # 约定使用 utf-8 编码
        packetInfo['topic'] = packet.topic.decode('gbk')
        packetInfo['msg'] = packet.value.decode('gbk')
        packetInfo['src host'] = str(packet[IP].src)
        packetInfo['dst host'] = str(packet[IP].dst)
        # 发送信号给主界面
        self.wiresharkStateChangedSignal.emit('🤩 抓到包啦')
        self.wiresharkStateChangedSignal.emit(
            f"源主机： {packetInfo['src host']}")
        self.wiresharkStateChangedSignal.emit(
            f"目标主机： {packetInfo['dst host']}")
        self.wiresharkStateChangedSignal.emit(
            f"主题： {packetInfo['topic']}")
        self.wiresharkStateChangedSignal.emit(
            f"消息：\n {packetInfo['msg']}")
        self.catchPacketSignal.emit(packetInfo)
        self.stopWireshark()

    def startWireshark(self):
        """ 开始抓包 """
        if not self.isStopWiresharp:
            self.wiresharkStateChangedSignal.emit('😆 客官别急，还在抓包呢...')
            return
        self.wiresharkStateChangedSignal.emit('👿 正在抓包中...')
        self.isStopWiresharp = False
        self.start()

    def stopWireshark(self):
        """ 停止抓包 """
        self.wiresharkStateChangedSignal.emit('😈 已停止抓包')
        self.isStopWiresharp = True
