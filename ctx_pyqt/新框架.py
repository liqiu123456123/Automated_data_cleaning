import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QLabel, \
    QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
from mian_win_data_cleaning_win import CtxUi
from mian_win_login import LoginMainWindow
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
        top_widget.setStyleSheet("background-color:#000000;")
        top_widget.setFixedHeight(60)
        # 创建一个横向布局
        h_layout = QHBoxLayout()

        # 创建图片标签并添加到横向布局
        image_label = QLabel()
        # 假设你有一个图片路径
        # 加载图片并调整其大小为64x64
        pixmap = QPixmap('img.png')
        scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        h_layout.addWidget(image_label)
        h_layout.setSpacing(20)
        # 创建文本标签并添加到横向布局
        text_label = QLabel("欢迎使用ADC！")
        text_label.setStyleSheet("QLabel { color: white; }")
        h_layout.addWidget(text_label)

        # 创建一个压缩空间控件并添加到横向布局
        # 使用QSizePolicy.Expanding作为策略可以使空间尽可能地被压缩
        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout.addItem(spacer_item)

        # 将横向布局设置为top_widget的布局
        top_widget.setLayout(h_layout)
        # 添加到主布局
        main_layout.addWidget(top_widget)

        # 创建第二个QWidget，用于包含win1和win2的QHBoxLayout
        second_widget = QWidget()
        second_layout = QHBoxLayout(second_widget)

        # 创建win1，固定宽度为60
        win1 = QWidget()
        win1.setFixedWidth(90)
        win1.setStyleSheet("background-color: #000000;")
        # 创建两个按钮
        button1 = QPushButton("ADC", win1)
        button2 = QPushButton("登陆", win1)
        # 设置字体样式
        font = QFont('微软雅黑', 12, QFont.Bold)  # 字体名称、大小、加粗
        button1.setFont(font)
        button2.setFont(font)
        text_label.setFont(font)
        button1.setStyleSheet("QPushButton { color: white; }")
        button2.setStyleSheet("QPushButton { color: white; }")
        spacer_item2 = QSpacerItem(40, 20, QSizePolicy.Minimum,QSizePolicy.Expanding)
        # 垂直布局用于放置按钮
        button_layout = QVBoxLayout(win1)
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.addItem(spacer_item2)
        button_layout.setSpacing(20)
        # 将win1添加到水平布局
        second_layout.addWidget(win1)

        # 创建win2的QStackedWidget
        win2 = QStackedWidget()
        win2.setStyleSheet("background-color: #ffffff;")
        # 创建两个界面，这里用QLabel代替其他复杂界面
        self.ctx_ui = CtxUi()
        self.login_res = LoginMainWindow()

        # 将界面添加到堆叠控件
        win2.addWidget(self.ctx_ui)
        win2.addWidget(self.login_res)

        # 将win2添加到水平布局
        second_layout.addWidget(win2)

        # 将第二个QWidget添加到主布局
        main_layout.addWidget(second_widget)

        # 连接按钮信号到槽函数
        button1.clicked.connect(lambda: win2.setCurrentIndex(0))
        button2.clicked.connect(lambda: win2.setCurrentIndex(1))
        main_layout.setSpacing(0)
        second_layout.setSpacing(0)
        second_layout.setContentsMargins(0, 0, 0, 0)
        # 设置窗口属性
        self.setWindowTitle('导航框架')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
