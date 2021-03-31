# coding:utf-8
import os
import json

from PyQt5.QtCore import Qt, QPoint, QEvent, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QToolButton, QFileDialog

from app.components.widgets.my_line_edit import LineEdit
from app.components.widgets.circle_widget import CircleWidget
from app.components.widgets.head_portrait import HeadPortrait
from app.common.functions.user_info import getUserInfo, writeUserInfo
from .head_portrait_mask import HeadPortraitMask
from .signature_line_edit import SignatureLineEdit


class WelcomeInterface(QWidget):
    """ 还原界面 """

    changeUserInfoSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.userInfo = getUserInfo()
        # 实例化小部件
        self.lineEdit = SignatureLineEdit(
            self.userInfo['personalSignature'], self)
        self.startConvButton = QToolButton(self)
        self.welcomeLabel = QLabel(f'欢迎, {self.userInfo["userName"]}', self)
        self.promptLabel = QLabel('搜索他人以开始聊天，或转到"联系人"以查看谁有空。', self)
        self.headPortraitWidget = HeadPortrait(
            self.userInfo['headPortraitPath'], (150, 150), self)
        self.headPortraitMask = HeadPortraitMask(self.headPortraitWidget)
        self.stateWidget = CircleWidget(
            r'app\resource\Image\welcome_interface\在线.png', 24, parent=self.headPortraitWidget)
        # 初始化窗口
        self.__initWidget()

    def __initWidget(self):
        """ 初始化窗口 """
        self.headPortraitMask.hide()
        self.lineEdit.setAlignment(Qt.AlignHCenter)
        self.lineEdit.setPlaceholderText('告诉朋友们你在忙什么')
        # 设置层叠样式
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName('welcomeInterface')
        self.promptLabel.setObjectName('promptLabel')
        self.welcomeLabel.setObjectName('welcomeLabel')
        self.lineEdit.setObjectName('lineEdit')
        self.__setQss()
        # 调整小部件大小
        self.resize(877, 917)

        self.startConvButton.resize(138, 50)
        self.welcomeLabel.resize(self.width(), 60)
        self.promptLabel.resize(self.width(), 30)
        # 标签水平居中
        self.promptLabel.setAlignment(Qt.AlignHCenter)
        self.welcomeLabel.setAlignment(Qt.AlignHCenter)
        # 调整小部件位置
        self.stateWidget.move(116, 116)
        self.welcomeLabel.move(0, 137)
        self.promptLabel.move(0, 603)
        # 安装事件过滤器
        self.headPortraitWidget.installEventFilter(self)
        # 信号连接到槽
        self.__connectSignalToSlot()

    def resizeEvent(self, e):
        """ 调整窗口大小 """
        self.promptLabel.move(
            int(self.width() / 2 - self.promptLabel.width() / 2), 603)
        self.welcomeLabel.move(
            int(self.width() / 2 - self.welcomeLabel.width() / 2), 137)
        self.headPortraitWidget.move(
            int(self.width() / 2 - self.headPortraitWidget.width() / 2), 243)
        self.startConvButton.move(
            int(self.width() / 2 - self.startConvButton.width() / 2), 514)
        self.lineEdit.move(
            int(self.width() / 2 - self.lineEdit.width() / 2), 422)

    def __setQss(self):
        """ 设置层叠样式表 """
        with open(r'app\resource\qss\welcome_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def eventFilter(self, obj, e: QEvent):
        """ 过滤事件 """
        if obj is self.headPortraitWidget:
            if e.type() == QEvent.Enter:
                self.headPortraitMask.show()
                return False
            elif e.type() == QEvent.Leave:
                self.headPortraitMask.hide()
                return False
        return super().eventFilter(obj, e)

    def __editHeadPortraitSlot(self):
        """ 编辑用户头像 """
        path, filterType = QFileDialog.getOpenFileName(
            self, '打开', './', '所有文件(*.png;*.jpg;*.jpeg;*jpe;*jiff)')
        if path:
            # 复制图片到封面文件夹下
            if os.path.abspath(self.userInfo['headPortraitPath']) == path:
                return
            # 暂存图片地址并刷新图片
            self.userInfo['headPortraitPath'] = path
            self.headPortraitWidget.setHeadPortrait(path)
            # 更新用户信息
            writeUserInfo(self.userInfo)
            # 发出更新头像的信号
            self.changeUserInfoSignal.emit()

    def __editPersonalSignatureSlot(self, text: str):
        """ 更新个性签名槽函数 """
        self.userInfo['personalSignature'] = text
        writeUserInfo(self.userInfo)
        self.changeUserInfoSignal.emit()

    def __connectSignalToSlot(self):
        """ 信号连接到槽 """
        self.headPortraitMask.clicked.connect(self.__editHeadPortraitSlot)
        self.lineEdit.changeSignatureSignal.connect(
            self.__editPersonalSignatureSlot)
