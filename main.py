# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

from my_main_window import WireSharp

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
font = QFont('Microsoft YaHei')
font.setStyleStrategy(QFont.PreferAntialias)
app.setFont(font)

# 创建窗口
demo = WireSharp()
demo.show()

# 开始主循环
sys.exit(app.exec_())
