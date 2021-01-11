# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics
from PyQt5.QtWidgets import QWidget, QLabel

from widget.my_button import ThreeStatePushButton, CircleButton


class DialogTitleBar(QWidget):
    """ 会话标题栏 """

    def __init__(self, contactName: str, parent=None):
        """ 初始化标题栏

        Parameters
        ----------
        contactName : str
            会话中联系人的名称

        parent : QWidget
            父级窗口
        """
        super().__init__(parent=parent)
        self.contactName = contactName
        # 实例化小部件
        stateIconPath_dict = {
            'normal': r'resource\Image\my_dialog_interface\当前在线_normal.png',
            'hover': r'resource\Image\my_dialog_interface\当前在线_hover.png',
            'pressed': r'resource\Image\my_dialog_interface\当前在线_pressed.png'
        }
        mediaIconPath_dict = {
            'normal': r'resource\Image\my_dialog_interface\媒体库_normal.png',
            'hover': r'resource\Image\my_dialog_interface\媒体库_hover.png',
            'pressed': r'resource\Image\my_dialog_interface\媒体库_pressed.png'
        }
        callIconPath_dict = {
            'normal': r'resource\Image\my_dialog_interface\音频通话_normal.png',
            'hover': r'resource\Image\my_dialog_interface\音频通话_hover.png',
            'pressed': r'resource\Image\my_dialog_interface\音频通话_pressed.png'
        }
        createGroupIconPath_dict = {
            'normal': r'resource\Image\my_dialog_interface\新建群组_normal.png',
            'hover': r'resource\Image\my_dialog_interface\新建群组_hover.png',
            'pressed': r'resource\Image\my_dialog_interface\新建群组_pressed.png'
        }

        self.contactNamesLabel = QLabel(contactName, self)
        self.stateButton = ThreeStatePushButton(
            stateIconPath_dict, '当前在线', (11, 10), self)
        self.mediaButton = ThreeStatePushButton(
            mediaIconPath_dict, '媒体库', (14, 11), self)
        self.callButton = CircleButton(callIconPath_dict, parent=self)
        self.createGroupButton = CircleButton(
            createGroupIconPath_dict, parent=self)
        # 初始化窗口
        self.__initWidget()

    def __initWidget(self):
        """ 初始化窗口 """
        self.resize(877, 111)
        # 设置尺寸
        self.stateButton.resize(77, 29)
        self.mediaButton.resize(65, 29)
        # 设置位置
        self.stateButton.move(24, 60)
        self.mediaButton.move(self.stateButton.x() +
                              self.stateButton.width() + 17, 60)
        self.contactNamesLabel.move(24, 20)
        # 设置层叠样式
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName('dialogTitleBar')
        self.__setQss()

    def setTitle(self, contactName: str):
        """ 设置标题栏联系人名称 """
        self.contactName = contactName
        self.__adjustTitle()

    def __adjustTitle(self):
        """ 调整标题标签 """
        fontMetrics = QFontMetrics(QFont('Microsoft YaHei', 19, 75))
        newText = fontMetrics.elidedText(
            self.contactName, Qt.ElideRight, self.width() - 240)
        self.contactNamesLabel.setText(newText)
        self.contactNamesLabel.adjustSize()

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'resource\qss\dialog_title_bar.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def paintEvent(self, e):
        """ 绘制背景 """
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(138, 141, 145), 2))
        painter.drawLine(self.stateButton.x() + self.stateButton.width() + 8, 68,
                         self.stateButton.x() + self.stateButton.width() + 8, 82)

    def resizeEvent(self, e):
        """ 调整窗口大小 """
        self.createGroupButton.move(
            self.width()-self.createGroupButton.width()-19, 30)
        self.callButton.move(self.createGroupButton.x() -
                             self.callButton.width() - 13, 30)
        self.__adjustTitle()
