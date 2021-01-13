# coding:utf-8
from time import time
from ctypes import POINTER, cast
from ctypes.wintypes import HWND, MSG, POINT
from copy import deepcopy

from PyQt5.QtCore import Qt, QTime
from win32.lib import win32con
from PyQt5.QtGui import QPixmap, QIcon
from win32 import win32api, win32gui
from PyQt5.QtWidgets import QWidget, QApplication, QStackedWidget

from effects import WindowEffect
from my_title_bar import TitleBar
from my_dialog_interface import DialogInterface
from my_welcome_interface import WelcomeInterface
from my_navigation_interface import NavigationInterface
from functions.get_host import getHost
from functions.user_info import getUserInfo, writeUserInfo
from functions.catch_packet import writeCatchPacket, readCatchPacket
from my_thread import WiresharkThread, ArpAttackThread, PublishThread

from .monitor_functions import isMaximized
from .c_structures import MINMAXINFO


class WireSharp(QWidget):
    """ WireSharp 聊天界面 """

    BORDER_WIDTH = 5

    def __init__(self):
        super().__init__()
        self.__getContactInfo()
        self.userInfo = getUserInfo()
        # 实例化小部件
        t1 = time()
        print('🤖 正在初始化界面...')
        self.titleBar = TitleBar(self)
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
        self.setWindowIcon(QIcon(r'resource\Image\icon\icon.png'))
        self.setAttribute(Qt.WA_TranslucentBackground | Qt.WA_StyledBackground)
        WindowEffect.setShadowEffect(self.winId())
        WindowEffect.setWindowAnimation(self.winId())
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
            r'resource\Image\head_portrait\硝子（1）.png',
            r'resource\Image\head_portrait\硝子（2）.png',
            r'resource\Image\head_portrait\硝子（3）.jpg',
        ]
        for i, (hostName, IP) in enumerate(host_list):
            self.contactInfo_list.append({
                'IP': IP,
                'contactName': hostName,
                'headPortraitPath': self.headPortraitPath_list[i % len(self.headPortraitPath_list)]
            })

    def resizeEvent(self, e):
        """ 调整窗口大小 """
        self.titleBar.resize(self.width(), self.titleBar.height())
        self.stackedWidget.resize(self.width() - 402, self.height() - 40)
        # 更新标题栏图标
        if isMaximized(int(self.winId())):
            self.titleBar.maxBt.setMaxState(True)

    def nativeEvent(self, eventType, message):
        """ 处理windows消息 """
        msg = MSG.from_address(message.__int__())
        if msg.message == win32con.WM_NCHITTEST:
            xPos = win32api.LOWORD(msg.lParam) - self.frameGeometry().x()
            yPos = win32api.HIWORD(msg.lParam) - self.frameGeometry().y()
            w, h = self.width(), self.height()
            lx = xPos < self.BORDER_WIDTH
            rx = xPos + 9 > w - self.BORDER_WIDTH
            ty = yPos < self.BORDER_WIDTH
            by = yPos > h - self.BORDER_WIDTH
            if (lx and ty):
                return True, win32con.HTTOPLEFT
            elif (rx and by):
                return True, win32con.HTBOTTOMRIGHT
            elif (rx and ty):
                return True, win32con.HTTOPRIGHT
            elif (lx and by):
                return True, win32con.HTBOTTOMLEFT
            elif ty:
                return True, win32con.HTTOP
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT
        elif msg.message == win32con.WM_NCCALCSIZE:
            if isMaximized(msg.hWnd):
                WindowEffect.adjustMaximizedClientRect(
                    HWND(msg.hWnd), msg.lParam)
            return True, 0
        if msg.message == win32con.WM_GETMINMAXINFO:
            if isMaximized(msg.hWnd):
                window_rect = win32gui.GetWindowRect(msg.hWnd)
                if not window_rect:
                    return False, 0
                # 获取显示器句柄
                monitor = win32api.MonitorFromRect(window_rect)
                if not monitor:
                    return False, 0
                # 获取显示器信息
                monitor_info = win32api.GetMonitorInfo(monitor)
                monitor_rect = monitor_info['Monitor']
                work_area = monitor_info['Work']
                # 将lParam转换为MINMAXINFO指针
                info = cast(
                    msg.lParam, POINTER(MINMAXINFO)).contents
                # 调整位置
                info.ptMaxSize.x = work_area[2] - work_area[0]
                info.ptMaxSize.y = work_area[3] - work_area[1]
                info.ptMaxTrackSize.x = info.ptMaxSize.x
                info.ptMaxTrackSize.y = info.ptMaxSize.y
                # 修改放置点的x,y坐标
                info.ptMaxPosition.x = abs(
                    window_rect[0] - monitor_rect[0])
                info.ptMaxPosition.y = abs(
                    window_rect[1] - monitor_rect[1])
                return True, 1
        return QWidget.nativeEvent(self, eventType, message)

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
        writeCatchPacket(packetInfo, 'data\\catch_packet.json')
        with open(r'resource\html\send_file.html', encoding='utf-8') as f:
            self.__sendMessage(f.read())

    def __startArpAttackSlot(self, IP: str):
        """ 开始 ARP 欺骗槽函数(发送错误 MAC 地址) """
        self.arpAttackThread.startArpAttack(IP, False)

    def __stopArpAttackSlot(self):
        """ 开始 ARP 欺骗槽函数 """
        self.arpAttackThread.stopArpAttack()

    def __publishSlot(self):
        """ 发布消息槽函数 """
        packetInfo = readCatchPacket('data\\catch_packet.json')
        self.publishThread.publish(
            packetInfo['dst host'], packetInfo['topic'], packetInfo['msg'])

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
