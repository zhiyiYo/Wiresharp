# coding:utf-8
import os
import json
from typing import List, Dict

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QFontMetrics, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QStackedWidget

from widget.state_widget import StateWidget
from widget.head_portrait import HeadPortrait
from my_chat_list_widget import ChatListWidget
from functions.user_info import getUserInfo
from my_contact_interface import ContactInterface
from widget.my_button import NavigationButton, OpacityThreeStateToolButton
from .search_line_edit import SearchLineEdit


class NavigationInterface(QWidget):
    """ 导航界面 """

    def __init__(self, contactInfo_list: List[Dict[str, str]], parent=None):
        super().__init__(parent=parent)
        # 读取用户信息
        self.userInfo = getUserInfo()
        # 实例化小部件
        self.searchLineEdit = SearchLineEdit(self)
        self.__createButtons()
        self.userNameLabel = QLabel(self)
        self.personalSignatureLabel = QLabel(self)
        self.headPortraitWidget = HeadPortrait(
            self.userInfo['headPortraitPath'], (45, 45), self)
        self.stackedWidget = QStackedWidget(self)
        self.chatListWidget = ChatListWidget(self)
        self.contactInterface = ContactInterface(contactInfo_list, self)
        self.stateWidget = StateWidget(parent=self)
        # 界面字典
        self.__interface_dict = {
            0: self.chatListWidget,
            1: self.contactInterface
        }
        # 初始化界面
        self.__initWidget()

    def __initWidget(self):
        """ 初始化界面 """
        self.setFixedWidth(402)
        self.resize(402, 917)
        self.stateWidget.move(40, 40)
        self.dialsButton.move(351, 70)
        self.searchButton.move(22, 83)
        self.stackedWidget.move(0, 183)
        self.userNameLabel.move(67, 13)
        self.searchLineEdit.move(10, 70)
        self.headPortraitWidget.move(10, 10)
        self.moreActionsButton.move(351, 11)
        self.personalSignatureLabel.move(67, 33)
        self.chatButton.move(38, 127)
        self.noticeButton.move(340, 127)
        self.contactButton.move(233, 127)
        self.conversationButton.move(138, 127)
        # 将子窗口添加到层叠窗口中
        self.stackedWidget.addWidget(self.chatListWidget)
        self.stackedWidget.addWidget(self.contactInterface)
        self.chatButton.setSelected(True)
        # 设置层叠样式
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName('navigationInterface')
        self.userNameLabel.setObjectName('userNameLabel')
        self.personalSignatureLabel.setObjectName('personalSignatureLabel')
        self.__setQss()
        # 调整个新签名和用户名长度
        self.__setLabelText()
        # 信号连接到槽函数
        self.__connectSignalToSlot()

    def __createButtons(self):
        """ 创建按钮 """
        opacity_dict = {'normal': 1, 'hover': 0.72, 'pressed': 0.2}
        chatButtonIconPath_dict = {
            'normal': r'resource\Image\navigation_interface\聊天_normal.png',
            'hover': r'resource\Image\navigation_interface\聊天_hover.png',
            'selected': r'resource\Image\navigation_interface\聊天_selected.png',
        }
        conversationButtonIconPath_dict = {
            'normal': r'resource\Image\navigation_interface\通话_normal.png',
            'hover': r'resource\Image\navigation_interface\通话_hover.png',
            'selected': r'resource\Image\navigation_interface\通话_selected.png',
        }
        contactsButtonIconPath_dict = {
            'normal': r'resource\Image\navigation_interface\联系人_normal.png',
            'hover': r'resource\Image\navigation_interface\联系人_hover.png',
            'selected': r'resource\Image\navigation_interface\联系人_selected.png',
        }
        noticeButtonIconPath_dict = {
            'normal': r'resource\Image\navigation_interface\通知_normal.png',
            'hover': r'resource\Image\navigation_interface\通知_hover.png',
            'selected': r'resource\Image\navigation_interface\通知_selected.png',
        }
        self.moreActionsButton = OpacityThreeStateToolButton(
            r'resource\Image\navigation_interface\更多操作.png',
            opacity_dict, parent=self)
        self.searchButton = OpacityThreeStateToolButton(
            r'resource\Image\navigation_interface\搜索.png', opacity_dict, (18, 18), self)
        self.dialsButton = OpacityThreeStateToolButton(
            r'resource\Image\navigation_interface\拨号盘.png', opacity_dict, (40, 40), self)
        self.chatButton = NavigationButton(
            chatButtonIconPath_dict, '聊天', parent=self)
        self.conversationButton = NavigationButton(
            conversationButtonIconPath_dict, '通话', parent=self)
        self.contactButton = NavigationButton(
            contactsButtonIconPath_dict, '联系人', (38, 42), parent=self)
        self.noticeButton = NavigationButton(
            noticeButtonIconPath_dict, '通知', parent=self)
        self.navigationButton_list = [
            self.chatButton, self.contactButton,
            self.conversationButton, self.noticeButton
        ]

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'resource\qss\navigation_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def paintEvent(self, e):
        """ 绘制背景 """
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(213, 217, 222)))
        painter.drawLine(0, 182, self.width(), 183)

    def resizeEvent(self, e):
        """ 调整窗口大小 """
        super().resizeEvent(e)
        self.stackedWidget.resize(self.width(), self.height() - 183)
        self.contactInterface.resize(self.stackedWidget.size())
        self.chatListWidget.resize(self.stackedWidget.size())

    def __setLabelText(self):
        """设置用户名和个新签名标签的文字并根据字符串长短来添加省略号 """
        # 调整个新签名
        fontMetrics = QFontMetrics(QFont('Microsoft YaHei', 8))
        newText = fontMetrics.elidedText(
            self.userInfo['personalSignature'], Qt.ElideRight, 250)
        self.personalSignatureLabel.setText(newText)
        self.personalSignatureLabel.adjustSize()
        # 调整用户名
        newText = fontMetrics.elidedText(
            self.userInfo['userName'], Qt.ElideRight, 260)
        self.userNameLabel.setText(newText)
        self.userNameLabel.adjustSize()

    def updateUserInfo(self, userInfo: dict):
        """ 更新用户信息 """
        self.userInfo = userInfo.copy()
        self.__setLabelText()
        self.headPortraitWidget.setHeadPortrait(userInfo['headPortraitPath'])

    def switchToContactInterface(self):
        """ 切换到联系人界面 """
        self.__switchInterface(1)

    def switchToChatInterface(self):
        """ 切换到联系人界面 """
        self.__switchInterface(0)

    def __switchInterface(self, index: int):
        """ 切换界面 """
        currentIndex = self.stackedWidget.currentIndex()
        if index not in self.__interface_dict.keys():
            self.navigationButton_list[index].setSelected(False)
            return
        elif index == currentIndex:
            return
        self.navigationButton_list[currentIndex].setSelected(False)
        self.navigationButton_list[index].setSelected(True)
        self.stackedWidget.setCurrentWidget(self.__interface_dict[index])

    def __connectSignalToSlot(self):
        """ 信号连接到槽函数 """
        # 切换界面
        for i, button in enumerate(self.navigationButton_list):
            button.clicked.connect(lambda x, i=i: self.__switchInterface(i))
