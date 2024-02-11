import os
import sys

from PyQt5.Qt import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, PushButton

from folder_file_ui import FolderFileUi
from project_requests import Requests_Api


class NewFolder(MessageBoxBase):
    """ Custom message box """
    signal_def = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('新建文件夹', self)
        self.urlLineEdit = LineEdit(self)
        self.urlLineEdit.setPlaceholderText('输入文件夹名称')
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.urlLineEdit)
        self.yesButton.setText('确定')
        self.cancelButton.setText('取消')
        self.widget.setMinimumWidth(350)
        self.yesButton.clicked.connect(self.enter_name)

    def enter_name(self):
        text = self.urlLineEdit.text()
        self.signal_def.emit(str(text))


class WebDiskUi(QWidget):
    def __init__(self, username, password):
        super().__init__()
        self.resize(600, 600)
        self.demo = Requests_Api(username, password)
        self.context = self.demo.get_folder_file(url="http://127.0.0.1:8000/netdisk/folder/root?format=json")
        # self.context = self.demo.get_folder_file(url="http://127.0.0.1:8000/netdisk/folder_all")
        # self.context = {'folders': ["root/test/aa", "root/test/bb", "root/test/aa", "root/test/bb"],
        #                 'files': ["a.txt", "a.csv"],
        #                 'path': 'root/test'}
        self.title_label = QLabel("当前目录:" + self.context["path"], self)
        self.title_label.move(240, 50)
        self.title_label.adjustSize()
        back = PushButton("返回上一级", self)
        back.clicked.connect(self.back_dir)
        new_dir = PushButton("新建文件夹", self)
        new_dir.clicked.connect(self.new_dir)
        upload_file = PushButton("上传文件", self)
        upload_file.clicked.connect(self.upload_file)
        back.move(5, 5)
        new_dir.move(110, 5)
        upload_file.move(215, 5)
        self.grid = QGridLayout()
        self.folder_show()

    def folder_show(self):
        # 清空网格布局中的所有控件
        item_list = list(range(self.grid.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序
        for i in item_list:
            item = self.grid.itemAt(i)
            self.grid.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
        file_type_flag = 1
        column = 0
        for index, item in enumerate(self.context["folders"] + self.context["files"]):
            if column == 3:
                column = 0
            item_name = item.split("/")[-1]
            if "." in item_name:
                file_type_flag = 0
            self.file_icon = FolderFileUi(item_name, file_type_flag)
            self.file_icon.signal_rename_def.connect(self.deal_emit_rename_slot)
            self.file_icon.signal_del_def.connect(self.deal_emit_del_slot)
            self.file_icon.setFixedSize(100, 80)
            self.file_icon.setStyleSheet("border-radius: 10px;")
            self.file_icon.clicked.connect(lambda checked, item=item: self.cd_dir(item))
            # self.file_icon.clicked.connect(lambda checked, item=item: self.cd_dir(item))
            rown = int(index / 3)
            self.grid.addWidget(self.file_icon, rown + 1, column)
            column += 1
            file_type_flag = 1  # 重新置为1，预防一次为0后后续都为0

        self.setLayout(self.grid)

    def cd_dir(self, button):
        tmp_dir = button
        if "." in tmp_dir:
            default_path = 'C:'
            if not os.path.exists(default_path):
                default_path = os.getcwd()
            file_path = QFileDialog.getExistingDirectory(self, '下载文件保存位置')
            url = "http://127.0.0.1:8000/netdisk/download/" + self.context["path"] + "/" + tmp_dir
            file_path = file_path + "/" + tmp_dir
            self.demo.down_file(url, file_path)
        else:
            self.context = self.demo.get_folder_file(
                url="http://127.0.0.1:8000/netdisk/folder/" + tmp_dir + "?format=json")
            self.folder_show()
            self.title_label.setText("当前目录:" + self.context["path"])
            self.title_label.update()
            self.title_label.adjustSize()

    def new_dir(self):
        # 新建之后把目录信息存到数据库，然后刷新当前目录ui
        self.w = NewFolder(self)
        self.w.show()
        self.w.signal_def.connect(self.deal_emit_dir_slot)

    def deal_emit_rename_slot(self, text_tuple):
        # 处理修改文件名信号
        print("信号", text_tuple)
        old_text, new_text = text_tuple
        # 区分文件夹或文件
        if "." in old_text:
            # 获取当前文件夹信息
            res = self.demo.get_url(
                url="http://127.0.0.1:8000/netdisk/folder/" + self.context["path"] + "?format=json")
            res = res["files"]
            name_to_id = {item['name']: item['id'] for item in res}
            name_to_size = {item['name']: item['size'] for item in res}
            name_list = {item['name'] for item in res}  # 文件名列表
            file_id = name_to_id.get(old_text)
            file_size = name_to_size.get(old_text)
            # 新文件名处理，没有后缀加上后缀
            if "." in new_text:
                pass
            else:
                new_text = new_text+"."+old_text.split(".")[-1]
            if new_text in name_list:
                msg_box = QMessageBox(QMessageBox.Critical, '错误提示', '文件名重复，请重新输入')
                msg_box.exec_()
            else:
                data = {"id": file_id, "name": new_text, "size": file_size}
                url = "http://127.0.0.1:8000/netdisk/folder/" + self.context["path"]
                self.demo.update_file_name(url, data)
                """
                刷新界面
                """
                self.context = self.demo.get_folder_file(
                    url="http://127.0.0.1:8000/netdisk/folder/" + self.context["path"] + "?format=json")
                self.folder_show()
                self.title_label.setText("当前目录:" + self.context["path"])
                self.title_label.update()
                self.title_label.adjustSize()

        else:
            # 获取当前目录的文件
            # res = self.demo.get_folder_all()  # 获取所有的文件夹和文件信息
            res = self.demo.get_url(
                url="http://127.0.0.1:8000/netdisk/folder/" + self.context["path"] + "?format=json")
            res = res["folder"]
            name_to_id = {item['name']: item['id'] for item in res}
            name_to_path = {item['name']: item['path'] for item in res}
            folder_name_list = [item['name'] for item in res]
            if new_text in folder_name_list:
                msg_box = QMessageBox(QMessageBox.Critical, '错误提示', '文件夹名重复，请重新输入')
                msg_box.exec_()
            else:
                folder_id = name_to_id.get(old_text)
                new_path = "/".join(name_to_path.get(old_text).split("/")[:-1]) + "/" + new_text  # 新路径
                data = {"id": folder_id, "name": new_text, "path": new_path}
                url = "http://127.0.0.1:8000/netdisk/folder/" + self.context["path"]
                self.demo.update_name(url, data)  # 修改文件夹名
                """
                刷新界面
                """
                self.context = self.demo.get_folder_file(
                    url="http://127.0.0.1:8000/netdisk/folder/" + self.context["path"] + "?format=json")
                self.folder_show()
                self.title_label.setText("当前目录:" + self.context["path"])
                self.title_label.update()
                self.title_label.adjustSize()

    def deal_emit_del_slot(self, text):
        #  删除文件或文件夹
        # url:当前路径拼接文件夹名字
        url = "http://127.0.0.1:8000/netdisk/folder/" + self.context["path"] + "/" + text
        print("删除url", url)
        if "." in text:
            # 一个特殊put请求
            res = self.demo.get_url(
                url="http://127.0.0.1:8000/netdisk/folder/" + self.context["path"] + "?format=json")
            res = res["files"]
            name_to_id = {item['name']: item['id'] for item in res}
            name_to_size = {item['name']: item['size'] for item in res}
            file_id = name_to_id.get(text)
            file_size = name_to_size.get(text)
            data = {"id": file_id, "name": "del_file", "size": file_size}
            url = "http://127.0.0.1:8000/netdisk/folder/" + self.context["path"]
            self.demo.delete_file(url, data)
        else:
            self.demo.delete_folder(url)

    def deal_emit_dir_slot(self, text):
        # 新建文件夹
        if self.context["path"] + "/" + text in self.context["folders"]:
            msg_box = QMessageBox(QMessageBox.Critical, '错误提示', '文件夹名重复，请重新输入')
            msg_box.exec_()
        else:
            new_dir_path = self.context["path"] + "/" + text
            self.context["folders"].append(self.context["path"] + "/" + text)
            res = self.demo.get_folder_all()
            # 创建一个新的字典，键是path属性值，值是相应的id
            path_to_id = {item['path']: item['id'] for item in res}
            path_to_owner = {item['path']: item['owner'] for item in res}
            # 要匹配的路径
            target_path = self.context["path"]
            # 使用新的字典查找匹配的id
            parent_id = path_to_id.get(target_path)
            owner = path_to_owner.get(target_path)
            self.demo.new_folder(text, new_dir_path, parent_id, owner)
            self.folder_show()

    def back_dir(self):
        # 从当前路径获取上一级路径，如果没有不操作
        # 获取上一级路径后，从数据库获取当前路径的内存，重新更新ui
        try:
            parent_path = "/".join(self.context["path"].split("/")[:-1])
            self.context = self.demo.get_folder_file(
                url="http://127.0.0.1:8000/netdisk/folder/" + parent_path + "?format=json")
            self.folder_show()
            self.title_label.setText("当前目录:" + self.context["path"])
            self.title_label.update()
            self.title_label.adjustSize()
        except:
            pass

    def upload_file(self):
        default_path = 'C:\MY'
        if not os.path.exists(default_path):
            default_path = os.getcwd()
        dlg = QFileDialog(None, "choose_file", default_path, 'All Files(*)')
        dlg.setFileMode(QFileDialog.AnyFile)
        if dlg.exec_():
            selected_name = dlg.selectedFiles()[0]
            url = "http://127.0.0.1:8000/netdisk/" + "upload/" + self.context["path"]
            self.demo.upload_file(url, selected_name)
        self.folder_show()
        self.context = self.demo.get_folder_file(
            url="http://127.0.0.1:8000/netdisk/folder/" + self.context["path"] + "?format=json")
        self.folder_show()
        self.title_label.setText("当前目录:" + self.context["path"])
        self.title_label.update()
        self.title_label.adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = WebDiskUi()
    demo.show()
    sys.exit(app.exec_())
