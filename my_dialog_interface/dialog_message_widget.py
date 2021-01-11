# coding:utf-8
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from .message_bubble import MessageBubble
from widget.head_portrait import HeadPortrait
from widget.my_button import ThreeStateToolButton


class DialogMessageWidget(QWidget):
    """ 对话消息小部件 """

    def __init__(self, contactName: str, imagePath: str, message: str,  direction: str = 'left', parent=None):
        """ 初始化消息小部件

        Parameters
        ----------
        contactName : str
            用户名

        imagePath : str
            用户头像路径

        message : str
            对话消息

        direction : str
            气泡方向，有 `left` 和 `right` 两种

        parent : QWidget
            父级窗口
        """
        super().__init__(parent=parent)
        self.message = message
        self.contactName = contactName
        if direction not in ['left', 'right']:
            raise Exception('起泡方向只能是 `left` 或者 `right`')
        self.direction = direction
        # 发送信息的时间
        self.sendMessageTime = QTime.currentTime().toString('H:mm')
        # 实例化小部件
        iconPath_dict = {
            'normal': r'resource\Image\my_dialog_interface\回应此消息_normal.png',
            'hover': r'resource\Image\my_dialog_interface\回应此消息_hover.png',
            'pressed': r'resource\Image\my_dialog_interface\回应此消息_pressed.png',
        }
        self.messageBubble = MessageBubble(message, direction, self)
        self.headPortraitWidget = HeadPortrait(imagePath, parent=self)
        self.userInfoLabel = QLabel(self)
        self.respondsMessageButton = ThreeStateToolButton(
            iconPath_dict, (18, 19), self)
        # 初始化窗口
        self.__initWidget()

    def __initWidget(self):
        """ 初始化窗口 """
        self.resize(877, max(72, self.messageBubble.height() + 23))
        self.setMinimumWidth(877)
        # 设置小部件位置
        if self.direction == 'left':
            self.userInfoLabel.setText(
                f'{self.contactName} ,   {self.sendMessageTime}')
            self.userInfoLabel.move(100, 1)
            self.messageBubble.move(100, 23)
            self.headPortraitWidget.move(37, 0)
            self.respondsMessageButton.move(
                self.messageBubble.x() + self.messageBubble.width() + 11, 25)
        else:
            self.userInfoLabel.setText(self.sendMessageTime)
            self.userInfoLabel.adjustSize()
            self.userInfoLabel.move(
                self.width()-self.userInfoLabel.width()-85, 0)
            self.messageBubble.move(
                self.width()-self.messageBubble.width()-100, 23)
            self.headPortraitWidget.move(
                self.width()-self.headPortraitWidget.width()-37, 0)
            self.respondsMessageButton.hide()
        # 设置层叠样式
        self.userInfoLabel.setObjectName('userInfoLabel')
        self.__setQss()

    def __setQss(self):
        """ 设置层叠样式表 """
        with open(r'resource\qss\dialog_message_widget.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def resizeEvent(self, e):
        """ 调整位置 """
        super().resizeEvent(e)
        # self.messageBubble.maxWidth = self.width() - 350
        # self.messageBubble.adjustSize_()
        if self.direction == 'right':
            self.userInfoLabel.move(
                self.width()-self.userInfoLabel.width()-85, 0)
            self.messageBubble.move(
                self.width()-self.messageBubble.width()-100, 23)
            self.headPortraitWidget.move(
                self.width() - self.headPortraitWidget.width() - 37, 0)
        else:
            self.respondsMessageButton.move(
                self.messageBubble.x() + self.messageBubble.width() + 11, 25)
