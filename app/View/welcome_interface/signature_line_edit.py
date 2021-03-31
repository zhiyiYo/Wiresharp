# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

from app.components.widgets.my_button import OpacityThreeStateToolButton
from app.components.widgets.my_line_edit import LineEdit


class SignatureLineEdit(LineEdit):
    """ 个性签名编辑框 """

    changeSignatureSignal = pyqtSignal(str)

    def __init__(self, text='', parent=None):
        super().__init__(text=text, parent=parent)
        opacity_dict = {'normal': 0.54, 'hover': 1, 'pressed': 0.2}
        self.editButton = OpacityThreeStateToolButton(
            r'app\resource\Image\welcome_interface\编辑个性签名.png', opacity_dict, (27, 28), self)
        self.resize(564, 50)
        self.editButton.move(532, 11)
        self.editButton.clicked.connect(self.__editButtonClickedSlot)

    def __editButtonClickedSlot(self):
        """ 按下编辑按钮后的槽函数 """
        if not self.hasFocus():
            self.setFocus()
        else:
            self.clearFocus()

    def focusInEvent(self, e):
        """ 更新图标 """
        self.editButton.setOpacityIcon(
            r'app\resource\Image\welcome_interface\确认个性签名.png')
        super().focusInEvent(e)

    def focusOutEvent(self, e):
        """ 更新图标并发送更新签名的信号 """
        self.editButton.setOpacityIcon(
            r'app\resource\Image\welcome_interface\编辑个性签名.png')
        super().focusOutEvent(e)
        self.changeSignatureSignal.emit(self.text())
