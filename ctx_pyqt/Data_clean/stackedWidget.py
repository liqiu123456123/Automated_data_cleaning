from .TabItem import *
from .configs import tables

class StackedWidget(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.setMinimumWidth(200)

    def show_table(self, index):
        self.addWidget(tables[index](parent=self.parent))