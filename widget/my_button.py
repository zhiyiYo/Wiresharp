# coding:utf-8"
from typing import Dict

from PyQt5.QtCore import QEvent, QPoint, QSize, Qt, QRect
from PyQt5.QtGui import (QBrush, QColor, QIcon, QPainter, QPen,
                         QPixmap, QFontMetrics, QFont)
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
        self.resize(*icon_size)
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
        iconPath_dict : dict
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
            key: QPixmap(iconPath_dict[key]) for key in iconPath_dict.keys()}
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


class NavigationButton(QPushButton):
    """ 导航界面按钮 """

    def __init__(self, iconPath_dict: dict, text: str, buttonSize: tuple = (26, 42), parent=None):
        """ 初始化按钮

        Parameters
        ----------
        iconPath_dict : dict
            按钮图标路径字典，分别对应字典的三个键 `normal`、`hover` 和 `selected`

        text : str
            按扭的文字

        buttonSize : tuple
            按钮大小

        parent : QWidget
            父级窗口
        """
        super().__init__(text, parent)
        self.resize(*buttonSize)
        self.setIcon(iconPath_dict)
        self.__state = 'normal'
        self.__isPressed = False
        # 初始化
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.installEventFilter(self)

    def setText(self, text: str):
        """ 设置按钮文字 """
        super().setText(text)
        self.update()

    def setIcon(self, iconPath_dict: dict):
        """ 设置按钮图标 """
        self.__iconPath_dict = iconPath_dict
        self.__iconPixmap_dict = {
            key: QPixmap(self.__iconPath_dict[key])
            for key in iconPath_dict.keys()
        }   # type:Dict[str,QPixmap]
        self.update()

    def setSelected(self, isSelected: bool):
        """ 设置按钮选中状态 """
        self.__state = 'selected' if isSelected else 'normal'
        self.update()

    def eventFilter(self, obj, e: QEvent):
        """ 过滤事件 """
        if obj is self:
            if e.type() in [QEvent.Enter, QEvent.Leave, QEvent.MouseButtonRelease, QEvent.MouseButtonPress]:
                if e.type() == QEvent.Enter and self.__state != 'selected':
                    self.__state = 'hover'
                elif e.type() == QEvent.Leave and self.__state != 'selected':
                    self.__state = 'normal'
                elif e.type() == QEvent.MouseButtonPress:
                    self.__isPressed = True
                elif e.type() == QEvent.MouseButtonRelease:
                    self.__isPressed = False
                    self.__state = 'selected'
                self.update()
                return False
        return super().eventFilter(obj, e)

    def paintEvent(self, e):
        """ 绘制图标和文字 """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        painter.setOpacity(0.22 if self.__isPressed else 1)
        # 绘制图标
        p = self.__iconPixmap_dict[self.__state]
        painter.drawPixmap(int(self.width() / 2 - p.width() / 2), 0, p)
        # 绘制文字
        color = (0, 120, 212) if self.__state == 'selected' else (158, 162, 166)
        painter.setPen(QPen(QColor(*color)))
        painter.setFont(QFont('Microsoft YaHei', 8))
        painter.drawText(0, 41, self.text())


class OpacityThreeStateToolButton(QToolButton):
    """ 根据状态的不同改变图标透明度的工具按钮 """

    def __init__(self, iconPath: str, opacity_dict: dict, buttonSize: tuple = (40, 45), parent=None):
        """ 初始化按钮

        Parameters
        ----------
        iconPath : str
            按钮图标路径

        opacity_dict : dict
            按钮透明度字典，分别对应 `normal`、`hover` 和 `pressed` 三种状态

        buttonSize : tuple
            按钮大小

        parent : QWidget
            父级窗口
        """
        super().__init__(parent=parent)
        self.__iconPath = iconPath
        self.opacity_dict = opacity_dict
        self.__state = 'normal'
        self.resize(*buttonSize)
        self.installEventFilter(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def eventFilter(self, obj, e: QEvent):
        """ 过滤事件 """
        if obj is self:
            if e.type() in [QEvent.Enter, QEvent.Leave, QEvent.MouseButtonPress, QEvent.MouseButtonRelease]:
                if e.type() in [QEvent.Leave, QEvent.MouseButtonRelease]:
                    self.__state = 'normal'
                elif e.type() == QEvent.Enter:
                    self.__state = 'hover'
                elif e.type() == QEvent.MouseButtonPress:
                    self.__state = 'pressed'
                self.update()
                return False
        return super().eventFilter(obj, e)

    def paintEvent(self, e):
        """ 绘制按钮 """
        painter = QPainter(self)
        painter.setOpacity(self.opacity_dict[self.__state])
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        # 绘制图标
        painter.drawPixmap(self.rect(), QPixmap(self.__iconPath))
