# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLineEdit

from app.components.widgets.my_menu import TextEditMenu


class SearchLineEdit(QLineEdit):
    """ 搜索框 """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(382, 40)
        self.setPlaceholderText('用户、群组和消息')
        self.menu = TextEditMenu(self)

    def contextMenuEvent(self, e):
        """ 右击菜单事件 """
        if not self.text():
            return
        self.menu.exec_(e.globalPos())
