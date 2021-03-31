# coding:utf-8
import os

from bs4 import BeautifulSoup
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import (QBrush, QColor, QDesktopServices, QFont, QFontMetrics,
                         QPainter, QPalette, QTextDocument, QMovie)
from PyQt5.QtWidgets import QLabel, QSizePolicy, QTextEdit, QWidget


class MessageBubble(QLabel):
    """ 消息气泡 """

    def __init__(self, message: str, direction: str = 'left', parent=None):
        """ 初始化消息气泡

        Parameters
        ----------
        message : str
            对话消息

        direction : str
            气泡方向，有 `left` 和 `right` 两种

        parent : QWidget
            父级窗口
        """
        super().__init__(message, parent)
        self.message = message
        if direction not in ['left', 'right']:
            raise Exception('气泡方向只能是 `left` 或者 `right`')
        self.direction = direction
        self.__bgColor_dict = {
            'left': QColor(242, 246, 249),
            'right': QColor(219, 244, 253)
        }
        self.bgColor = self.__bgColor_dict[direction]  # type:QColor
        self.maxWidth = 525
        # 初始化窗口
        self.__initWidget()

    def __initWidget(self):
        """ 初始化窗口 """
        self.resize(575, 50)
        # 设置文本可选中
        self.setTextInteractionFlags(
            Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        # 设置层叠样式
        self.__setQss()
        # 如果信息不是HTML格式，就调整气泡宽度
        if not BeautifulSoup(self.message, 'html.parser').find():
            self.setWordWrap(True)
            self.adjustSize_()
        else:
            # 如果有动图就设置一个QMovie
            img = BeautifulSoup(self.message, 'html.parser').find('img')
            if img and img.get('src') and img.get('src').endswith('.gif'):
                movie = QMovie(img.get('src'))
                self.setMovie(movie)
                movie.start()
            self.adjustSize()
        # 信号连接到槽函数
        self.linkActivated.connect(
            lambda x: QDesktopServices.openUrl(QUrl('file:///'+os.path.realpath(x))))

    def adjustSize_(self):
        """ 调整大小 """
        self.adjustWidth()
        self.adjustSize()
        if self.width() < self.maxWidth:
            self.resize(self.width(), 54)

    def adjustWidth(self):
        """ 根据消息长度调整气泡长度 """
        fontMetrics = QFontMetrics(QFont('Microsoft YaHei', 12))
        width = fontMetrics.width(self.text()) + 35
        self.setFixedWidth(min(width, self.maxWidth))

    def __setQss(self):
        """ 设置层叠样式表 """
        with open(r'app\resource\qss\message_bubble.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def paintEvent(self, e):
        """ 绘制边框 """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(self.bgColor)))
        painter.drawRoundedRect(self.rect(), 10, 10)
        if self.direction == 'left':
            painter.drawRect(0, 0, 10, 10)
        else:
            painter.drawRect(self.width()-10, 0, self.width(), 10)
        super().paintEvent(e)
