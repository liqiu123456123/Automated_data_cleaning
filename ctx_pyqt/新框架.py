import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QStackedWidget, QLabel, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from mian_win_data_cleaning_win import CtxUi
from mian_win_login import LoginMainWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setup_main_layout()
        self.setup_top_widget()
        self.setup_content_widget()
        self.setup_window_properties()

    def setup_main_layout(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.resize(1000, 860)

    def setup_top_widget(self):
        top_widget = self.create_top_widget()
        self.main_layout.addWidget(top_widget)

    def create_top_widget(self):
        top_widget = QWidget()
        top_widget.setStyleSheet("background-color:#007BFF;")
        top_widget.setFixedHeight(60)

        h_layout = QHBoxLayout()
        h_layout.setSpacing(20)

        image_label = self.create_image_label('img.png', 64)
        h_layout.addWidget(image_label)

        text_label = QLabel("欢迎使用ADC！")
        text_label.setStyleSheet("QLabel { color: white; }")
        text_label.setFont(QFont('微软雅黑', 12, QFont.Bold))
        h_layout.addWidget(text_label)

        spacer_item = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        h_layout.addItem(spacer_item)

        top_widget.setLayout(h_layout)
        return top_widget

    def create_image_label(self, image_path, size):
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        return image_label

    def setup_content_widget(self):
        second_widget = QWidget()
        second_layout = QHBoxLayout(second_widget)
        second_layout.setSpacing(0)
        second_layout.setContentsMargins(0, 0, 0, 0)

        nav_widget = self.create_nav_widget()
        second_layout.addWidget(nav_widget)

        self.stacked_widget = self.create_stacked_widget()
        second_layout.addWidget(self.stacked_widget)

        self.main_layout.addWidget(second_widget)

    def create_nav_widget(self):
        nav_widget = QWidget()
        nav_widget.setFixedWidth(90)
        nav_widget.setStyleSheet("background-color: #007BFF;")

        button1 = self.create_nav_button("ADC")
        button2 = self.create_nav_button("登陆")

        button_layout = QVBoxLayout(nav_widget)
        button_layout.addWidget(button1)
        button_layout.addWidget(button2)
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        button_layout.setSpacing(20)

        button1.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        button2.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        return nav_widget

    def create_nav_button(self, text):
        button = QPushButton(text)
        button.setFont(QFont('微软雅黑', 12, QFont.Bold))
        button.setStyleSheet("QPushButton { color: white; }")
        return button

    def create_stacked_widget(self):
        stacked_widget = QStackedWidget()
        stacked_widget.setStyleSheet("background-color: #ffffff;")

        self.ctx_ui = CtxUi()
        self.login_res = LoginMainWindow()

        stacked_widget.addWidget(self.ctx_ui)
        stacked_widget.addWidget(self.login_res)

        return stacked_widget

    def setup_window_properties(self):
        self.setWindowTitle('ADC')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
