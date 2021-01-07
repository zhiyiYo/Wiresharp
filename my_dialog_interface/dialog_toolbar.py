# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from .dialog_text_edit import DialogTextEdit
from widget.my_button import CircleButton, ThreeStateToolButton


class DialogToolbar(QWidget):
    """ 会话工具栏 """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        catchPacketIconPath_dict = {
            'normal': r'resource\Image\my_dialog_interface\添加文件_normal.png',
            'hover': r'resource\Image\my_dialog_interface\添加文件_hover.png',
            'pressed': r'resource\Image\my_dialog_interface\添加文件_pressed.png'
        }
        arpSpoofIconPath_dict = {
            'normal': r'resource\Image\my_dialog_interface\将联系人发送至聊天_normal.png',
            'hover': r'resource\Image\my_dialog_interface\将联系人发送至聊天_hover.png',
            'pressed': r'resource\Image\my_dialog_interface\将联系人发送至聊天_pressed.png'
        }
        publishIconPath_dict = {
            'normal': r'resource\Image\my_dialog_interface\安排通话_normal.png',
            'hover': r'resource\Image\my_dialog_interface\安排通话_hover.png',
            'pressed': r'resource\Image\my_dialog_interface\安排通话_pressed.png'
        }
        moreActionsIconPath_dict = {
            'normal': r'resource\Image\my_dialog_interface\更多操作_normal.png',
            'hover': r'resource\Image\my_dialog_interface\更多操作_hover.png',
            'pressed': r'resource\Image\my_dialog_interface\更多操作_pressed.png'
        }
        sendMessageIconPath_dict = {
            'normal': r'resource\Image\my_dialog_interface\发送消息_normal.png',
            'hover': r'resource\Image\my_dialog_interface\发送消息_normal.png',
            'pressed': r'resource\Image\my_dialog_interface\发送消息_pressed.png',
        }
        # 实例化小部件
        self.dialogTextEdit = DialogTextEdit(self)
        self.publishButton = CircleButton(publishIconPath_dict, parent=self)
        self.arpSpoofButton = CircleButton(arpSpoofIconPath_dict, parent=self)
        self.catchPacketButton = CircleButton(
            catchPacketIconPath_dict, parent=self)
        self.moreActionsButton = CircleButton(
            moreActionsIconPath_dict, parent=self)
        self.sendMessageButton = ThreeStateToolButton(
            sendMessageIconPath_dict, (51, 50), self)
        # 初始化界面
        self.__initWidget()

    def __initWidget(self):
        """ 初始化界面 """
        self.resize(877, 100)
        # 隐藏发送消息按钮
        self.sendMessageButton.hide()
        # 设置小部件位置
        self.dialogTextEdit.move(100, 12)
        self.sendMessageButton.move(724, 18)
        self.catchPacketButton.move(
            self.dialogTextEdit.x()+self.dialogTextEdit.width()+10, 18)
        self.arpSpoofButton.move(
            self.catchPacketButton.x()+self.catchPacketButton.width()+10, 18)
        self.publishButton.move(
            self.arpSpoofButton.x()+self.arpSpoofButton.width()+10, 18)
        self.moreActionsButton.move(
            self.publishButton.x()+self.publishButton.width()+10, 18)
        # 设置提示信息
        self.publishButton.setToolTip('发布消息')
        self.arpSpoofButton.setToolTip('开始欺骗')
        self.sendMessageButton.setToolTip('发送消息')
        self.catchPacketButton.setToolTip('开始抓包')
        # 设置层叠样式
        self.__setQss()
        # 信号连接到槽函数
        self.__connectSignalToSlot()

    def __connectSignalToSlot(self):
        """ 信号连接到槽函数 """
        self.dialogTextEdit.resizeSignal.connect(
            lambda x: self.resize(self.width(), self.height()+x))
        self.dialogTextEdit.hasTextSignal.connect(self.__hasTextSlot)

    def __hasTextSlot(self, hasText: bool):
        """ 根据输入框是否含有文本来设置按钮可见性 """
        self.publishButton.setHidden(hasText)
        self.arpSpoofButton.setHidden(hasText)
        self.moreActionsButton.setHidden(hasText)
        self.catchPacketButton.setHidden(hasText)
        self.sendMessageButton.setVisible(hasText)

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'resource\qss\dialog_toolbar.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
