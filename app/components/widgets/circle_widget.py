# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from PyQt5.QtWidgets import QWidget


class CircleWidget(QWidget):
    """ 圆形小部件 """

    def __init__(self, iconPath: str, radius: int, bgColor: tuple = (255, 255, 255), parent=None):
        """ 初始化圆心小部件

        Parameters
        ----------
        iconPath :str
            图标路径

        radius : int
            圆形背景半径

        bgColor : tuple
            背景色

        parent : QWidget
            父级窗口
        """
        super().__init__(parent=parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.__iconPixmap = QPixmap(iconPath)
        self.resize(radius, radius)
        self.bgColor = bgColor
        self.radius = radius

    def setIcon(self, iconPath: str):
        """ 设置图标 """
        self.__iconPixmap = QPixmap(iconPath)
        self.update()

    def setBackgroundColor(self, bgColor: tuple):
        """ 设置背景色 """
        self.bgColor = bgColor
        self.update()

    def paintEvent(self, e):
        """ 绘制背景 """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(*self.bgColor)))
        painter.drawRoundedRect(self.rect(), self.radius, self.radius)
        painter.drawPixmap(0, 0, self.__iconPixmap)
