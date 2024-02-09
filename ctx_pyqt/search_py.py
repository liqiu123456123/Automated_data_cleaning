
# coding:utf-8
import sys
import re
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QCompleter, QPushButton

from qfluentwidgets import LineEdit, PushButton, SearchLineEdit, setTheme, Theme, CheckBox
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from itertools import product


class SearchWin(QWidget):
    signal_def = pyqtSignal(tuple)

    def __init__(self, main_text=None, flag=None):
        super().__init__()
        # self.setStyleSheet("Demo {background: rgb(32, 32, 32)}")
        # setTheme(Theme.DARK)
        self.main_text = main_text
        self.search_text = None
        self.flag = flag
        self.setWindowTitle("查找")
        self.lineEdit = SearchLineEdit(self)
        self.button = PushButton('查找下一个', self)
        self.button.clicked.connect(self.search)
        self.check = CheckBox("区分大小写", self)
        self.re_check = CheckBox("正则表达式", self)
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
        self.completer = QCompleter(stands, self.lineEdit)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setMaxVisibleItems(10)
        self.lineEdit.setCompleter(self.completer)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setPlaceholderText('查找内容')
        self.resize(450, 170)
        self.lineEdit.setFixedSize(260, 33)
        self.button.setFixedSize(120, 33)
        self.button.move(320, 40)
        self.lineEdit.move(38, 40)
        self.check.move(40, 100)
        self.re_check.move(300, 100)
        self.setStyleSheet("background-color: #BFEFFF;")

    def search(self):
        self.search_text = self.lineEdit.text()
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
                    print("区分大小写", res_list)
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


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = SearchWin()
    w.show()
    app.exec_()


