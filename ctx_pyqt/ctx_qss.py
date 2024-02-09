def ctx_ui_style():
    return'''
    QFrame {
           background-color: #BFEFFF;
           }
    QTextEdit {
           background-color: #BFEFFF;
           }
    QDockWidget {
           background-color: #BFEFFF;
           font-family: 微软雅黑;
           font-size: 18px;
           }
    QTableView {
           background-color: #BFEFFF;
           color: #000000;
}
    QMenu {
            background-color:#BFEFFF;
            border:1px solid rgba(82,130,164,1);
    }
    QMenu::item {
            min-width:50px;
            font-size: 12px;
            color: #000000;
            background-color:#B2DFEE;
            border:1px solid rgba(82,130,164,1);
            padding:1px 1px;
            margin:1px 1px;}

    QMenu::item:selected {
            background-color:#9AC0CD;
            border:1px solid rgba(82,130,164,1);
            }  /*选中或者说鼠标滑过状态*/
    QMenu::item:pressed {
            background-color:#B2DFEE;
            border:1px solid rgba(82,130,164,1);/*摁下状态*/
                }

    QMenuBar {
            background-color:#BFEFFF;
            border:1px solid rgba(82,130,164,1);
                }
    QMenuBar::selected{
            background-color:transparent;
                }/*设置菜单栏选中背景色*/
    QMenuBar::item{
            font-size:16px;
            font-family:Microsoft YaHei;color:#000000;
                }/*设置菜单栏字体为白色，透明度为1（取值范围0.0-255）*/

    QTreeView{
            background-color:#BFEFFF;
                }

    QHeaderView::section {
            background-color: #BFEFFF;
            color: black;
            }
}
            '''