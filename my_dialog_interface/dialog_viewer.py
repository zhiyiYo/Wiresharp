# coding:utf-8
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QFont
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication, QScrollBar

from widget.my_scroll_area import ScrollArea
from .dialog_message_widget import DialogMessageWidget


class ScrollWidget(QWidget):
    """ 会话视图的滚动小部件 """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def paintEvent(self, e):
        """ 绘制背景 """
        super().paintEvent(e)
        painter = QPainter(self)
        # 绘制分割线
        painter.setPen(QPen(QColor(244, 244, 244)))
        lineWidth = int((self.width() - 268) / 2)
        painter.drawLine(100, 28, 100 + lineWidth, 29)
        painter.drawLine(self.width()-lineWidth -
                         100, 28, self.width()-100, 29)
        painter.setPen(QPen(QColor(220, 221, 222)))
        painter.drawLine(100, 29, 100 + lineWidth, 30)
        painter.drawLine(self.width()-lineWidth -
                         100, 29, self.width()-100, 30)
        # 添加文字
        painter.setPen(QPen(QColor(138, 141, 145)))
        painter.setFont(QFont('Microsoft YaHei', 9))
        painter.drawText(100 + lineWidth + 20, 36, '今天')


class DialogViewer(ScrollArea):
    """ 会话视图 """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 实例化小部件
        self.scrollWidget = ScrollWidget(self)
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self.messageWidget_list = []  # type:List[DialogMessageWidget]
        self.leftMessageWidget_list = []
        self.rightMessageWidget_list = []
        # 初始化窗口
        self.__initWidget()

    def __initWidget(self):
        """ 初始化窗口 """
        # 调整大小
        self.resize(877, 557)
        self.scrollWidget.resize(self.size())
        # 设置布局
        self.setWidget(self.scrollWidget)
        # 隐藏水平滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 设置层叠样式
        self.__setQss()

    def addMessageWidget(self, contactName: str, imagePath: str, message: str, direction: str = 'left'):
        """ 向视图中添加聊天气泡

        Parameters
        ----------
        contactName : str
            用户名

        imagePath : str
            用户头像路径

        message : str
            对话消息

        direction : str
            气泡方向，有 `left` 和 `right` 两种
        """
        messageWidget = DialogMessageWidget(
            contactName, imagePath, message, direction, self.scrollWidget)
        messageWidget.resize(self.width(), messageWidget.height())

        # 设置小部件的位置
        if self.messageWidget_list:
            y = self.messageWidget_list[-1].y() + \
                self.messageWidget_list[-1].height()
        else:
            y = 58
        messageWidget.move(0, y+12)

        # 将对话消息小部件添加到列表中
        self.messageWidget_list.append(messageWidget)
        if message == 'left':
            self.leftMessageWidget_list.append(messageWidget)
        else:
            self.rightMessageWidget_list.append(messageWidget)

        # 调整窗口大小
        newHeight = y + messageWidget.height() + 10
        self.scrollWidget.resize(
            self.width(), max(self.scrollWidget.height(), newHeight + 10))
        # 强制更新层叠样式
        messageWidget.show()
        self.setStyle(QApplication.style())
        # 自动滚动到底部
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def resizeEvent(self, e):
        """ 调整窗口大小 """
        self.verticalScrollBar().move(-1, 20)
        self.verticalScrollBar().resize(
            self.verticalScrollBar().width(), self.height() - 40)
        self.scrollWidget.resize(self.width(), self.scrollWidget.height())
        for widget in self.messageWidget_list:
            widget.resize(self.width(), widget.height())

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'resource\qss\dialog_viewer.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
