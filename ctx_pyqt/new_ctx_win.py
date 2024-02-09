# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout,QVBoxLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import (MSFluentWindow,
                            SubtitleLabel, setFont)

from newwin_ctx import CtxUi
from newwin_login import LoginMainWindow


# 使用网络功能需要先注册登录，用户不登录也可使用CTX网络功能之外的功能

class Widget_ctx(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        ctxui = CtxUi()
        self.hBoxLayout.addWidget(ctxui)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.setObjectName(text.replace(' ', '-'))



class Widget_web(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        webui = LoginMainWindow(parent)
        self.hBoxLayout.addWidget(webui)
        self.setObjectName(text.replace(' ', '-'))


class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)
        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()
        # create sub interface
        self.data_clean = Widget_ctx('数据清洗', self)
        self.reg_login = Widget_web('注册/登陆', self)
        self.help = Widget('帮助界面', self)
        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.data_clean, FIF.ASTERISK, '数据清洗')
        self.addSubInterface(self.reg_login, FIF.VIDEO, '注册/登陆')
        self.addSubInterface(self.help, FIF.HELP, '帮助')

    def initWindow(self):
        self.resize(1200, 800)
        # 加载图标
        pixmap = QPixmap('shoko.png')
        # 调整图标大小为 64x64（你可以根据需要修改这个尺寸）
        scaled_pixmap = pixmap.scaled(128, 128, Qt.KeepAspectRatio)
        # 使用调整后的 QPixmap 创建 QIcon
        self.setWindowIcon(QIcon(scaled_pixmap))
        # self.setWindowIcon(QIcon('shoko.png'))
        self.setWindowTitle('ADC,启动！！！')
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    # setTheme(Theme.LIGHT)
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
