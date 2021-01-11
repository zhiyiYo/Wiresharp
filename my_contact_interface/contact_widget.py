# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel

from widget.head_portrait import HeadPortrait


class ContactWidget(QWidget):
    """ 联系人小部件 """

    selectContactSignal = pyqtSignal(dict)

    def __init__(self, contactInfo: dict, parent=None):
        """ 创建联系人小部件

        Parameters
        ----------
        contactInfo : dict
            联系人信息字典，要求具有以下形式::

            contactInfo = {
                'IP': str,
                'contactName': str,
                'headPortraitPath': str
            }
        """
        super().__init__(parent=parent)
        self.contactInfo = contactInfo.copy()
        self.contactName = contactInfo['contactName']  # type:str
        self.IP = contactInfo['IP']  # type:str
        # 实例化小部件
        self.contactNameLabel = QLabel(self.contactName, self)
        self.headPortraitWidget = HeadPortrait(
            self.contactInfo['headPortraitPath'], parent=self)
        self.windowMask = QWidget(self)
        # 初始化窗口
        self.__initWidget()

    def __initWidget(self):
        """ 初始化窗口 """
        self.setFixedSize(402, 74)
        self.windowMask.resize(self.size())
        self.windowMask.hide()
        self.headPortraitWidget.move(12, 10)
        self.contactNameLabel.move(75, 23)
        # 设置层叠样式
        self.setAttribute(Qt.WA_StyledBackground)
        self.contactNameLabel.setObjectName('contactNameLabel')
        self.windowMask.setObjectName('windowMask')
        self.__setQss()

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'resource\qss\contact_widget.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.windowMask.show()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.windowMask.hide()
        self.selectContactSignal.emit(self.contactInfo)
