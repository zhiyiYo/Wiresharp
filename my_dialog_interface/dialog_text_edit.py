# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QTextDocument, QKeyEvent, QContextMenuEvent
from PyQt5.QtWidgets import QTextEdit

from widget.my_button import CircleButton
from widget.my_menu import TextEditMenu


class DialogTextEdit(QTextEdit):
    """ 会话消息输入框 """

    resizeSignal = pyqtSignal(int)  # 调整大小信号
    hasTextChanged = pyqtSignal(bool)  # 是否含有文本信号
    sendMessageSignal = pyqtSignal(str)  # 按下回车键后发送消息

    def __init__(self, parent):
        super().__init__(parent=parent)
        iconPath_dict = {'normal': r'resource\Image\my_dialog_interface\笑脸_normal.png',
                         'hover': r'resource\Image\my_dialog_interface\笑脸_hover.png',
                         'pressed': r'resource\Image\my_dialog_interface\笑脸_pressed.png'}
        self.smileFaceButton = CircleButton(iconPath_dict, parent=self)
        self.menu = TextEditMenu(self)
        # 之前有文本标志位
        self.hasTextBefore = False
        # 初始化界面
        self.__initWidget()
        self.setFocus()

    def __initWidget(self):
        """ 初始化界面 """
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setPlaceholderText('键入消息')
        # self.__setQss()
        # 信号连接槽函数
        self.textChanged.connect(self.__textChangedSlot)

    def __setQss(self):
        """ 设置层叠样式 """
        with open('resource\\qss\\dialog_text_edit.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def resizeEvent(self, e):
        """ 调整窗口大小 """
        super().resizeEvent(e)
        self.smileFaceButton.move(8, self.height() - 56)

    def adjustWidth(self):
        """ 调整输入框宽度 """
        # 当前是否含有文本
        hasTextCurrent = bool(self.toPlainText())
        # 双边触发
        if not self.hasTextBefore and hasTextCurrent:
            self.setFixedWidth(self.width() + 180)
            self.hasTextChanged.emit(True)
        elif self.hasTextBefore and not hasTextCurrent:
            self.setFixedWidth(self.width() - 180)
            self.hasTextChanged.emit(False)
        # 更新标志位
        self.hasTextBefore = hasTextCurrent

    def adjustHeight(self):
        """ 根据文本内容调整高度 """
        document = self.document()  # type:QTextDocument
        if document:
            newHeight = document.size().height() + 30
            if newHeight != self.height():
                self.resizeSignal.emit(newHeight - self.height())
                self.setFixedHeight(newHeight)

    def __textChangedSlot(self):
        """ 文本改变时改变高度和宽度 """
        self.adjustWidth()
        self.adjustHeight()

    def keyPressEvent(self, e: QKeyEvent):
        """ 按下回车后发送消息 """
        if e.key() in [16777220, 16777221] and self.toPlainText():
            self.sendMessageSignal.emit(self.toPlainText())
            self.clear()
            return
        super().keyPressEvent(e)

    def contextMenuEvent(self, e: QContextMenuEvent):
        """ 设置右击菜单 """
        self.menu.exec_(e.globalPos())
