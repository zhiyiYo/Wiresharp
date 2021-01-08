# coding:utf-8

""" 自定义按钮库"""


from PyQt5.QtCore import QEvent, QPoint, QSize, Qt
from PyQt5.QtGui import (QBrush, QColor, QIcon, QPainter, QPen,
                         QPixmap)
from PyQt5.QtWidgets import (QApplication, QGraphicsBlurEffect, QLabel,
                             QPushButton, QToolButton)


class ThreeStatePushButton(QPushButton):
    """ 三态按钮 """

    def __init__(self, iconPath_dict: dict, text='', iconSize: tuple = (130, 17), parent=None):
        super().__init__(text, parent)
        self.__iconPath_dict = iconPath_dict
        self.setIcon(QIcon(self.__iconPath_dict['normal']))
        self.setIconSize(QSize(*iconSize))
        self.installEventFilter(self)

    def eventFilter(self, obj, e):
        """ 当鼠标移到播放模式按钮上时更换图标 """
        if obj == self:
            if e.type() in [QEvent.Enter, QEvent.HoverMove]:
                self.setIcon(QIcon(self.__iconPath_dict['hover']))
            elif e.type() in [QEvent.Leave, QEvent.MouseButtonRelease]:
                self.setIcon(QIcon(self.__iconPath_dict['normal']))
            elif e.type() == QEvent.MouseButtonPress:
                self.setIcon(QIcon(self.__iconPath_dict['pressed']))
        return False


class ThreeStateToolButton(QToolButton):
    """ 三种状态对应三种图标的按钮，iconPath_dict提供按钮normal、hover、pressed三种状态下的图标地址 """

    def __init__(self, iconPath_dict: dict, icon_size: tuple = (50, 50), parent=None):
        super().__init__(parent)
        # 引用图标地址字典
        self.iconPath_dict = iconPath_dict
        self.resize(icon_size[0], icon_size[1])
        # 初始化小部件
        self.initWidget()

    def initWidget(self):
        """ 初始化小部件 """
        self.setCursor(Qt.ArrowCursor)
        self.setIcon(QIcon(self.iconPath_dict['normal']))
        self.setIconSize(QSize(self.width(), self.height()))
        self.setStyleSheet('border: none; margin: 0px')

    def enterEvent(self, e):
        """ hover时更换图标 """
        self.setIcon(QIcon(self.iconPath_dict['hover']))

    def leaveEvent(self, e):
        """ leave时更换图标 """
        self.setIcon(QIcon(self.iconPath_dict['normal']))

    def mousePressEvent(self, e):
        """ 鼠标左键按下时更换图标 """
        if e.button() == Qt.RightButton:
            return
        self.setIcon(QIcon(self.iconPath_dict['pressed']))
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        """ 鼠标左键按下时更换图标 """
        if e.button() == Qt.RightButton:
            return
        self.setIcon(QIcon(self.iconPath_dict['normal']))
        super().mouseReleaseEvent(e)


class CircleButton(QToolButton):
    """ 圆形工具按钮 """

    def __init__(self, iconPath_dict: dict, radius=25, parent=None):
        """ 初始化按钮

        Parameters
        ----------
        iconPath : dict
            按钮图标路径字典，包含 `normal`、'hover' 和 `pressed` 三个键以及对应的图标路径

        radius : int
            按钮半径大小

        parent : QWidget
            父级窗口
        """
        super().__init__(parent=parent)
        self.__radius = radius
        self.__state = 'normal'
        self.__bgColor = QColor(241, 241, 241)
        self.__iconPath_dict = iconPath_dict
        self.__iconPixmap_dict = {
            key: QPixmap(iconPath_dict[key]).scaled(
                radius, radius, Qt.KeepAspectRatio, Qt.SmoothTransformation) for key in iconPath_dict.keys()}
        self.__initWidget()

    def __initWidget(self):
        """ 初始化界面 """
        self.installEventFilter(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(2 * self.__radius, 2 * self.__radius)

    def eventFilter(self, obj, e: QEvent):
        """ 过滤事件 """
        if obj is self:
            if e.type() in [QEvent.Enter, QEvent.Leave, QEvent.MouseButtonPress, QEvent.MouseButtonRelease]:
                if e.type() in [QEvent.Leave, QEvent.MouseButtonRelease]:
                    self.__state = 'normal'
                    self.__bgColor = QColor(241, 241, 241)
                elif e.type() == QEvent.Enter:
                    self.__state = 'hover'
                    self.__bgColor = QColor(229, 228, 232)
                elif e.type() == QEvent.MouseButtonPress:
                    self.__state = 'pressed'
                    self.__bgColor = QColor(249, 249, 250)
                self.update()
                return False
        return super().eventFilter(obj, e)

    def paintEvent(self, e):
        """ 绘制按钮 """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        # 绘制背景
        brush = QBrush(self.__bgColor)
        painter.setBrush(brush)
        painter.drawRoundedRect(self.rect(), self.__radius, self.__radius)
        # 绘制图标
        painter.drawPixmap(self.rect(), self.__iconPixmap_dict[self.__state])
