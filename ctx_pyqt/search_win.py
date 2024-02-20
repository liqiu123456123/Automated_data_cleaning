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
        self.setWindowTitle("查找")
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        h_layout_one = QHBoxLayout()
        h_layout_two = QHBoxLayout()
        self.lineEdit = LineEdit(self)
        self.button = PushButton('查找下一个', self)
        self.button.clicked.connect(self.search)
        h_layout_one.addWidget(self.lineEdit)
        h_layout_one.addWidget(self.button)
        main_layout.addLayout(h_layout_one)
        self.check = CheckBox("区分大小写", self)
        self.re_check = CheckBox("正则表达式", self)
        h_layout_two.addWidget(self.check)
        h_layout_two.addWidget(self.re_check)
        main_layout.addLayout(h_layout_two)
        self.count = 0
        self.lineEdit.setPlaceholderText('查找内容')
        self.resize(450, 170)
        self.lineEdit.setFixedSize(260, 33)

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


