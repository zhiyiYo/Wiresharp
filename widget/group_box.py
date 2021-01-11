# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel


class GroupBox(QWidget):
    """ 分组框 """

    def __init__(self, title: str = '', parent=None):
        super().__init__(parent=parent)
        self.title = title
