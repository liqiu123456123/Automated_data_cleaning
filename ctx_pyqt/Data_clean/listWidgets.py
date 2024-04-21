from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Data_clean.configs import items, tables
from qfluentwidgets import PushButton


class MyListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainwindow = parent
        self.setDragEnabled(True)
        # 选中不显示虚线
        # self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)


class UsedListWidget(MyListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.setAcceptDrops(True)
        self.setFlow(QListView.TopToBottom)  # 设置列表方向
        self.setDefaultDropAction(Qt.MoveAction)  # 设置拖放为移动而不是复制一个
        self.setDragDropMode(QAbstractItemView.InternalMove)  # 设置拖放模式, 内部拖放
        self.itemClicked.connect(self.show_attr)
        self.setMinimumWidth(200)
        self.move_item = None

    def contextMenuEvent(self, e):
        # 右键菜单事件
        item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
        if not item: return  # 判断是否是空白区域
        menu = QMenu()
        delete_action = QAction('删除', self)
        delete_action.triggered.connect(lambda: self.delete_item(item))  # 传递额外值
        menu.addAction(delete_action)
        menu.exec(QCursor.pos())

    def delete_item(self, item):
        # 删除操作
        self.takeItem(self.row(item))
        self.mainwindow.update_image()  # 更新frame
        self.mainwindow.dock_attr.close()

    def dropEvent(self, event):
        super().dropEvent(event)
        self.mainwindow.update_image()

    def show_attr(self):
        # 控件进入,显示选项窗口
        for table in tables:
            self.mainwindow.stackedWidget.addWidget(table(parent=self.parent))
        item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
        if not item: return
        # param = item.get_params()  # 获取当前item的属性
        # print("param", param)
        if type(item) in items:
            index = items.index(type(item))  # 获取item对应的table索引
            self.mainwindow.stackedWidget.setCurrentIndex(index)
            # self.mainwindow.stackedWidget.addWidget(tables[index](parent=self.parent))
            # self.mainwindow.stackedWidget.currentWidget().update_params(param)  # 更新对应的table
            self.mainwindow.dock_attr.show()


class FuncListWidget1(MyListWidget):
    def __init__(self, itemlist, parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet("QWidget{margin:0px; padding:0px;}")
        self.setFixedHeight(106)
        self.setSpacing(5)
        # self.setFixedWidth(100)
        self.itemlist = itemlist
        self.setFlow(QListView.TopToBottom)  # 设置列表方向
        self.setViewMode(QListView.IconMode)  # 设置列表模式
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 关掉滑动条
        self.setAcceptDrops(False)
        for itemType in self.itemlist:
            item1 = itemType()
            self.addItem(item1)
            self.setItemWidget(item1, item1.widget)
        self.itemClicked.connect(self.add_used_function)

    def add_used_function(self):
        # 加入到已选操作
        func_item = self.currentItem()
        if type(func_item) in self.itemlist:
            use_item = type(func_item)()
            self.mainwindow.useListWidget.use_list.addItem(use_item)
            self.mainwindow.useListWidget.use_list.setItemWidget(use_item, use_item.widget)
            self.mainwindow.update_image()

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.setCurrentRow(-1)  # 取消选中状态


class ImageLabel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        grid = QVBoxLayout()
        self.clean_list = FuncListWidget1(items, parent)
        grid.addWidget(self.clean_list)
        grid.setContentsMargins(0, 0, 0, 0)
        self.setObjectName("数据清洗")
        self.setLayout(grid)


class Usebutton(QWidget):
    signal_ctx_satrt = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        grid = QGridLayout()
        self.parent = parent
        self.use_list = UsedListWidget(parent)
        self.button = PushButton("ADC,启动！", self)
        self.button.clicked.connect(self.ctx_start)
        # self.button.setStyleSheet("background-color: #BFEFFF;")
        grid.addWidget(self.use_list, 0, 0)
        grid.addWidget(self.button, 1, 0)
        grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(grid)

    def ctx_start(self):
        print("启动！")
        summary_params = {}
        # 获取listwidget中条目数
        count = len(tables)
        # stackedWidget.widget(i)索引为写入时的顺序
        for i in range(count):
            widget = self.parent.stackedWidget.widget(i)
            summary_params[widget.__class__.__name__] = widget.get_params1()
        self.signal_ctx_satrt.emit(summary_params)