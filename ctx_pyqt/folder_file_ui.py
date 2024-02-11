import sys

from qfluentwidgets import RoundMenu, Action, MenuAnimationType
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import LineEdit, PushButton
from PyQt5.Qt import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from project_requests import Requests_Api


class CustomMessageBox(QWidget):
    """ Custom message box """
    signal_def = pyqtSignal(tuple)

    def __init__(self, label_name):
        super().__init__()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        hlayout = QHBoxLayout()
        self.setWindowTitle("名字修改")
        self.resize(200, 130)
        self.lock_lineEdit = LineEdit(self)
        self.lock_lineEdit.setText(label_name)
        self.lock_lineEdit.setReadOnly(True)
        self.lineEdit = LineEdit(self)
        self.lineEdit.setPlaceholderText('输入内容')
        self.button = PushButton('确定', self)
        self.button.clicked.connect(self.enter_name)
        self.quit = PushButton('取消', self)
        self.quit.clicked.connect(self.quit_win)
        hlayout.addWidget(self.button)
        hlayout.addWidget(self.quit)
        main_layout.addWidget(self.lock_lineEdit)
        main_layout.addWidget(self.lineEdit)
        main_layout.addLayout(hlayout)

    def enter_name(self):
        old_text = self.lock_lineEdit.text()
        new_text = self.lineEdit.text()
        self.signal_def.emit((old_text, new_text))
        self.close()

    def quit_win(self):
        self.close()


class FolderFileUi(QPushButton):
    signal_rename_def = pyqtSignal(tuple)
    signal_del_def = pyqtSignal(str)
    def __init__(self, file_name=None, file_type=None):
        super().__init__()
        # file_type：1代表文件夹，0代表文件
        self.resize(65, 75)
        if file_name is None:
            file_name = "aa"
        if file_type is None:
            file_type = 1
        self.folds_name_label = QLabel(file_name, self)
        self.folds_image_label = QLabel(self)
        if file_type == 1:
            self.folds_name_label.move(42, 63)
            pixmap = QPixmap(r"C:\Users\Administrator\PycharmProjects\deal_tool\CTX\ctx_pyqt\icon\文件夹.png")
            self.folds_image_label.setPixmap(pixmap)
        else:
            self.folds_name_label.move(31, 65)
            pixmap = QPixmap(r"C:\Users\Administrator\PycharmProjects\deal_tool\CTX\ctx_pyqt\icon\文件.png")
            self.folds_image_label.setPixmap(pixmap)
        self.folds_image_label.setScaledContents(True)
        self.folds_image_label.setFixedSize(60, 60)
        self.folds_image_label.move(20, 5)

    def contextMenuEvent(self, evt: QContextMenuEvent) -> None:
        menu = RoundMenu(parent=self)
        rename = Action(FIF.COPY, '重命名')
        rename.triggered.connect(self.rename_fun)
        del_btn = Action(FIF.COPY, '删除')
        del_btn.triggered.connect(self.del_fun)
        menu.addAction(rename)
        menu.addAction(del_btn)
        menu.exec(evt.globalPos(), aniType=MenuAnimationType.DROP_DOWN)

    def rename_fun(self):
        # 修改ui上的文件夹名字
        # 更新数据库中的信息
        self.w = CustomMessageBox(self.folds_name_label.text())
        self.w.show()
        self.w.signal_def.connect(self.deal_emit_dir_slot)

    def deal_emit_dir_slot(self, text_tuple):
        # 重名判断,判断当前目录是否有重名
        # 更新ui，更新数据库
        # 判断是文件还是文件夹
        self.signal_rename_def.emit(text_tuple)
        # flag =1
        # if "." in self.folds_name_label.text():
        #     if text in context["files"]:
        #         flag = 0
        #         msg_box = QMessageBox(QMessageBox.Critical, '错误提示', '名字重复，请重新输入')
        #         msg_box.exec_()
        # else:
        #     if text in context["folders"]:
        #         flag = 0
        #         msg_box = QMessageBox(QMessageBox.Critical, '错误提示', '名字重复，请重新输入')
        #         msg_box.exec_()
        # if flag:
        #     # ui更新名字
        #     self.folds_name_label.setText(text)
        #     self.folds_name_label.update()
        #     # 数据库更新记录
        #     self.demo = Requests_Api()
        #     # 发送更新请求

    def del_fun(self):
        # 更新ui
        # 更新数据库中的信息
        # 删了后重新刷新UI
        # post请求，调用视图中的删除方法
        self.signal_del_def.emit(self.folds_name_label.text())
        self.folds_image_label.deleteLater()
        self.folds_name_label.deleteLater()
        self.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = FolderFileUi()
    demo.show()
    sys.exit(app.exec_())