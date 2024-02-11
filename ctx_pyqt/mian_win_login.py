
import sys

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QMessageBox
from PyQt5.QtWidgets import QFrame, QHBoxLayout,QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout, QStackedWidget
from qfluentwidgets import FluentIcon
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import LineEdit, PasswordLineEdit, PrimaryPushButton, HyperlinkLabel

from mian_win_web import WebUi
from project_requests import Requests_Api



class Widget_web(QFrame):
    def __init__(self, text, parent,username,password):
        super().__init__(parent=parent)
        username = username
        password = password
        self.hBoxLayout = QHBoxLayout(self)
        webui = WebUi(username,password)
        self.hBoxLayout.addWidget(webui)
        self.setObjectName(text.replace(' ', '-'))

class LoginWin(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.request_api = None
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle('登录')

        login_title = QLabel("ADC,您的团队数据分析利器", self)
        self.username = LineEdit(self)
        self.username.setPlaceholderText('账号')
        self.password = PasswordLineEdit(self)
        self.password.setPlaceholderText('密码')
        login_button = PrimaryPushButton('登录', self, FluentIcon.UPDATE)
        login_button.clicked.connect(self.login)
        forget_link = HyperlinkLabel('忘记密码？', self)
        image_label = QLabel(self)
        image_qq_label = QLabel(self)
        image_wx_label = QLabel(self)
        image_wb_label = QLabel(self)
        pix_winter = QPixmap("冬季.jpg")
        pix_qq = QPixmap("企鹅.png")
        pix_wx = QPixmap("V.png")
        pix_wb = QPixmap("403420.png")
        image_label.setPixmap(pix_winter)
        image_qq_label.setPixmap(pix_qq)
        image_wx_label.setPixmap(pix_wx)
        image_wb_label.setPixmap(pix_wb)
        # self.setStyleSheet("QWidget{background: #BBFFFF}")
        login_title.setStyleSheet("color: #000000;font-weight: bold;font-size: 26px; ")
        self.setGeometry(300, 300, 960, 640)
        self.username.setGeometry(600, 224, 235, 40)
        self.password.setGeometry(600, 300, 235, 40)
        login_button.setGeometry(600, 380, 235, 30)
        # regsiter_button.setGeometry(600, 380, 100, 30)
        image_label.setGeometry(90, 100, 440, 420)
        image_wb_label.move(780, 450)
        login_title.move(570, 140)
        forget_link.move(685, 420)
        image_qq_label.move(600, 450)
        image_wx_label.move(690, 450)

    def login(self):
        print("开始登陆")
        username = self.username.text()
        password = self.password.text()
        url = "http://127.0.0.1:8000/login"
        self.request_api = Requests_Api(username,password)
        response = self.request_api.login(url, username, password)
        if "用户登陆" not in response.text:
            self.videoInterface2 = Widget_web('Video Interface2', self, username,password)
            self.parent.addSubInterface(self.videoInterface2, FIF.CLOUD, '云盘')
            self.close()


class ResWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.request_api = None
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle('注册')
        main_layout = QVBoxLayout()
        code_layout = QHBoxLayout()
        self.setLayout(main_layout)
        login_title = QLabel("ADC,您的团队数据分析利器", self)
        self.username = LineEdit(self)
        self.username.setPlaceholderText('账号')
        self.password = PasswordLineEdit(self)
        self.password.setPlaceholderText('密码')
        self.confirm_password = PasswordLineEdit(self)
        self.confirm_password.setPlaceholderText('确认密码')
        self.email = LineEdit(self)
        self.email.setPlaceholderText('邮箱账号')
        self.code = LineEdit(self)
        self.code.setPlaceholderText('验证码')
        code_button = QPushButton('获取验证码', self)
        code_button.clicked.connect(self.get_code)
        login_button = PrimaryPushButton('注册', self, FluentIcon.UPDATE)
        login_button.clicked.connect(self.register)
        image_label = QLabel(self)
        image_qq_label = QLabel(self)
        image_wx_label = QLabel(self)
        image_wb_label = QLabel(self)
        pix_winter = QPixmap("冬季.jpg")
        pix_qq = QPixmap("企鹅.png")
        pix_wx = QPixmap("V.png")
        pix_wb = QPixmap("403420.png")
        image_label.setPixmap(pix_winter)
        image_qq_label.setPixmap(pix_qq)
        image_wx_label.setPixmap(pix_wx)
        image_wb_label.setPixmap(pix_wb)
        login_title.setStyleSheet("color: #000000;font-weight: bold;font-size: 26px; ")
        self.setGeometry(300, 300, 960, 640)
        self.username.setGeometry(600, 224, 235, 40)
        self.password.setGeometry(600, 300, 235, 40)
        self.confirm_password.setGeometry(600, 376, 235, 40)
        self.email.setGeometry(600, 446, 235, 40)
        code_layout.addWidget(self.code)
        code_layout.addWidget(code_button)
        main_layout.addWidget(login_title)
        main_layout.addWidget(self.username)
        main_layout.addWidget(self.password)
        main_layout.addWidget(self.confirm_password)
        main_layout.addWidget(self.email)
        main_layout.addLayout(code_layout)
        main_layout.addWidget(login_button)
        # login_button.setGeometry(600, 430, 235, 30)
        # image_label.setGeometry(90, 100, 440, 420)
        # image_wb_label.move(780, 450)
        # login_title.move(570, 140)
        # image_qq_label.move(600, 450)
        # image_wx_label.move(690, 450)

    def register(self):
        # 有username值返回username，没有返回空
        print("注册")
        self.username_text = self.username.text()
        self.password_text = self.password.text()
        cp = self.confirm_password.text()
        email = self.email.text()
        value = self.code.text()
        self.request_api = Requests_Api(self.username_text,self.password_text)
        url = "http://127.0.0.1:8000/user/register"
        request = self.request_api.resgiter(url, self.username_text, self.password_text,cp,email,value)
        # 验证码不对提示
        print(request.text)
        if "确认密码" not in request.text:
            msg_box = QMessageBox(QMessageBox.Information, '完成提示', '恭喜您，注册完成')
            msg_box.exec_()
        if "验证码错误" in request.text:
            msg_box = QMessageBox(QMessageBox.Information, '完成提示', '验证码错误')
            msg_box.exec_()
    def get_code(self):
        # 发送验证码
        self.username_text = self.username.text()
        self.password_text = self.password.text()
        self.request_api = Requests_Api(self.username_text,self.password_text)
        email = self.email.text()
        self.request_api.get_code(email)

class LoginMainWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.loginWidget = LoginWin(self.parent)
        self.stack.addWidget(self.loginWidget)

        self.registerWidget = ResWindow()
        self.stack.addWidget(self.registerWidget)

        self.loginButton = QPushButton('还没有账号，去注册', self)
        self.loginButton.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(self.loginButton)

        self.registerButton = QPushButton('已经有账号，去登陆', self)
        self.registerButton.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(self.registerButton)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = LoginMainWindow(1)
    demo.show()
    sys.exit(app.exec_())





