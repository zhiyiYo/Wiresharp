# coding:utf-8
from typing import List, Union

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QListWidgetItem, QLabel, QAction, QMenu

from app.common.window_effect import WindowEffect
from app.components.widgets.my_listWidget import ListWidget
from app.components.widgets.my_button import ThreeStateToolButton
from .contact_widget import ContactWidget


class ContactListWidget(ListWidget):
    """ 消息框列表控件 """

    selectContactSignal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.contactWidget_list = []  # type:List[ContactWidget]
        self.item_list = []  # type:List[QListWidgetItem]
        # 实例化小部件
        self.addToFavoritesAct = QAction('添加到收藏夹', self)
        self.viewProfileAct = QAction('查看个人资料', self)
        self.editContactAct = QAction('编辑联系人', self)
        self.contextMenu = QMenu(self)
        self.windowEffect = WindowEffect()
        # 初始化窗口
        self.__initWidget()

    def __initWidget(self):
        """ 初始化窗口 """
        self.resize(402, 74)
        self.setFixedWidth(402)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 将动作添加到菜单
        self.contextMenu.setWindowFlags(
            self.contextMenu.windowFlags() | Qt.NoDropShadowWindowHint)
        self.windowEffect.addShadowEffect(self.contextMenu.winId())
        self.contextMenu.addActions(
            [self.addToFavoritesAct, self.viewProfileAct, self.editContactAct])
        # 设置层叠样式
        self.__setQss()
        # 信号连接到槽
        self.__connectSignalToSlot()

    def addContactWidget(self, contact: Union[dict, ContactWidget]):
        """ 添加联系人小部件

        Parameters
        ----------
        contact : Union[dict, ContactWidget]
            联系人信息字典或者联系人小部件，如果是字典，要求具有以下形式::

            contact = {
                'IP': str,
                'contactName': str,
                'headPortraitPath': str
            }
        """
        if isinstance(contact, dict):
            contactWidget = ContactWidget(contact, self)
        else:
            contactWidget = contact
        item = QListWidgetItem(self)
        item.setSizeHint(contactWidget.size())
        self.setItemWidget(item, contactWidget)
        self.contactWidget_list.append(contactWidget)
        self.item_list.append(item)
        self.resize(402, self.count() * contactWidget.height())
        contactWidget.selectContactSignal.connect(self.selectContactSignal)

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'app\resource\qss\contact_list_widget.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def contactCount(self):
        """ 返回联系人框的个数 """
        return self.count()

    def contextMenuEvent(self, e):
        """ 右击菜单事件 """
        hitIndex = self.indexAt(e.pos()).column()
        # 显示右击菜单
        if hitIndex > -1:
            self.contextMenu.exec(self.cursor().pos())

    def __connectSignalToSlot(self):
        """ 信号连接到槽 """
