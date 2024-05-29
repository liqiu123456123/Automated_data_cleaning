def ctx_ui_style():
    return '''
    QFrame, QTextEdit, QDockWidget, QTableView, QTreeView, QMenuBar {
        background-color: #BFEFFF;
    }

    QDockWidget {
        font-family: 微软雅黑;
        font-size: 18px;
    }

    QTableView {
        color: #000000;
    }

    QMenu {
        background-color: #BFEFFF;
        border: 1px solid rgba(82,130,164,1);
    }

    QMenu::item {
        min-width: 50px;
        font-size: 12px;
        color: #000000;
        background-color: #B2DFEE;
        border: 1px solid rgba(82,130,164,1);
        padding: 1px;
        margin: 1px;
    }

    QMenu::item:selected {
        background-color: #9AC0CD;
        border: 1px solid rgba(82,130,164,1);
    }

    QMenu::item:pressed {
        background-color: #B2DFEE;
        border: 1px solid rgba(82,130,164,1);
    }

    QMenuBar {
        background-color: #BFEFFF;
        border: 1px solid rgba(82,130,164,1);
    }

    QMenuBar::selected {
        background-color: transparent;
    }

    QMenuBar::item {
        font-size: 16px;
        font-family: Microsoft YaHei;
        color: #000000;
    }

    QHeaderView::section {
        background-color: #BFEFFF;
        color: black;
    }
    '''
