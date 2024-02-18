import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from data_cleaning_win import Menu


class CtxUi(QWidget):
    def __init__(self):
        super(CtxUi, self).__init__()
        self.initUI()

    def initUI(self):
        # 设置全局布局为水平布局，设置标题与初始大小窗口
        hbox = QHBoxLayout()
        self.menu = Menu()
        self.setWindowTitle("CTX")
        self.setGeometry(100, 70, 1200, 900)
        hbox.addWidget(self.menu)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setLayout(hbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = CtxUi()
    demo.show()
    sys.exit(app.exec_())
