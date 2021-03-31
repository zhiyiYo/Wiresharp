# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from PyQt5.QtWidgets import QWidget


class HeadPortraitMask(QWidget):
    """ 头像遮罩 """

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(150, 150)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.__isPressed = False
        self.__iconPixmap = QPixmap(
            r'app\resource\Image\welcome_interface\编辑头像.png')

    def mousePressEvent(self, e):
        self.__isPressed = True
        self.update()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.__isPressed = False
        self.update()
        super().mouseReleaseEvent(e)
        self.clicked.emit()

    def paintEvent(self, e):
        """ 绘制背景和图标 """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        alpha = 0.13 if self.__isPressed else 0.7
        painter.setOpacity(alpha)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.drawRoundedRect(self.rect(), 75, 175)
        painter.drawPixmap(0, 0, self.__iconPixmap)
