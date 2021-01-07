# coding:utf-8
from PyQt5.QtCore import Qt, QEvent, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from PyQt5.QtWidgets import QToolButton, QLineEdit, QTextEdit

from widget.my_button import CircleButton
from functions.auto_wrap import autoWrap


class DialogTextEdit(QTextEdit):
    """ 会话消息输入框 """

    resizeSignal = pyqtSignal(int)  # 调整大小信号
    hasTextSignal = pyqtSignal(bool)  # 是否含有文本信号

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        iconPath_dict = {'normal': r'resource\Image\my_dialog_interface\笑脸_normal.png',
                         'hover': r'resource\Image\my_dialog_interface\笑脸_hover.png',
                         'pressed': r'resource\Image\my_dialog_interface\笑脸_pressed.png'}
        self.smileFaceButton = CircleButton(iconPath_dict, parent=self)
        # 初始化界面
        self.__initWidget()
        self.setFocus()

    def __initWidget(self):
        """ 初始化界面 """
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setPlaceholderText('键入消息')
        self.resize(438, 62)
        self.__setQss()
        # 信号连接槽函数
        self.textChanged.connect(self.__adjustSize)

    def __setQss(self):
        """ 设置层叠样式 """
        with open('resource\\qss\\dialog_text_edit.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def resizeEvent(self, e):
        """ 调整窗口大小 """
        super().resizeEvent(e)
        self.smileFaceButton.move(8, self.height()-56)

    def __adjustSize(self):
        """ 调整输入框高度 """
        # 调整宽度并发送信号
        newWidth = 617 if self.toPlainText() else 438
        self.resize(newWidth, self.height())
        self.hasTextSignal.emit(bool(self.toPlainText()))
        # todo: 调整高度
        nextText, lineBreaksNum = autoWrap(self.toPlainText(), 46)
        if 62 + 25 * lineBreaksNum != self.height():
            self.resizeSignal.emit(62 + 25*lineBreaksNum-self.height())
            self.resize(self.width(), 62 + 25*lineBreaksNum)
