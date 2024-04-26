import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QLabel
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建主垂直布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # 设置布局的四个间距都为0
        self.resize(1000, 860)
        # 创建第一个QWidget，背景色为绿色，固定高度为60
        top_widget = QWidget()
        top_widget.setStyleSheet("background-color: blue;")
        top_widget.setFixedHeight(60)

        # 添加到主布局
        main_layout.addWidget(top_widget)

        # 创建第二个QWidget，用于包含win1和win2的QHBoxLayout
        second_widget = QWidget()
        second_layout = QHBoxLayout(second_widget)

        # 创建win1，固定宽度为60
        win1 = QWidget()
        win1.setFixedWidth(60)

        # 创建两个按钮
        button1 = QPushButton("界面1", win1)
        button2 = QPushButton("界面2", win1)

        # 垂直布局用于放置按钮
        button_layout = QVBoxLayout(win1)
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)

        # 将win1添加到水平布局
        second_layout.addWidget(win1)

        # 创建win2的QStackedWidget
        win2 = QStackedWidget()

        # 创建两个界面，这里用QLabel代替其他复杂界面
        label1 = QLabel("这是界面1的内容", win2)
        label2 = QLabel("这是界面2的内容", win2)

        # 将界面添加到堆叠控件
        win2.addWidget(label1)
        win2.addWidget(label2)

        # 将win2添加到水平布局
        second_layout.addWidget(win2)

        # 将第二个QWidget添加到主布局
        main_layout.addWidget(second_widget)

        # 连接按钮信号到槽函数
        button1.clicked.connect(lambda: win2.setCurrentIndex(0))
        button2.clicked.connect(lambda: win2.setCurrentIndex(1))

        # 设置窗口属性
        self.setWindowTitle('PyQt QStackedWidget 示例')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())