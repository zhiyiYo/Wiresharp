# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QBrush
from PyQt5.QtWidgets import QWidget


class HeadPortrait(QWidget):
    """ 用户头像 """

    def __init__(self, imagePath: str, headPortraitSize: tuple = (50, 50), parent=None):
        """ 初始化头像

        Parameters
        ----------
        imagePath : str
            头像图像的路径

        headPortraitSize : tuple
            头像的大小

        parent : QWidget
            父级窗口
        """
        super().__init__(parent=parent)
        self.setFixedSize(*headPortraitSize)
        self.__imagePixmap = QPixmap(imagePath).scaled(
            *headPortraitSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # type:QPixmap

    def setHeadPortrait(self, imagePath: str):
        """ 更新用户头像 """
        self.__imagePixmap = QPixmap(imagePath).scaled(
            *self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.update()

    def paintEvent(self, e):
        """ 绘制头像 """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.__imagePixmap))
        radius = min(self.width() / 2, self.height() / 2)
        painter.drawRoundedRect(self.rect(), radius, radius)
