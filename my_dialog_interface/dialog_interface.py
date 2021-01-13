# coding:utf-8
import os
import re
import json
from typing import List
from copy import deepcopy
from collections import OrderedDict

from PyQt5.QtCore import Qt, pyqtSignal, QTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QStackedWidget

from functions.user_info import getUserInfo
from .dialog_viewer import DialogViewer
from .dialog_title_bar import DialogTitleBar
from .dialog_toolbar import DialogToolbar


class DialogInterface(QWidget):
    """ 会话界面 """

    sendMessageSignal = pyqtSignal(dict)    # 发送对话消息
    recvMessageSignal = pyqtSignal(dict)    # 收到对话消息
    startWiresharkSignal = pyqtSignal(str)  # 开始抓包线程
    stopWiresharkSignal = pyqtSignal()      # 停止抓包线程
    stopArpAttackSignal = pyqtSignal()      # 停止 ARP 欺骗
    startArpAttackSignal = pyqtSignal(str)  # 开始 ARP 欺骗
    publishSignal = pyqtSignal()            # 发布消息

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.currentDialogIndex = 0
        # 读取用户信息
        self.userInfo = getUserInfo()
        # 当前联系人信息
        self.currentContactInfo = {}
        # 抓包标志位
        self.isCatchingPacket = False
        self.isArpAttack = False
        # 实例化小部件
        self.dialogTitleBar = DialogTitleBar('', self)
        self.dialogToolbar = DialogToolbar(self)
        self.stackedWidget = QStackedWidget(self)
        self.__dialogViewer_list = []  # type:List[DialogViewer]
        self.__dialogInfo_list = []  # type:List[dict]
        self.__IPIndex_dict = OrderedDict()
        # 初始化窗口
        self.__initWidget()

    def __initWidget(self):
        """ 初始化窗口 """
        self.dialogToolbar.raise_()
        self.setAttribute(Qt.WA_StyledBackground)
        self.setMinimumSize(877, self.dialogTitleBar.height() +
                            self.dialogToolbar.height() + 200)
        self.resize(877, 917)
        self.stackedWidget.resize(self.width(), self.height(
        ) - self.dialogTitleBar.height() - self.dialogToolbar.height())
        self.stackedWidget.move(0, self.dialogTitleBar.height())
        # 设置层叠样式
        self.__setQss()
        # 信号连接到槽
        self.__connectSignalToSlot()

    def resizeEvent(self, e):
        """ 改变窗口大小 """
        # 调整小部件尺寸
        self.dialogTitleBar.resize(self.width(), self.dialogTitleBar.height())
        self.dialogToolbar.resize(self.width(), self.dialogToolbar.height())
        self.__toolBarHeightChangedSlot()

    def dialogCount(self):
        """ 返回会话个数 """
        return len(self.__dialogViewer_list)

    def addDialog(self, contactInfo: dict, isSetToCurrentDialog: bool = True):
        """ 添加一个会话 """
        dialogViewer = DialogViewer(self)
        self.stackedWidget.addWidget(dialogViewer)
        self.__dialogViewer_list.append(dialogViewer)
        # 存储用户和会话消息
        dialogInfo = contactInfo.copy()
        dialogInfo['message_list'] = []
        self.__dialogInfo_list.append(dialogInfo)
        self.__IPIndex_dict[contactInfo['IP']] = self.dialogCount() - 1
        # 将其设为当前会话
        if isSetToCurrentDialog:
            self.setCurrentDialog(self.dialogCount() - 1)

    def removeDialog(self, IP: str):
        """ 移除会话 """
        index = self.__IPIndex_dict.pop(IP)
        dialogViewer = self.__dialogViewer_list.pop(index)
        self.__dialogInfo_list.pop(index)
        self.stackedWidget.removeWidget(dialogViewer)
        # 更新下标
        for i, key in enumerate(self.__IPIndex_dict.keys()):
            self.__IPIndex_dict[key] = i
        # 释放内存
        dialogViewer.deleteLater()

    def setCurrentDialogByIP(self, IP: str):
        """ 根据IP设置当前窗口 """
        index = self.__IPIndex_dict[IP]
        self.setCurrentDialog(index)

    def setCurrentDialog(self, index: int):
        """ 设置当前会话 """
        self.currentDialogIndex = index
        self.stackedWidget.setCurrentIndex(index)
        self.dialogTitleBar.setTitle(
            self.__dialogInfo_list[index]['contactName'])
        self.currentContactInfo = self.__dialogInfo_list[index]

    def __toolBarHeightChangedSlot(self):
        """ 工具栏高度改变对应的槽函数 """
        self.dialogToolbar.move(0, self.height()-self.dialogToolbar.height())
        self.stackedWidget.resize(self.width(), self.height(
        ) - self.dialogToolbar.height() - self.dialogTitleBar.height())

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'resource\qss\dialog_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def __sendMessageSlot(self, message: str):
        """ 发送消息 """
        dialogViewer = self.currentDialog()
        dialogViewer.addMessageWidget(
            self.userInfo['userName'],
            self.userInfo['headPortraitPath'],
            message, 'right')
        # 发送信号，要求主界面更新对话框列表或者创建对话框
        index = self.stackedWidget.currentIndex()
        messageInfo = deepcopy(self.__dialogInfo_list[index])
        messageInfo['message'] = message
        messageInfo['time'] = QTime.currentTime().toString('H:mm')
        self.sendMessageSignal.emit(messageInfo)
        # 更新当前联系人
        self.currentContactInfo = self.__dialogInfo_list[index]
        # 分析指令
        self.__analyseMessage(message)

    def __analyseMessage(self, message: str):
        """ 分析消息中的指令 """
        if re.search(r'开始.*抓包', message) and message.find('停') == -1:
            self.__startWireshark(self.currentContactInfo)
        elif re.search(r'停止.*抓包', message) and message.find('开始') == -1:
            self.__stopWireshark()
        elif re.search(r'开始.*攻击', message):
            self.__startArpAttack(self.currentContactInfo)
        elif re.search(r'停止.*攻击', message):
            self.__stopArpAttack()
        elif message.find('发布') != -1:
            self.__publish()
        else:
            messageInfo = deepcopy(self.currentContactInfo)
            messageInfo['time'] = QTime.currentTime().toString('H:mm')
            messageInfo['message'] = '<center><img src="resource\Image\emoticon\新花样.gif" /></center>'
            self.receiveMessageSlot(messageInfo)

    def __startWireshark(self, messageInfo: dict):
        """ 开始抓包 """
        self.isCatchingPacket = True
        self.startWiresharkSignal.emit(messageInfo['IP'])
        self.dialogToolbar.catchPacketButton.setToolTip('停止抓包')

    def __stopWireshark(self):
        """ 停止抓包 """
        self.isCatchingPacket = False
        self.stopWiresharkSignal.emit()
        self.dialogToolbar.catchPacketButton.setToolTip('开始抓包')

    def __startArpAttack(self, messageInfo: dict):
        """ 开始 ARP 攻击(发送错误 MAC 地址) """
        self.isArpAttack = True
        self.startArpAttackSignal.emit(messageInfo['IP'])
        self.dialogToolbar.arpSpoofButton.setToolTip('停止欺骗')

    def __stopArpAttack(self):
        """ 开始 ARP 攻击 """
        self.isArpAttack = False
        self.stopArpAttackSignal.emit()
        self.dialogToolbar.arpSpoofButton.setToolTip('开始欺骗')

    def receiveMessageSlot(self, messageInfo: dict):
        """ 收到消息 """
        dialogViewer = self.currentDialog()
        dialogViewer.addMessageWidget(
            messageInfo['contactName'],
            messageInfo['headPortraitPath'],
            messageInfo['message'], 'left')
        self.recvMessageSignal.emit(messageInfo)

    def __connectSignalToSlot(self):
        """ 信号连接到槽函数 """
        self.dialogToolbar.sendMessageSignal.connect(self.__sendMessageSlot)
        self.dialogToolbar.publishButton.clicked.connect(
            self.__publishButtonClickedSlot)
        self.dialogToolbar.arpSpoofButton.clicked.connect(
            self.__arpAttackButtonClickedSlot)
        self.dialogToolbar.catchPacketButton.clicked.connect(
            self.__catchPacketButtonClickedSlot)
        self.dialogToolbar.adjustHeightSignal.connect(
            self.__toolBarHeightChangedSlot)

    def currentDialog(self) -> DialogViewer:
        """ 返回当前会话视图 """
        return self.stackedWidget.currentWidget()

    def __catchPacketButtonClickedSlot(self):
        """ 抓包按钮槽函数 """
        msg = '停止抓包' if self.isCatchingPacket else '开始抓包'
        self.__sendMessageSlot(msg)

    def __arpAttackButtonClickedSlot(self):
        """ ARP 攻击按钮槽函数 """
        msg = '开始 ARP 攻击' if not self.isArpAttack else '停止 ARP 攻击'
        self.__sendMessageSlot(msg)

    def __publishButtonClickedSlot(self):
        """ 发布按钮槽函数 """
        self.__sendMessageSlot('发布假消息')

    def __publish(self):
        """ 发布消息 """
        self.publishSignal.emit()

    @property
    def IPIndex_dict(self):
        return self.__IPIndex_dict
