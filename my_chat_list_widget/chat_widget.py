# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFontMetrics, QFont
from PyQt5.QtWidgets import QWidget, QLabel

from widget.head_portrait import HeadPortrait
from widget.state_widget import StateWidget


class ChatWidget(QWidget):
    """ 聊天小部件 """

    def __init__(self, messageInfo: dict, parent=None):
        super().__init__(parent=parent)
        self.messageInfo = messageInfo.copy()
        self.__bgColor_dict = {
            'normal': QColor(240, 244, 248),
            'hover': QColor(220, 241, 250),
            'selected': QColor(199, 237, 252)
        }
        # 实例化小部件
        self.headPortraitWidget = HeadPortrait(
            messageInfo['headPortraitPath'], (45, 45), self)
        self.userNameLabel = QLabel(messageInfo['userName'], self)
        self.messageLabel = QLabel(self)
        self.timeLabel = QLabel(messageInfo['time'], self)
        self.stateWidget = StateWidget('在线', False, parent=self)
        self.windowMask = QWidget(self)
        # 初始化界面
        self.__initWidget()

    def __initWidget(self):
        """ 初始化界面 """
        # 调整尺寸
        self.setFixedSize(402, 75)
        self.__setMessageText()
        self.windowMask.resize(self.size())
        self.windowMask.hide()
        # 设置小部件位置
        self.headPortraitWidget.move(10, 12)
        self.userNameLabel.move(68, 11)
        self.messageLabel.move(68, 36)
        self.stateWidget.move(40, 43)
        self.timeLabel.move(345, 11)
        # 设置层叠样式
        self.setObjectName('chatWidget')
        self.timeLabel.setObjectName('timeLabel')
        self.windowMask.setObjectName('windowMask')
        self.messageLabel.setObjectName('messageLabel')
        self.userNameLabel.setObjectName('userNameLabel')
        self.__setQss()

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'resource\qss\chat_widget.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.windowMask.show()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.windowMask.hide()

    def updateWindow(self, messageInfo: dict):
        """ 更新窗口 """
        self.messageInfo = messageInfo
        self.timeLabel.setText(messageInfo['time'])
        self.userNameLabel.setText(messageInfo['userName'])
        self.headPortraitWidget.setHeadPortrait(
            messageInfo['headPortraitPath'])
        # 调整标签显示的文本
        self.__setMessageText()

    def __setMessageText(self):
        """根据消息长短来添加省略号 """
        fontMetrics_1 = QFontMetrics(QFont('Microsoft YaHei', 11))
        newText = fontMetrics_1.elidedText(
            self.messageInfo['message'], Qt.ElideRight, 255)
        self.messageLabel.setText(newText)
