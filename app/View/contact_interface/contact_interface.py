# coding:utf-8
from typing import List, Dict

import pinyin
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QVBoxLayout

from app.components.widgets.my_scroll_area import ScrollArea
from app.components.widgets.my_button import ThreeStateToolButton
from .contact_list_widget import ContactListWidget
from .contact_widget import ContactWidget


class ContactInterface(ScrollArea):
    """ 联系人界面 """

    selectContactSignal = pyqtSignal(dict)

    def __init__(self, contactInfo_list: List[Dict[str, str]], parent=None):
        """ 初始化联系人界面 """
        super().__init__(parent=parent)
        self.contactInfo_list = contactInfo_list
        self.item_list = []
        self.contactWidget_list = []
        self.contactWidgetDict_list = []
        # 实例化小部件
        iconPath = {
            'normal': r'app\resource\Image\navigation_interface\联系人按钮_normal.png',
            'hover': r'app\resource\Image\navigation_interface\联系人按钮_normal.png',
            'pressed': r'app\resource\Image\navigation_interface\联系人按钮_pressed.png',
        }
        self.searchLabel = QLabel(self)
        self.scrollWidget = QWidget(self)
        self.showMenuArrow = QLabel(self)
        self.backgroundLabel = QLabel(self)
        self.showMenuLabel = QLabel('我的联系人', self)
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self.startChatInSkypeLabel = QLabel('开始在 Wiresharp 上聊天', self)
        self.contactButton = ThreeStateToolButton(iconPath, (104, 38), self)
        self.useSearchLabel = QLabel('使用"搜索"在 Wiresharp 上查找任何人。', self)
        # 创建联系人分组
        self.__createContactWidget()
        self.__createContactGroup()
        # 初始化界面
        self.__initWidget()

    def __initWidget(self):
        """ 初始化界面 """
        self.resize(402, 680)
        self.setFixedWidth(402)
        self.setWidget(self.scrollWidget)
        self.searchLabel.setPixmap(
            QPixmap(r'app\resource\Image\navigation_interface\查找.png'))
        self.backgroundLabel.setPixmap(
            QPixmap(QPixmap(r'app\resource\Image\navigation_interface\开始在Skype上聊天.png')))
        self.showMenuArrow.setPixmap(
            QPixmap(r'app\resource\Image\navigation_interface\排序聊天下拉菜单箭头.png'))
        # 移动小部件
        self.showMenuLabel.move(11, 18)
        self.showMenuArrow.move(93, 28)
        self.contactButton.move(285, 8)
        self.searchLabel.move(18, 329+55)
        self.useSearchLabel.move(46, 326+55)
        self.backgroundLabel.move(121, 117+55)
        self.startChatInSkypeLabel.move(48, 284+55)
        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setContentsMargins(0, 55, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        # 设置层叠样式
        self.startChatInSkypeLabel.setObjectName('startChatInSkypeLabel')
        self.showMenuLabel.setObjectName('showMenuLabel')
        self.useSearchLabel.setObjectName('useSearchLabel')
        self.setAttribute(Qt.WA_StyledBackground)
        self.__setQss()
        self.setPromptMsgVisible(not bool(self.contactInfo_list))

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'app\resource\qss\contact_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def __createContactWidget(self):
        """ 创建联系人小部件 """
        for contactInfo in self.contactInfo_list:
            contactWidget = ContactWidget(contactInfo, self)
            self.contactWidget_list.append(contactWidget)
            # 将联系人小部件及其首字母组成字典添加到列表中
            self.contactWidgetDict_list.append({
                'contactWidget': contactWidget,
                'firstLetter': pinyin.get_initial(contactInfo['contactName'])[0].upper()
            })

    def __createContactGroup(self):
        """ 创建联系人分组 """
        firstLetter_list = []
        self.groupBoxDict_list = []
        # 根据首字母创建分组和列表控件
        for contactWidget_dict in self.contactWidgetDict_list:
            firstLetter = contactWidget_dict['firstLetter']
            contactWidget = contactWidget_dict['contactWidget']
            # 如果首字母属于不在列表中就将创建分组
            if firstLetter not in firstLetter_list:
                firstLetter_list.append(firstLetter)
                group = QGroupBox(firstLetter, self.scrollWidget)
                vBoxLayout = QVBoxLayout(group)
                contactListWidget = ContactListWidget(group)
                vBoxLayout.addWidget(contactListWidget)
                vBoxLayout.setContentsMargins(0, 0, 0, 0)
                self.groupBoxDict_list.append({
                    'groupBox': group,
                    'contactWidget_list': [],
                    'vBoxLayout': QVBoxLayout,
                    'firstLetter': firstLetter,
                    'contactListWidget': contactListWidget
                })
                contactListWidget.selectContactSignal.connect(
                    self.__emitselectContactSignal)
            # 将联系人小部件添加到分组的列表控件控件中
            index = firstLetter_list.index(firstLetter)
            self.groupBoxDict_list[index]['contactWidget_list'].append(
                contactWidget)
            self.groupBoxDict_list[index]['contactListWidget'].addContactWidget(
                contactWidget)
        # 排序列表
        self.groupBoxDict_list.sort(key=lambda item: item['firstLetter'])
        # 将分组框添加到界面中
        h = 0
        for groupBox_dict in self.groupBoxDict_list:
            # 调整分组框尺寸
            deltaH = len(groupBox_dict['contactWidget_list']) * 75 + 23
            groupBox_dict['groupBox'].setFixedSize(402, deltaH)
            self.vBoxLayout.addWidget(
                groupBox_dict['groupBox'], 0, Qt.AlignTop)
            h += deltaH
        self.scrollWidget.resize(
            402, 55 + 30 * len(self.groupBoxDict_list) + h)

    def resizeEvent(self, e):
        """ 调整窗口大小 """
        self.scrollWidget.resize(self.width(), self.scrollWidget.height())

    def setPromptMsgVisible(self, isVisible: bool):
        """ 设置提示消息的可见性 """
        self.searchLabel.setVisible(isVisible)
        self.useSearchLabel.setVisible(isVisible)
        self.backgroundLabel.setVisible(isVisible)
        self.startChatInSkypeLabel.setVisible(isVisible)

    def __emitselectContactSignal(self, contactInfo: dict):
        """ 发送选中联系人的消息 """
        sender = self.sender()  # type:ContactListWidget
        # 清除其他列表的选中状态
        for groupBox_dict in self.groupBoxDict_list:
            contactListWidget = groupBox_dict['contactListWidget']
            if not (contactListWidget is sender):
                contactListWidget.clearSelection()
        # 发送信号
        self.selectContactSignal.emit(contactInfo)
