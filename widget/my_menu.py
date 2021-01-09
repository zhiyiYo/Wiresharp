# coding:utf-8

from effects.window_effect import WindowEffect
from PyQt5.QtCore import (QAbstractAnimation, QEasingCurve, QEvent,
                          QPropertyAnimation, QRect, Qt)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QMenu, QTextEdit, QLineEdit


class TextEditMenu(QMenu):
    """ 输入框右击菜单 """

    def __init__(self, parent):
        super().__init__('', parent)
        # 不能直接改width
        self.animation = QPropertyAnimation(self, b'geometry')
        self.initWidget()

    def initWidget(self):
        """ 初始化小部件 """
        self.setObjectName('textEditMenu')
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        WindowEffect.setShadowEffect(self.winId())
        self.__setQss()

    def createActions(self):
        # 创建动作
        self.cutAct = QAction(
            QIcon('resource\\Image\\text_edit_menu\\黑色剪刀.png'), '剪切', self, shortcut='Ctrl+X', triggered=self.parent().cut)
        self.copyAct = QAction(
            QIcon('resource\\Image\\text_edit_menu\\黑色复制.png'), '复制', self, shortcut='Ctrl+C', triggered=self.parent().copy)
        self.pasteAct = QAction(
            QIcon('resource\\Image\\text_edit_menu\\黑色粘贴.png'), '粘贴', self, shortcut='Ctrl+V', triggered=self.parent().paste)
        self.cancelAct = QAction(
            QIcon('resource\\Image\\text_edit_menu\\黑色撤销.png'), '取消操作', self, shortcut='Ctrl+Z', triggered=self.parent().undo)
        self.selectAllAct = QAction(
            '全选', self, shortcut='Ctrl+A', triggered=self.parent().selectAll)
        # 创建动作列表
        self.action_list = [self.cutAct, self.copyAct,
                            self.pasteAct, self.cancelAct, self.selectAllAct]

    def exec_(self, pos):
        # 删除所有动作
        self.clear()
        # clear之后之前的动作已不再存在故需重新创建
        self.createActions()
        # 初始化属性
        self.setProperty('hasCancelAct', 'false')
        width = 176
        actionNum = len(self.action_list)
        # 访问系统剪贴板
        self.clipboard = QApplication.clipboard()
        # 根据剪贴板内容是否为text分两种情况讨论
        text = self.parent().text() if isinstance(
            self, QLineEdit) else self.parent().toPlainText()
        selectedText = self.parent().selectedText() if isinstance(
                    self, QLineEdit) else self.parent().textCursor().selectedText()
        if self.clipboard.mimeData().hasText():
            # 再根据3种情况分类讨论
            if text:
                self.setProperty('hasCancelAct', 'true')
                width = 213
                if selectedText:
                    self.addActions(self.action_list)
                else:
                    self.addActions(self.action_list[2:])
                    actionNum -= 2
            else:
                self.addAction(self.pasteAct)
                actionNum = 1
        else:
            if text:
                self.setProperty('hasCancelAct', 'true')
                width = 213
                if selectedText:
                    self.addActions(
                        self.action_list[:2] + self.action_list[3:])
                    actionNum -= 1
                else:
                    self.addActions(self.action_list[3:])
                    actionNum -= 3
            else:
                return
        # 每个item的高度为38px，10为上下的内边距和
        height = actionNum * 38 + 10
        # 不能把初始的宽度设置为0px，不然会报警
        self.animation.setStartValue(
            QRect(pos.x(), pos.y(), 1, height))
        self.animation.setEndValue(
            QRect(pos.x(), pos.y(), width, height))
        self.setStyle(QApplication.style())
        # 开始动画
        self.animation.start()
        super().exec_(pos)

    def __setQss(self):
        """ 设置层叠样式 """

    def __setQss(self):
        """ 设置层叠样式 """
        with open('resource\\qss\\text_edit_menu.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
