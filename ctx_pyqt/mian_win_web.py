import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from web_disk_ui import WebDiskUi


class WebUi(QWidget):
    def __init__(self, username, password):
        super(WebUi, self).__init__()
        self.username = username
        self.password = password
        self.initUI()

    def initUI(self):
        # 设置全局布局为水平布局，设置标题与初始大小窗口
        hbox = QHBoxLayout()
        self.web = WebDiskUi(self.username, self.password)
        hbox.addWidget(self.web)
        self.setLayout(hbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = WebUi()
    demo.show()
    sys.exit(app.exec_())
