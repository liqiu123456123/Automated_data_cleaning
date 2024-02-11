from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Data_clean.ComboCheckBox import ComboCheckBox
# from new_table_main_win import Menu
import global_var
import copy


class TabItem(QTableWidget):
    def __init__(self, parent=None):
        super(TabItem, self).__init__(parent=parent)
        self.mainwindow = parent
        self.setShowGrid(True)  # 显示网格
        self.setAlternatingRowColors(True)  # 隔行显示颜色
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().sectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().sectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setStretchLastSection(True)
        self.setFocusPolicy(Qt.NoFocus)
        # self.m = Menu()
        # self.m.signal_main_to_usebutton(self.deal_signal_main_to_usebutton)

    # def signal_connect(self):
    #     for spinbox in self.findChildren(QSpinBox):
    #         spinbox.valueChanged.connect(self.update_item)
    #     for doublespinbox in self.findChildren(QDoubleSpinBox):
    #         doublespinbox.valueChanged.connect(self.update_item)
    #     for combox in self.findChildren(QComboBox):
    #         combox.currentIndexChanged.connect(self.update_item)
    #     for checkbox in self.findChildren(QCheckBox):
    #         checkbox.stateChanged.connect(self.update_item)
    # def deal_signal_main_to_usebutton(self, col_list):
    #     pass
    #     print("信号接收成功",col_list)
    def update_item(self):
        param = self.get_params()
        self.mainwindow.useListWidget.use_list.currentItem().update_params(param)
        # self.mainwindow.update_image()

    def update_params(self, param=None):
        for key in param.keys():
            box = self.findChild(QWidget, name=key)
            if isinstance(box, QSpinBox) or isinstance(box, QDoubleSpinBox):
                box.setValue(param[key])
            elif isinstance(box, QComboBox):
                box.setCurrentIndex(param[key])
            elif isinstance(box, QCheckBox):
                box.setChecked(param[key])

    def get_params1(self):
        param = {}
        for spinbox in self.findChildren(QLineEdit):
            param[spinbox.objectName()] = spinbox.text()
        for spinbox in self.findChildren(QTextEdit):
            param[spinbox.objectName()] = spinbox.toPlainText()
        for doublespinbox in self.findChildren(QDoubleSpinBox):
            param[doublespinbox.objectName()] = doublespinbox.value()
        for combox in self.findChildren(QComboBox):
            param[combox.objectName()] = combox.currentText()
        for combox in self.findChildren(QCheckBox):
            param[combox.objectName()] = combox.isChecked()
        return param


class NanTableWidget(TabItem):
    def __init__(self, parent=None):
        # 缺失数量放在编辑界面显示上
        super(NanTableWidget, self).__init__(parent=parent)
        self.setColumnCount(2)
        self.setRowCount(6)
        self.setHorizontalHeaderLabels(['选项', '值'])
        item_list = ['删除缺失值', '删除空值所在的行', '删除空值所在的列', '填充缺失值', '填充为指定值', '填充为其他']
        for index, item in enumerate(item_list):
            newItem = QTableWidgetItem(item)
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setItem(index, 0, newItem)
        self.setSpan(0, 0, 1, 2)
        self.setSpan(3, 0, 1, 2)
        self.line_edit = QLineEdit(self)
        self.line_edit.setObjectName('填充为指定值')
        self.setCellWidget(4, 1, self.line_edit)
        self.kind_comBox = QComboBox()
        self.kind_comBox.setObjectName('删除空值所在的行')
        self.kind_comBox.addItems(['否', '是'])
        self.setCellWidget(1, 1, self.kind_comBox)
        self.kind_comBox2 = QComboBox()
        self.kind_comBox2.setObjectName('删除空值所在的列')
        self.kind_comBox2.addItems(['否', '是'])
        self.setCellWidget(2, 1, self.kind_comBox2)
        self.kind_comBox3 = QComboBox()
        self.kind_comBox3.setObjectName('填充为其他')
        self.kind_comBox3.addItems(["否", "前一个观测值", "后一个观测值", "平均值", "中位数", "众数"])
        self.setCellWidget(5, 1, self.kind_comBox3)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.signal_connect()


