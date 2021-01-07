# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from widget.my_button import ThreeStateToolButton


class DialogTitlebar(QWidget):
    """ 会话标题栏 """

    def __init__(self, contactName: str, parent=None):
        """ 初始化标题栏

        Parameters
        ----------
        contactName : str
            会话中联系人的名称

        parent : QWidget
            父级窗口
        """
        super().__init__(parent=parent)
        self.contactName = contactName
        self.contactNamesLabel = QLabel(contactName, self)
        # 初始化窗口
        self.__initWidget()

    def __initWidget(self):
        """ 初始化窗口 """


    def setcontactNamesName(self, contactName: str):
        """ 设置标题栏联系人名称 """
        self.contactName = contactName
        self.contactNamesLabel.setText(contactName)
