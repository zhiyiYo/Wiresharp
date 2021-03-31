# coding:utf-8
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QBrush, QColor
from PyQt5.QtWidgets import QLabel, QMenu, QAction, QApplication

from app.common.window_effect import WindowEffect


class StateWidget(QLabel):
    """ 用户状态小部件 """

    def __init__(self, state: str = '在线', isClickable: bool = True, bgColor: tuple = (240, 244, 248), parent=None):
        """ 初始化状态小部件

        Parameters
        ----------
        state : str
            用户状态，有`在线`、`离开`、`请勿打扰`和`隐身`四种

        isClickable : bool
            是否可点击

        bgColor : tuple
            背景颜色

        parent : QWidget
            父级窗口
        """
        super().__init__(parent=parent)
        self.isClickable = isClickable
        self.bgColor = bgColor
        self.state_list = ['在线', '离开', '请勿打扰', '隐身']
        iconPath_dict = {
            '在线': r'app\resource\Image\navigation_interface\在线.png',
            '离开': r'app\resource\Image\navigation_interface\离开.png',
            '隐身': r'app\resource\Image\navigation_interface\隐身.png',
            '请勿打扰': r'app\resource\Image\navigation_interface\请勿打扰.png',
            '下拉菜单箭头': r'app\resource\Image\navigation_interface\下拉菜单箭头.png'
        }
        self.__iconPixmap_dict = {
            key: QPixmap(iconPath_dict[key]) for key in iconPath_dict.keys()
        }
        # 初始化界面
        self.setFixedSize(16, 16)
        self.setState(state)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.__setQss()

    def setState(self, state: str):
        """ 设置状态，状态有`在线`、`离开`、`请勿打扰`和`隐身`四种"""
        if state not in self.state_list:
            raise Exception('状态只能是 `在线`、`离开`、`请勿打扰`和`隐身` 中的一种')
        self.state = state
        self.setPixmap(self.__iconPixmap_dict[state])

    def enterEvent(self, e):
        if self.isClickable:
            self.setPixmap(self.__iconPixmap_dict['下拉菜单箭头'])

    def leaveEvent(self, e):
        self.setPixmap(self.__iconPixmap_dict[self.state])

    def mouseReleaseEvent(self, QMouseEvent):
        """ 显示下拉菜单 """
        if not self.isClickable:
            super().mouseReleaseEvent(QMouseEvent)
            return
        menu = QMenu(self)
        windowEffect = WindowEffect()
        menu.setObjectName('stateMenu')
        menu.setWindowFlags(menu.windowFlags() | Qt.NoDropShadowWindowHint)
        windowEffect.addShadowEffect(menu.winId())
        action_list = []
        for state in self.state_list:
            if state != self.state:
                act = QAction(state, self)
            else:
                act = QAction(
                    QIcon(r'app\resource\Image\navigation_interface\选中状态.png'), state, self)
            action_list.append(act)
            act.triggered.connect(lambda x, s=state: self.setState(s))
        menu.addActions(action_list)
        menu.exec(QPoint(self.window().x(), self.window().y()+109))

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'app\resource\qss\text_edit_menu.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def setBackgroundColor(self, color: tuple):
        """ 设置背景色 """
        self.bgColor = color
        self.update()

    def paintEvent(self, e):
        """ 绘制背景 """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(*self.bgColor)))
        painter.drawRoundedRect(self.rect(), 8, 8)
        super().paintEvent(e)
