# coding:utf-8
import os
import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget, QLabel, QStackedWidget

from my_chat_list_widget import ChatListWidget
from widget.head_portrait import HeadPortrait
from widget.state_widget import StateWidget
from widget.my_button import NavigationButton, OpacityThreeStateToolButton
from .search_line_edit import SearchLineEdit


class NavigationInterface(QWidget):
    """ 导航界面 """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 读取用户信息
        self.__readUserInfo()
        # 实例化小部件
        self.searchLineEdit = SearchLineEdit(self)
        self.__createButtons()
        self.personalSignatureLabel = QLabel(
            self.userInfo['personalSignature'], self)
        self.headPortraitWidget = HeadPortrait(
            self.userInfo['headPortraitPath'], (45, 45), self)
        self.stackedWidget = QStackedWidget(self)
        self.chatListWidget = ChatListWidget(self)
        self.stateWidget = StateWidget(parent=self)
        self.userNameLabel = QLabel(self.userInfo['userName'], self)
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
        self.contactsButton.move(233, 127)
        self.conversationButton.move(138, 127)
        # 将子窗口添加到层叠窗口中
        self.stackedWidget.addWidget(self.chatListWidget)
        self.chatButton.setSelected(True)
        # 设置层叠样式
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName('navigationInterface')
        self.userNameLabel.setObjectName('userNameLabel')
        self.personalSignatureLabel.setObjectName('personalSignatureLabel')
        self.__setQss()

    def __readUserInfo(self):
        """ 读取用户信息 """
        if not os.path.exists('config'):
            os.mkdir('config')
        try:
            with open('config\\user_info.json', encoding='utf-8') as f:
                self.userInfo = json.load(f)
        except:
            self.userInfo = {
                "userName": "之一",
                "personalSignature": "うそじゃないよ",
                "headPortraitPath": "resource\\Image\\head_portrait\\硝子（1）.png"
            }

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
        self.contactsButton = NavigationButton(
            contactsButtonIconPath_dict, '联系人', (38, 42), parent=self)
        self.noticeButton = NavigationButton(
            noticeButtonIconPath_dict, '通知', parent=self)


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
