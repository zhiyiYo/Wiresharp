# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget


class WindowMask(QWidget):
    """ 窗口遮罩 """

    def __init__(self, bgColor: tuple = (255, 255, 255, 55), parent=None):
        super().__init__(parent=parent)
        self.setObjectName('windowMask')
        self.setAttribute(Qt.WA_StyledBackground)
        self.bgColor = bgColor
        r, g, b, a = bgColor
        self.setStyleSheet(f'background:rgba({r,g,b,a})')