class RepeatTabledWidget(TabItem):
    def __init__(self, parent=None):
        super(RepeatTabledWidget, self).__init__(parent=parent)
        col_name = global_var.get_value("col_name")
        new_col_name = [item + "重复" for item in col_name]
        new_col_name.insert(0, "所有列重复")
        new_col_name.insert(0, "否")
        self.setColumnCount(2)
        self.setRowCount(3)
        self.setHorizontalHeaderLabels(['选项', '值'])
        item_list = ['删除重复数据', '删除重复行（选择参考列）', '删除重复列']
        for index, item in enumerate(item_list):
            newItem = QTableWidgetItem(item)
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setItem(index, 0, newItem)
        self.setSpan(0, 0, 1, 2)
        self.kind_comBox = QComboBox()
        self.kind_comBox.setObjectName('删除重复行')
        self.kind_comBox.addItems(new_col_name)
        self.setCellWidget(1, 1, self.kind_comBox)
        self.kind_comBox2 = QComboBox()
        self.kind_comBox2.setObjectName('删除重复列')
        self.kind_comBox2.addItems(['否', '是'])
        self.setCellWidget(2, 1, self.kind_comBox2)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.signal_connect()


class ColTabledWidget(TabItem):
    def __init__(self, parent=None):
        super(ColTabledWidget, self).__init__(parent=parent)
        self.setColumnCount(2)
        self.setRowCount(2)
        self.setHorizontalHeaderLabels(['选项', '值'])
        item_list = ['列名重命名', '输入所有\n字段的新列名，英文逗号隔开']
        for index, item in enumerate(item_list):
            newItem = QTableWidgetItem(item)
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setItem(index, 0, newItem)
        self.setSpan(0, 0, 1, 2)
        self.kind_comBox = QTextEdit()
        self.kind_comBox.setObjectName('列名重命名')
        self.setCellWidget(1, 1, self.kind_comBox)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resizeRowToContents(1)
        # self.signal_connect()


class FormatTabledWidget(TabItem):
    def __init__(self, parent=None):
        super(FormatTabledWidget, self).__init__(parent=parent)
        col_name = global_var.get_value("col_name")
        col_list = copy.deepcopy(col_name)
        col_count = len(col_list)  # 文件中的字段数量
        self.setColumnCount(2)
        self.setRowCount(col_count + 1)
        self.setHorizontalHeaderLabels(['选项', '值'])
        col_list.insert(0, "格式转换")
        for index, item in enumerate(col_list):
            self.kind_comBox = QComboBox()
            self.kind_comBox.setObjectName(col_list[index])
            self.kind_comBox.addItems(['不修改', '整数类型', '小数类型', '日期时间', '文本'])
            newItem = QTableWidgetItem(item)
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setItem(index, 0, newItem)
            if index > 0:
                self.setCellWidget(index, 1, self.kind_comBox)
        self.setSpan(0, 0, 1, 2)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.signal_connect()


