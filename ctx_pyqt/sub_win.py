
# coding:utf-8
import re
import sys
from itertools import product

from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QCompleter
from qfluentwidgets import PushButton, SearchLineEdit, CheckBox, BodyLabel


class SubWin(QWidget):
    signal_def = pyqtSignal(tuple)
    signal_sub_def = pyqtSignal(tuple)
    signal_sub_all_def = pyqtSignal(tuple)

    def __init__(self, main_text=None, flag=None):
        super().__init__()
        # self.setStyleSheet("Demo {background: rgb(32, 32, 32)}")
        # setTheme(Theme.DARK)
        self.sub_index = None
        self.sub_list = None
        self.flag = flag
        self.main_text = main_text
        self.search_text = None
        self.setWindowTitle("替换")
        self.search_line_edit = SearchLineEdit(self)
        self.sub_line_edit = SearchLineEdit(self)
        self.search_button = PushButton('查找下一个', self)
        self.sub_button = PushButton('替换', self)
        self.sub_all_button = PushButton('替换全部', self)
        self.search_button.clicked.connect(self.search)
        self.sub_button.clicked.connect(self.sub_event)
        self.sub_all_button.clicked.connect(self.sub_all)
        self.check = CheckBox("区分大小写", self)
        self.re_check = CheckBox("正则表达式", self)

        self.search_content_label = BodyLabel("查找内容：", self)
        self.sub_content_label = BodyLabel("替换为：", self)
        self.count = 0

        # add completer
        stands = [
            "Star Platinum", "Hierophant Green",
            "Made in Haven", "King Crimson",
            "Silver Chariot", "Crazy diamond",
            "Metallica", "Another One Bites The Dust",
            "Heaven's Door", "Killer Queen",
            "The Grateful Dead", "Stone Free",
            "The World", "Sticky Fingers",
            "Ozone Baby", "Love Love Deluxe",
            "Hermit Purple", "Gold Experience",
            "King Nothing", "Paper Moon King",
            "Scary Monster", "Mandom",
            "20th Century Boy", "Tusk Act 4",
            "Ball Breaker", "Sex Pistols",
            "D4C • Love Train", "Born This Way",
            "SOFT & WET", "Paisley Park",
            "Wonder of U", "Walking Heart",
            "Cream Starter", "November Rain",
            "Smooth Operators", "The Matte Kudasai"
        ]
        self.completer = QCompleter(stands, self.search_line_edit)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setMaxVisibleItems(10)
        self.search_line_edit.setCompleter(self.completer)
        self.search_line_edit.setClearButtonEnabled(True)
        self.search_line_edit.setPlaceholderText('查找内容')
        self.sub_line_edit.setPlaceholderText('替换内容')
        self.resize(600, 300)
        self.search_line_edit.setFixedSize(260, 33)
        self.sub_line_edit.setFixedSize(260, 33)
        self.search_content_label.setFixedSize(60, 33)
        self.sub_content_label.setFixedSize(60, 33)
        self.search_button.setFixedSize(120, 33)
        self.sub_button.setFixedSize(120, 33)
        self.sub_all_button.setFixedSize(120, 33)
        self.search_button.move(420, 40)
        self.sub_button.move(420, 80)
        self.sub_all_button.move(420, 120)
        self.search_line_edit.move(138, 40)
        self.sub_line_edit.move(138, 90)
        self.search_content_label.move(50, 40)
        self.sub_content_label.move(50, 90)
        self.check.move(50, 150)
        self.re_check.move(50, 200)
        self.setStyleSheet("background-color: #BFEFFF;")

    def search(self):
        self.search_text = self.search_line_edit.text()
        res_list = []
        # 区分大小写
        if self.flag:  # 表格和文本分情况考虑
            pass
            if self.check.isChecked():  # 文本大小写
                res_list = [i.span() for i in re.finditer(self.search_text, self.main_text)]
            else:
                res_list = [i.span() for i in re.finditer(self.search_text, self.main_text, re.I)]
            # 是否使用正则
            if self.re_check.isChecked():
                res_list = [i.span() for i in re.finditer(self.search_text, self.main_text)]
            else:
                res_list = [i.span() for i in re.finditer(re.escape(self.search_text), self.main_text)]
            # 处理没有匹配到的情况
            try:
                self.signal_def.emit(res_list[self.count])  # 信号的触发
                self.count += 1
                if self.count == len(res_list):  # 循环
                    self.count = 0
            except:
                msg_box = QMessageBox(QMessageBox.Critical, '错误提示', '找不到' + self.search_text)
                msg_box.exec_()


        else:
            if self.check.isChecked():
                for i, j in product(range(len(self.main_text)), range(max([len(i) for i in self.main_text]))):
                    if re.search(self.search_text, str(self.main_text[i][j])):
                        res_list.append((i, j))
            else:
                for i, j in product(range(len(self.main_text)), range(max([len(i) for i in self.main_text]))):
                    if re.search(self.search_text, str(self.main_text[i][j]), re.I):
                        res_list.append((i, j))
            # 是否使用正则
            if self.re_check.isChecked():
                for i, j in product(range(len(self.main_text)), range(max([len(i) for i in self.main_text]))):
                    if re.search(self.search_text, str(self.main_text[i][j])):
                        res_list.append((i, j))
            else:
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

        self.sub_list = res_list
        self.sub_index = self.count

    def sub_event(self):
        # 获取索引，替换索引所在位置的内容
        # 替换后跳转到下一个位置
        old_text = self.search_line_edit.text()
        sub_text = self.sub_line_edit.text()
        try:
            if self.flag:
                self.signal_sub_def.emit((self.sub_list[self.count - 1], self.sub_list, self.count - 1, sub_text))
                self.count += 1
            else:
                self.signal_sub_def.emit((self.sub_list[self.count - 1], self.sub_list, self.count - 1, sub_text, old_text))
                self.count += 1
        except:
            pass

    def sub_all(self):
        sub_text = self.sub_line_edit.text()
        old_text = self.search_line_edit.text()
        if self.flag:
            try:
                self.signal_sub_all_def.emit((old_text, sub_text))
                self.count += 1
            except:
                pass
        else:
            try:
                self.signal_sub_all_def.emit((old_text, sub_text, self.sub_list))
                self.count += 1
            except:
                pass


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = SubWin()
    w.show()
    app.exec_()


