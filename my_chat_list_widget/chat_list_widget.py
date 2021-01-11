# coding:utf-8
from typing import List

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QListWidgetItem, QLabel, QAction, QMenu

from effects import WindowEffect
from widget.my_listWidget import ListWidget
from widget.my_button import ThreeStateToolButton
from .chat_widget import ChatWidget


class ChatListWidget(ListWidget):
    """ 消息框列表控件 """

    deleteChatSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 所有聊天的联系人信息字典
        self.IPContactName_dict = {}  # type:dict
        self.widgetIP_dict = {}  # widget为key
        self.IPWidget_dict = {}  # IP为key
        # 聊天小部件列表
        self.chatWidget_list = []  # type:List[ChatWidget]
        self.item_list = []  # type:List[QListWidgetItem]
        self.setViewportMargins(0, 55, 0, 0)
        # 实例化小部件
        iconPath = {
            'normal': r'resource\Image\navigation_interface\聊天按钮_normal.png',
            'hover': r'resource\Image\navigation_interface\聊天按钮_normal.png',
            'pressed': r'resource\Image\navigation_interface\聊天按钮_pressed.png',
        }
        self.searchLabel = QLabel(self)
        self.backgroundLabel = QLabel(self)
        self.showSortMenuArrow = QLabel(self)
        self.showSortMenuLabel = QLabel('近期聊天', self)
        self.chatButton = ThreeStateToolButton(iconPath, (89, 39), self)
        self.startChatInSkypeLabel = QLabel('开始在 Wiresharp 上聊天', self)
        self.useSearchLabel = QLabel('使用"搜索"在 Wiresharp 上查找任何人。', self)
        self.addToFavoritesAct = QAction('添加到收藏夹', self)
        self.viewProfileAct = QAction('查看个人资料', self)
        self.markUnreadAct = QAction('标记为未读', self)
        self.hideChatAct = QAction('隐藏对话', self)
        self.deleteChatAct = QAction('删除对话', self)
        self.contextMenu = QMenu(self)
        # 初始化窗口
        self.__initWidget()

    def __initWidget(self):
        """ 初始化窗口 """
        self.resize(402, 680)
        self.setFixedWidth(402)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.searchLabel.setAttribute(Qt.WA_TranslucentBackground)
        self.searchLabel.setPixmap(
            QPixmap(r'resource\Image\navigation_interface\查找.png'))
        self.backgroundLabel.setPixmap(
            QPixmap(QPixmap(r'resource\Image\navigation_interface\开始在Skype上聊天.png')))
        self.showSortMenuArrow.setPixmap(
            QPixmap(r'resource\Image\navigation_interface\排序聊天下拉菜单箭头.png'))
        # 移动小部件
        self.chatButton.move(300, 8)
        self.searchLabel.move(18, 329+55)
        self.useSearchLabel.move(46, 326+55)
        self.showSortMenuLabel.move(11, 18)
        self.showSortMenuArrow.move(75, 28)
        self.backgroundLabel.move(121, 117+55)
        self.startChatInSkypeLabel.move(48, 284+55)
        # 将动作添加到菜单
        WindowEffect.setShadowEffect(self.contextMenu.winId())
        self.contextMenu.addActions([self.addToFavoritesAct, self.viewProfileAct,
                                     self.markUnreadAct, self.hideChatAct, self.deleteChatAct])
        # 设置层叠样式
        self.startChatInSkypeLabel.setObjectName('startChatInSkypeLabel')
        self.showSortMenuLabel.setObjectName('showShortMenuLabel')
        self.useSearchLabel.setObjectName('useSearchLabel')
        self.__setQss()
        # 信号连接到槽
        self.__connectSignalToSlot()

    def addChatWidget(self, messageInfo: dict):
        """ 添加聊天小部件

        Parameters
        ----------
        messageInfo : dict
            对话消息字典，字典结构如下::

            messageInfo = {
                'contactName': str,
                'IP': str,
                'time': str,
                'message': str,
                'headPortraitPath': str
            }
        """
        chatWidget = ChatWidget(messageInfo, self)
        item = QListWidgetItem(self)
        item.setSizeHint(chatWidget.size())
        self.setItemWidget(item, chatWidget)
        self.chatWidget_list.append(chatWidget)
        self.item_list.append(item)
        # 将聊天人信息添加到字典中
        self.IPWidget_dict[messageInfo['IP']] = chatWidget
        self.widgetIP_dict[chatWidget] = messageInfo['IP']
        self.IPContactName_dict[messageInfo['IP']] = messageInfo['contactName']
        # 根据当前聊天框个数设置提示消息可见性
        self.__checkChatCount()

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'resource\qss\chat_list_widget.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def chatCount(self):
        """ 返回聊天框的个数 """
        return self.count()

    def setPromptMsgVisible(self, isVisible: bool):
        """ 设置提示消息的可见性 """
        self.searchLabel.setVisible(isVisible)
        self.useSearchLabel.setVisible(isVisible)
        self.backgroundLabel.setVisible(isVisible)
        self.startChatInSkypeLabel.setVisible(isVisible)

    def __checkChatCount(self):
        """ 根据聊天框的个数设置提示消息可见性 """
        count = sum(not item.isHidden() for item in self.item_list)
        self.setPromptMsgVisible(count <= 1)

    def deleteChatWidget(self, index: int):
        """ 移除指定的聊天框 """
        widget = self.chatWidget_list.pop(index)
        # 弹出IP
        IP = self.widgetIP_dict.pop(widget)
        self.IPContactName_dict.pop(IP)
        self.IPWidget_dict.pop(IP)
        # 弹出 item
        self.item_list.pop(index)
        self.removeItemWidget(self.item(index))
        self.takeItem(index)
        # 释放内存
        widget.deleteLater()
        self.__checkChatCount()
        # 发出信号
        self.deleteChatSignal.emit(IP)

    def contextMenuEvent(self, e):
        """ 右击菜单事件 """
        hitIndex = self.indexAt(e.pos()).column()
        # 显示右击菜单
        if hitIndex > -1:
            self.contextMenu.exec(self.cursor().pos())

    def __hideChatSlot(self):
        """ 隐藏消息框槽函数 """
        self.item(self.currentRow()).setHidden(True)
        self.__checkChatCount()

    def __connectSignalToSlot(self):
        """ 信号连接到槽 """
        self.deleteChatAct.triggered.connect(
            lambda: self.deleteChatWidget(self.currentRow()))
        self.hideChatAct.triggered.connect(self.__hideChatSlot)

    def findChatListWidgetByIP(self, IP: str) -> ChatWidget:
        """ 通过IP地址查找聊天框 """
        return self.IPWidget_dict[IP]