class IlocTableWidget(TabItem):
    def __init__(self, parent=None):
        super(IlocTableWidget, self).__init__(parent=parent)
        col_name = global_var.get_value("col_name")
        col_list = copy.deepcopy(col_name)
        self.setColumnCount(2)
        self.setRowCount(8)
        self.setHorizontalHeaderLabels(['选项', '值'])
        for index, item in enumerate(("数据筛选", "数值范围筛选", "选择字段", "文本包含筛选", "选择字段")):
            newItem = QTableWidgetItem(item)
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            if item == "选择字段":
                pass
            else:
                if index >= 3:
                    self.setItem(index + 2, 0, newItem)
                else:
                    self.setItem(index, 0, newItem)
        self.col_win = QWidget()
        layout = QVBoxLayout()
        col_label1 = QLabel("选择字段", self.col_win)
        layout.addWidget(col_label1)
        combobox1 = ComboCheckBox(col_list)
        combobox1.setObjectName("数值范围选择字段")
        layout.addWidget(combobox1)
        self.col_win.setLayout(layout)
        self.setCellWidget(2, 0, self.col_win)
        self.setSpan(2, 0, 3, 1)
        # 大于
        self.col_win = QWidget()
        layout = QHBoxLayout()
        col_label1 = QLabel("大于:", self.col_win)
        layout.addWidget(col_label1)
        combobox2 = QLineEdit()
        combobox2.setObjectName("大于")
        combobox2.setFixedSize(60, 18)
        layout.addWidget(combobox2)
        self.col_win.setLayout(layout)
        self.setCellWidget(2, 1, self.col_win)
        self.setRowHeight(2, 40)
        # 介于
        self.col_win = QWidget()
        layout = QHBoxLayout()
        combobox3 = QLineEdit()
        combobox3.setObjectName("介于下限")
        combobox3.setFixedSize(60, 18)
        layout.addWidget(combobox3)
        col_label1 = QLabel("介于:", self.col_win)
        layout.addWidget(col_label1)
        combobox4 = QLineEdit()
        combobox4.setObjectName("介于上限")
        combobox4.setFixedSize(60, 18)
        layout.addWidget(combobox4)
        self.col_win.setLayout(layout)
        self.setCellWidget(3, 1, self.col_win)
        self.setRowHeight(3, 40)
        # 小于
        self.col_win = QWidget()
        layout = QHBoxLayout()
        col_label1 = QLabel("小于:", self.col_win)
        layout.addWidget(col_label1)
        combobox5 = QLineEdit()
        combobox5.setObjectName("小于")
        combobox5.setFixedSize(60, 18)
        layout.addWidget(combobox5)
        self.col_win.setLayout(layout)
        self.setCellWidget(4, 1, self.col_win)
        self.setRowHeight(4, 40)
        self.setSpan(0, 0, 1, 2)
        self.setSpan(1, 0, 1, 2)
        self.setSpan(4, 0, 1, 2)
        self.setSpan(5, 0, 1, 2)
        # 文本包含选择字段
        self.col_win = QWidget()
        layout = QVBoxLayout()
        col_label1 = QLabel("选择字段", self.col_win)
        layout.addWidget(col_label1)
        combobox6 = ComboCheckBox(col_list)
        combobox6.setObjectName("文本包含字段")
        layout.addWidget(combobox6)
        self.col_win.setLayout(layout)
        self.setCellWidget(6, 0, self.col_win)
        self.setRowHeight(6, 80)
        # 文本包含
        self.col_win = QWidget()
        layout = QHBoxLayout()
        col_label1 = QLabel("包含右边文本:", self.col_win)
        layout.addWidget(col_label1)
        combobox7 = QLineEdit(self.col_win)
        combobox7.setObjectName("文本包含内容")
        combobox7.setFixedSize(60, 18)
        layout.addWidget(combobox7)
        self.col_win.setLayout(layout)
        self.setCellWidget(6, 1, self.col_win)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.signal_connect()


class DatasortTableWidget(TabItem):
    def __init__(self, parent=None):
        super(DatasortTableWidget, self).__init__(parent=parent)
        col_name = global_var.get_value("col_name")
        print("数据排序col_name", col_name)
        col_list = copy.deepcopy(col_name)
        col_count = len(col_list)  # 文件中的字段数量
        self.setColumnCount(2)
        self.setRowCount(col_count + 2)
        self.setHorizontalHeaderLabels(['选项', '值'])
        col_list.insert(0, "数据排序")
        for index, item in enumerate(col_list):
            self.kind_comBox = QComboBox()
            self.kind_comBox.setObjectName(col_list[index])
            self.kind_comBox.addItems(['不排序', '升序', '降序'])
            newItem = QTableWidgetItem(item)
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setItem(index, 0, newItem)
            if index > 0:
                self.setCellWidget(index, 1, self.kind_comBox)
        self.setSpan(0, 0, 1, 2)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


class DataoverTableWidget(TabItem):
    def __init__(self, parent=None):
        super(DataoverTableWidget, self).__init__(parent=parent)
        col_name = global_var.get_value("col_name")
        col_list = copy.deepcopy(col_name)
        col_count = len(col_list)  # 文件中的字段数量
        self.setColumnCount(2)
        self.setRowCount(col_count + 1)
        self.setHorizontalHeaderLabels(['选项', '值'])
        col_list.insert(0, "3σ原则异常值处理")
        for index, item in enumerate(col_list):
            self.kind_comBox = QComboBox()
            self.kind_comBox.setObjectName(col_list[index])
            self.kind_comBox.addItems(['不处理', '删除该行', '填为0', '填为平均值', '填为中位数', '填为众数'])
            newItem = QTableWidgetItem(item)
            newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.setItem(index, 0, newItem)
            if index > 0:
                self.setCellWidget(index, 1, self.kind_comBox)
        self.setSpan(0, 0, 1, 2)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
