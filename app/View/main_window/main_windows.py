# coding:utf-8
from copy import deepcopy
from time import time

from app.common.functions.catch_packet import readCatchPacket, writeCatchPacket
from app.common.functions.get_host import getHost
from app.common.functions.user_info import getUserInfo
from app.common.my_thread import (ArpAttackThread, PublishThread,
                                  WiresharkThread)
from app.components.frameless_window import FramelessWindow
from app.View.dialog_interface import DialogInterface
from app.View.navigation_interface import NavigationInterface
from app.View.welcome_interface import WelcomeInterface
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QStackedWidget


class WireSharp(FramelessWindow):
    """ WireSharp 聊天界面 """

    BORDER_WIDTH = 5

    def __init__(self):
        super().__init__()
        self.__getContactInfo()
        self.userInfo = getUserInfo()
        # 实例化小部件
        t1 = time()
        print('🤖 正在初始化界面...')
        self.stackedWidget = QStackedWidget(self)
        self.dialogInterface = DialogInterface(self)
        self.welcomeInterface = WelcomeInterface(self)
        self.navigationInterface = NavigationInterface(
            self.contactInfo_list, self)
        print(f'✅ 完成界面的初始化，耗时{time()-t1:.2f}s')
        # 创建线程
        self.publishThread = PublishThread(self)
        self.wiresharkThread = WiresharkThread(self)
        self.arpAttackThread = ArpAttackThread(self)
        # 引用子窗口
        self.chatListWidget = self.navigationInterface.chatListWidget
        self.contactInterface = self.navigationInterface.contactInterface
        # 初始化界面
        self.__initWidget()

    def __initWidget(self):
        """ 初始化界面 """
        self.setWindowTitle('Wiresharp')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(r'app\resource\Image\icon\icon.png'))
        self.setAttribute(Qt.WA_TranslucentBackground | Qt.WA_StyledBackground)
        # 调整窗口大小和小部件位置
        self.navigationInterface.move(0, 40)
        self.stackedWidget.move(403, 40)
        self.resize(1279, 957)
        # 将窗口添加到层叠窗口中
        self.stackedWidget.addWidget(self.welcomeInterface)
        self.stackedWidget.addWidget(self.dialogInterface)
        # 在去除任务栏的显示区域居中显示
        desktop = QApplication.desktop().availableGeometry()
        self.move(int(desktop.width() / 2 - self.width() / 2),
                  int(desktop.height() / 2 - self.height() / 2))
        # 信号连接到槽函数
        self.__connectSignalToSlot()

    def __getContactInfo(self) -> list:
        """ 获取联系人信息 """
        print('🌍 正在获取局域网内的主机...')
        t1 = time()
        host_list = getHost()
        print(f'✅ 完成局域网内主机的获取，耗时{time()-t1:.2f}s')
        self.contactInfo_list = []
        self.headPortraitPath_list = [
            r'app\resource\Image\head_portrait\硝子（1）.png',
            r'app\resource\Image\head_portrait\硝子（2）.png',
            r'app\resource\Image\head_portrait\硝子（3）.jpg',
        ]
        for i, (hostName, IP) in enumerate(host_list):
            self.contactInfo_list.append({
                'IP': IP,
                'contactName': hostName,
                'headPortraitPath': self.headPortraitPath_list[i % len(self.headPortraitPath_list)]
            })

    def resizeEvent(self, e):
        """ 调整窗口大小 """
        super().resizeEvent(e)
        self.stackedWidget.resize(self.width() - 402, self.height() - 40)
        if hasattr(self, 'navigationInterface'):
            self.navigationInterface.resize(
                self.navigationInterface.width(), self.height()-40)

    def __connectSignalToSlot(self):
        """ 将信号连接到槽函数 """
        # 欢迎界面信号连接到槽函数
        self.welcomeInterface.changeUserInfoSignal.connect(
            self.__changeUserInfoSlot)
        self.welcomeInterface.startConvButton.clicked.connect(
            self.navigationInterface.switchToContactInterface)
        # todo:联系人界面信号连接到槽函数
        self.contactInterface.selectContactSignal.connect(
            self.__selectContactSlot)
        self.chatListWidget.currentChatChanged.connect(
            self.__currentChatChangedSlot)
        self.chatListWidget.deleteChatSignal.connect(self.__deleteChatSlot)
        # todo:会话界面信号连接到槽函数
        self.dialogInterface.sendMessageSignal.connect(self.__newMessageSlot)
        self.dialogInterface.recvMessageSignal.connect(self.__newMessageSlot)
        self.dialogInterface.publishSignal.connect(self.__publishSlot)
        self.dialogInterface.startWiresharkSignal.connect(
            self.__startWiresharpSlot)
        self.dialogInterface.stopWiresharkSignal.connect(
            self.__stopWiresharpSlot)
        self.dialogInterface.startArpAttackSignal.connect(
            self.__startArpAttackSlot)
        self.dialogInterface.stopArpAttackSignal.connect(
            self.__stopArpAttackSlot)
        # todo:线程信号连接到槽函数
        self.wiresharkThread.catchPacketSignal.connect(self.__catchPacketSlot)
        self.wiresharkThread.wiresharkStateChangedSignal.connect(
            self.__wiresharpStateChangedSlot)
        self.arpAttackThread.arpAttackStateChangedSignal.connect(
            self.__arpAttackStateChangedSlot)
        self.publishThread.publishStateChangedSignal.connect(
            self.__publishStateChangedSlot)

    def __changeUserInfoSlot(self):
        """ 更新用户信息 """
        self.userInfo = getUserInfo()
        self.navigationInterface.updateUserInfo(self.userInfo)

    def __selectContactSlot(self, contactInfo: dict):
        """ 选中联系人时显示对话窗口 """
        # 如果选中的IP不在聊天列表已有的聊天用户中，就新建一个对话窗口
        IP = contactInfo['IP']
        if IP not in list(self.chatListWidget.IPContactName_dict.keys()) \
                + list(self.dialogInterface.IPIndex_dict.keys()):
            self.dialogInterface.addDialog(contactInfo)
        else:
            self.dialogInterface.setCurrentDialogByIP(IP)
        # 将当前窗口设置为对话界面
        self.stackedWidget.setCurrentWidget(self.dialogInterface)

    def __currentChatChangedSlot(self, IP: str):
        """ 当前选中的聊天框改变对应的槽函数 """
        self.dialogInterface.setCurrentDialogByIP(IP)
        self.stackedWidget.setCurrentWidget(self.dialogInterface)

    def __newMessageSlot(self, messageInfo: dict):
        """ 发送/接收 对话消息的槽函数 """
        IP = messageInfo['IP']
        # 如果对话框中没有当前的联系人对话记录，就创建一个新的聊天框，否则更新聊天框
        if IP not in self.chatListWidget.IPContactName_dict.keys():
            self.chatListWidget.addChatWidget(messageInfo)
        else:
            chatWidget, i = self.chatListWidget.findChatListWidgetByIP(
                IP, True)
            self.chatListWidget.setCurrentItem(
                self.chatListWidget.item_list[i])
            chatWidget.updateWindow(messageInfo)

    def __deleteChatSlot(self, IP: str):
        """ 删除对话框槽函数 """
        self.stackedWidget.setCurrentWidget(self.welcomeInterface)
        self.dialogInterface.removeDialog(IP)

    def __startWiresharpSlot(self, IP: str):
        """ 开始抓包 """
        self.arpAttackThread.stopArpAttack()
        self.arpAttackThread.startArpAttack(IP)
        self.wiresharkThread.startWireshark()

    def __stopWiresharpSlot(self):
        """ 停止抓包 """
        self.wiresharkThread.stopWireshark()
        self.arpAttackThread.stopArpAttack()

    def __catchPacketSlot(self, packetInfo: dict):
        """ 抓到包的槽函数 """
        self.arpAttackThread.stopArpAttack()
        self.dialogInterface.isArpAttack = False
        self.dialogInterface.isCatchingPacket = False
        # 将数据包保存到本地
        writeCatchPacket(packetInfo, 'app\\data\\catch_packet.json')
        with open(r'app\resource\html\send_file.html', encoding='utf-8') as f:
            self.__sendMessage(f.read())

    def __startArpAttackSlot(self, IP: str):
        """ 开始 ARP 欺骗槽函数(发送错误 MAC 地址) """
        self.arpAttackThread.startArpAttack(IP, False)

    def __stopArpAttackSlot(self):
        """ 开始 ARP 欺骗槽函数 """
        self.arpAttackThread.stopArpAttack()

    def __publishSlot(self):
        """ 发布消息槽函数 """
        packetInfo = readCatchPacket('app\\data\\catch_packet.json')
        if packetInfo:
            self.publishThread.publish(
                packetInfo['dst host'], packetInfo['topic'], packetInfo['msg'])
        else:
            self.__sendMessage('😋 当前没有抓到的包可供发布哦~')

    def __publishStateChangedSlot(self, message: str):
        """ 发布状态改变对应的槽函数 """
        self.__sendMessage(message)

    def __wiresharpStateChangedSlot(self, message: str):
        """ 显示 Wiresharp 线程发来的消息 """
        self.__sendMessage(message)

    def __arpAttackStateChangedSlot(self, message: str):
        """ 显示 ARP 攻击线程发来的消息 """
        self.__sendMessage(message)

    def __sendMessage(self, message: str):
        """ 作为contact发送消息 """
        messageInfo = deepcopy(self.dialogInterface.currentContactInfo)
        messageInfo['message'] = message
        messageInfo['time'] = QTime.currentTime().toString('H:mm')
        self.dialogInterface.receiveMessageSlot(messageInfo)
