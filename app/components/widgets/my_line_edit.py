# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLineEdit

from .my_menu import TextEditMenu


class LineEdit(QLineEdit):
    """ 单行输入框 """

    def __init__(self, text:str='', parent=None):
        super().__init__(text, parent=parent)
        self.contextMenu = TextEditMenu(self)

    def contextMenuEvent(self, e):
        self.contextMenu.exec_(e.globalPos())
