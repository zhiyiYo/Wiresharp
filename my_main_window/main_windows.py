# coding:utf-8
from ctypes import POINTER, cast
from ctypes.wintypes import HWND, MSG, POINT

from PyQt5.QtCore import Qt
from win32.lib import win32con
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication
from win32 import win32api, win32gui

from effects import WindowEffect
from my_title_bar import TitleBar
from my_dialog_interface import DialogInterface
from my_navigation_interface import NavigationInterface

from .monitor_functions import isMaximized
from .c_structures import *


class WireSharp(QWidget):
    """ WireSharp 聊天界面 """

    BORDER_WIDTH = 5

    def __init__(self):
        super().__init__()
        # 实例化小部件
        self.titleBar = TitleBar(self)
        self.dialogInterface = DialogInterface(self)
        self.navigationInterface = NavigationInterface(self)
        self.chatListWidget = self.navigationInterface.chatListWidget
        # 初始化界面
        self.__initWidget()

    def __initWidget(self):
        """ 初始化界面 """
        self.setWindowFlags(Qt.FramelessWindowHint)
        WindowEffect.setShadowEffect(self.winId())
        WindowEffect.setWindowAnimation(self.winId())
        self.navigationInterface.move(0, 40)
        self.resize(1279, 957)
        # 在去除任务栏的显示区域居中显示
        desktop = QApplication.desktop().availableGeometry()
        self.move(int(desktop.width() / 2 - self.width() / 2),
                  int(desktop.height() / 2 - self.height() / 2))

    def resizeEvent(self, e):
        """ 调整窗口大小 """
        if hasattr(self, 'dialogInterface'):
            self.dialogInterface.move(403, 40)
            self.dialogInterface.resize(self.width() - 402, self.height() - 40)
        self.titleBar.resize(self.width(), self.titleBar.height())

    def nativeEvent(self, eventType, message):
        """ 处理windows消息 """
        msg = MSG.from_address(message.__int__())
        if msg.message == win32con.WM_NCHITTEST:
            xPos = win32api.LOWORD(msg.lParam) - self.frameGeometry().x()
            yPos = win32api.HIWORD(msg.lParam) - self.frameGeometry().y()
            w, h = self.width(), self.height()
            lx = xPos < self.BORDER_WIDTH
            rx = xPos + 9 > w - self.BORDER_WIDTH
            ty = yPos < self.BORDER_WIDTH
            by = yPos > h - self.BORDER_WIDTH
            if (lx and ty):
                return True, win32con.HTTOPLEFT
            elif (rx and by):
                return True, win32con.HTBOTTOMRIGHT
            elif (rx and ty):
                return True, win32con.HTTOPRIGHT
            elif (lx and by):
                return True, win32con.HTBOTTOMLEFT
            elif ty:
                return True, win32con.HTTOP
            elif by:
                return True, win32con.HTBOTTOM
            elif lx:
                return True, win32con.HTLEFT
            elif rx:
                return True, win32con.HTRIGHT
        elif msg.message == win32con.WM_NCCALCSIZE:
            if isMaximized(msg.hWnd):
                WindowEffect.adjustMaximizedClientRect(
                    HWND(msg.hWnd), msg.lParam)
            return True, 0
        if msg.message == win32con.WM_GETMINMAXINFO:
            if isMaximized(msg.hWnd):
                window_rect = win32gui.GetWindowRect(msg.hWnd)
                if not window_rect:
                    return False, 0
                # 获取显示器句柄
                monitor = win32api.MonitorFromRect(window_rect)
                if not monitor:
                    return False, 0
                # 获取显示器信息
                monitor_info = win32api.GetMonitorInfo(monitor)
                monitor_rect = monitor_info['Monitor']
                work_area = monitor_info['Work']
                # 将lParam转换为MINMAXINFO指针
                info = cast(
                    msg.lParam, POINTER(MINMAXINFO)).contents
                # 调整位置
                info.ptMaxSize.x = work_area[2] - work_area[0]
                info.ptMaxSize.y = work_area[3] - work_area[1]
                info.ptMaxTrackSize.x = info.ptMaxSize.x
                info.ptMaxTrackSize.y = info.ptMaxSize.y
                # 修改放置点的x,y坐标
                info.ptMaxPosition.x = abs(
                    window_rect[0] - monitor_rect[0])
                info.ptMaxPosition.y = abs(
                    window_rect[1] - monitor_rect[1])
                return True, 1
        return QWidget.nativeEvent(self, eventType, message)
