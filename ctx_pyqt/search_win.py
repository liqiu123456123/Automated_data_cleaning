# coding:utf-8
import re
from qfluentwidgets import PushButton, CheckBox, LineEdit
from PyQt5.QtWidgets import QWidget, QMessageBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
from itertools import product


class SearchWin(QWidget):
    signal_def = pyqtSignal(tuple)

    def __init__(self, main_text=None):
        super().__init__()
        self.main_text = main_text
        self.search_text = None
        self.count = 0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("查找")
        self.resize(450, 170)

        main_layout = QVBoxLayout(self)  # 设置布局

        # 创建第一行水平布局
        h_layout_one = QHBoxLayout()
        self.lineEdit = LineEdit(self)
        self.lineEdit.setPlaceholderText('查找内容')
        self.lineEdit.setFixedSize(260, 33)  # 设置文本输入框的大小
        self.button = PushButton('查找下一个', self)
        self.button.clicked.connect(self.search)  # 连接按钮点击事件到search方法
        h_layout_one.addWidget(self.lineEdit)
        h_layout_one.addWidget(self.button)
        main_layout.addLayout(h_layout_one)

        # 创建第二行水平布局
        h_layout_two = QHBoxLayout()
        self.check = CheckBox("区分大小写", self)
        self.re_check = CheckBox("正则表达式", self)
        h_layout_two.addWidget(self.check)
        h_layout_two.addWidget(self.re_check)
        main_layout.addLayout(h_layout_two)

    def search(self):
        self.search_text = self.lineEdit.text()
        res_list = []
        # 区分大小写
        # 表格
        if self.check.isChecked():
            # 区分大小写选项
            for i, j in product(range(len(self.main_text)), range(max([len(i) for i in self.main_text]))):
                if re.search(self.search_text, str(self.main_text[i][j])):
                    res_list.append((i, j))
        else:
            # 不区分大小写
            for i, j in product(range(len(self.main_text)), range(max([len(i) for i in self.main_text]))):
                if re.search(self.search_text, str(self.main_text[i][j]), re.I):
                    res_list.append((i, j))
        if self.re_check.isChecked():
            # 使用正则
            for i, j in product(range(len(self.main_text)), range(max([len(i) for i in self.main_text]))):
                if re.search(self.search_text, str(self.main_text[i][j])):
                    res_list.append((i, j))
        else:
            # 不使用正则
            for i, j in product(range(len(self.main_text)), range(max([len(i) for i in self.main_text]))):
                if re.search(re.escape(self.search_text), str(self.main_text[i][j])):
                    res_list.append((i, j))
        # 处理没有匹配到的情况
        try:
            self.signal_def.emit(res_list[self.count])  # 信号的触发
            self.count += 1
            if self.count == len(res_list):  # 循环
                self.count = 0

        except:
            msg_box = QMessageBox(QMessageBox.Critical, '错误提示', '找不到' + self.search_text)
            msg_box.exec_()


