import os
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MyItem(QListWidgetItem):
    def __init__(self, name=None, parent=None):
        super(MyItem, self).__init__()
        img = os.path.join(r"C:\Users\Administrator\PycharmProjects\deal_tool\CTX\ctx_pyqt\icon", name + ".png")
        # 自定义item中的widget 用来显示自定义的内容
        self.widget = QWidget()
        self.widget.setObjectName("itemwin")
        self.widget.setStyleSheet("#itemwin{ background-color: #FFFFFF; } #itemwin:hover{background-color : #FFDAB9;}")
        hbox = QVBoxLayout()
        self.name_label = QLabel(name, self.widget)
        # self.name_label.setStyleSheet("QLabel{ background-color: #FFEFD5; } QLabel:hover{background-color : #FFDAB9;}")
        self.name_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.image_label = QLabel(self.widget)
        self.image_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        pixmap = QPixmap(img)
        self.image_label.setPixmap(pixmap)
        hbox.addWidget(self.image_label)
        hbox.addWidget(self.name_label)
        self.widget.setLayout(hbox)
        # # 用来显示name
        # self.nameLabel = QLabel()
        # self.nameLabel.setText(name)
        # # 用来显示avator(图像)
        # self.avatorLabel = QLabel()
        # # 设置图像源 和 图像大小
        # self.avatorLabel.setPixmap(QPixmap(img).scaled(50, 50))
        # # 设置布局用来对nameLabel和avatorLabel进行布局
        # self.hbox = QHBoxLayout()
        # self.hbox.addWidget(self.avatorLabel)
        # # 设置widget的布局
        # self.widget.setLayout(self.hbox)
        # 设置自定义的QListWidgetItem的sizeHint，不然无法显示
        self.setSizeHint(QSize(100, 100))
        # self.setIcon(QIcon(img))
        # self.setSizeHint(QSize(100, 100))  # size


class NanItem(MyItem):
    def __init__(self, parent=None):
        super(NanItem, self).__init__('缺失值处理', parent=parent)


class RepeatItem(MyItem):
    def __init__(self, parent=None):
        super().__init__(
            '重复值处理', parent=parent)


class ColItem(MyItem):
    def __init__(self, parent=None):
        super().__init__(
            '列名重命名', parent=parent)



class FormatItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('格式转换',
                         parent=parent)



class IlocItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('数据筛选',
                         parent=parent)



class DatasortItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('数据排序',
                         parent=parent)



class DataoverItem(MyItem):
    def __init__(self, parent=None):
        super().__init__('异常值处理',
                         parent=parent)
