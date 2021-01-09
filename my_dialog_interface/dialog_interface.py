# coding:utf-8
import os
import json
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QStackedWidget

from .dialog_viewer import DialogViewer
from .dialog_title_bar import DialogTitleBar
from .dialog_toolbar import DialogToolbar


class DialogInterface(QWidget):
    """ 会话界面 """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.currentDialogIndex = 0
        # 读取用户信息
        self.__readUserInfo()
        # 实例化小部件
        self.dialogTitleBar = DialogTitleBar('', self)
        self.dialogToolbar = DialogToolbar(self)
        self.stackedWidget = QStackedWidget(self)
        self.__dialogViewer_list = []  # type:List[DialogViewer]
        self.__dialogInfo_list = []    # type:List[dict]
        # 初始化窗口
        self.__initWidget()

    def __initWidget(self):
        """ 初始化窗口 """
        self.setAttribute(Qt.WA_StyledBackground)
        self.setMinimumSize(877, self.dialogTitleBar.height() +
                            self.dialogToolbar.height() + 200)
        self.resize(877, 917)
        self.stackedWidget.resize(self.width(), 577)
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
        for w in self.__dialogViewer_list + [self.stackedWidget]:
            w.resize(self.width(), self.height(
            ) - self.dialogToolbar.height() - self.dialogTitleBar.height())
        # 移动小部件
        self.dialogToolbar.move(0, self.height()-self.dialogToolbar.height())

    def dialogCount(self):
        """ 返回会话个数 """
        return len(self.__dialogViewer_list)

    def addDialog(self, contactName: str, isSetToCurrentDialog: bool = True):
        """ 添加一个会话 """
        dialogViewer = DialogViewer(self)
        self.stackedWidget.addWidget(dialogViewer)
        self.__dialogViewer_list.append(dialogViewer)
        # 存储用户和会话消息
        self.__dialogInfo_list.append({
            'contactName': contactName,
            'message_list': []
        })
        # 将其设为当前会话
        if isSetToCurrentDialog:
            self.setCurrentDialog(self.dialogCount()-1)

    def setCurrentDialog(self, index: int):
        """ 设置当前会话 """
        self.currentDialogIndex = index
        self.stackedWidget.setCurrentIndex(index)
        self.dialogTitleBar.setTitle(
            self.__dialogInfo_list[index]['contactName'])

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
        self.receiveMessageSlot({
            'userName': 'second first',
            'headPortraitPath': r'resource\Image\head_portrait\硝子（2）.png',
            'message': '???'}
        )

    def receiveMessageSlot(self, messageInfo: dict):
        """ 收到消息 """
        dialogViewer = self.currentDialog()
        dialogViewer.addMessageWidget(
            messageInfo['userName'],
            messageInfo['headPortraitPath'],
            messageInfo['message'], 'left')

    def __connectSignalToSlot(self):
        """ 信号连接到槽函数 """
        self.dialogToolbar.sendMessageSignal.connect(self.__sendMessageSlot)
        self.dialogToolbar.adjustHeightSignal.connect(
            lambda x: self.resize(self.width(), self.height() + x))

    def currentDialog(self) -> DialogViewer:
        """ 返回当前会话视图 """
        return self.stackedWidget.currentWidget()

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
