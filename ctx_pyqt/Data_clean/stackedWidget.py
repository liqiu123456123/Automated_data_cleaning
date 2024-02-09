from deal_tool.CTX.ctx_pyqt.Data_clean.TabItem import *
from deal_tool.CTX.ctx_pyqt.Data_clean.configs import tables

class StackedWidget(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.setMinimumWidth(200)

    def show_table(self, index):
        self.addWidget(tables[index](parent=self.parent))