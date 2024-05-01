from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QMessageBox, QFrame, QHBoxLayout, QVBoxLayout, \
    QStackedWidget
from qfluentwidgets import LineEdit, PasswordLineEdit, PrimaryPushButton, FluentIcon as FIF
from mian_win_web import WebUi
from project_requests import Requests_Api


class Widget_web(QFrame):
    def __init__(self, text, parent, username, password):
        super().__init__(parent=parent)
        username = username
        password = password
        self.hBoxLayout = QHBoxLayout(self)
        webui = WebUi(username, password)
        self.hBoxLayout.addWidget(webui)
        self.setObjectName(text.replace(' ', '-'))


class LoginWin(QWidget):
    def __init__(self):
        super().__init__()
        self.request_api = None
        self.init_ui()

    def init_ui(self) -> None:
        self.login_layout = QVBoxLayout()
        self.login_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        login_title = QLabel("Automated_data_cleaning", self)
        login_title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 水平垂直居中对齐
        self.username = LineEdit(self)
        self.username.setFixedSize(320, 30)
        self.username.setPlaceholderText('账号')
        self.password = PasswordLineEdit(self)
        self.password.setFixedSize(320, 30)
        self.password.setPlaceholderText('密码')
        login_button = PrimaryPushButton('登录', self, FIF.UPDATE)
        login_button.setFixedSize(320, 30)
        login_button.clicked.connect(self.login)
        login_title.setStyleSheet("color: #000000;font-weight: bold;font-size: 20px; ")
        self.login_layout.addWidget(login_title)
        self.login_layout.addWidget(self.username)
        self.login_layout.addWidget(self.password)
        self.login_layout.addWidget(login_button)
        self.setLayout(self.login_layout)
        self.login_layout.setSpacing(30)
        self.login_layout.setContentsMargins(0, 30, 0, 90)

    def login(self):
        username = self.username.text()
        password = self.password.text()
        url = "http://127.0.0.1:8000/login"
        self.request_api = Requests_Api(username, password)
        response = self.request_api.login(url, username, password)
        if "用户登陆" not in response.text:
            self.videoInterface2 = Widget_web('Video Interface2', self, username, password)
            self.parent.addSubInterface(self.videoInterface2, FIF.CLOUD, '云盘')
            self.close()


class ResWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.request_api = None
        self.init_ui()

    def init_ui(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        code_layout = QHBoxLayout()
        code_layout.setSpacing(20)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)
        login_title = QLabel("Automated_data_cleaning", self)
        login_title.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 水平垂直居中对齐
        self.username = LineEdit(self)
        self.username.setFixedSize(320, 30)
        self.username.setPlaceholderText('账号')
        self.password = PasswordLineEdit(self)
        self.password.setFixedSize(320, 30)
        self.password.setPlaceholderText('密码')
        self.confirm_password = PasswordLineEdit(self)
        self.confirm_password.setFixedSize(320, 30)
        self.confirm_password.setPlaceholderText('确认密码')
        self.email = LineEdit(self)
        self.email.setPlaceholderText('邮箱账号')
        self.email.setFixedSize(320, 30)
        self.code = LineEdit(self)
        self.code.setPlaceholderText('验证码')
        self.code.setFixedSize(180, 30)
        code_button = QPushButton('获取验证码', self)
        code_button.setFixedSize(120, 30)
        code_button.clicked.connect(self.get_code)
        login_button = PrimaryPushButton('注册', self, FIF.UPDATE)
        login_button.clicked.connect(self.register)
        login_title.setStyleSheet("color: #000000;font-weight: bold;font-size: 20px; ")
        code_layout.addWidget(self.code)
        code_layout.addWidget(code_button)
        main_layout.addWidget(login_title)
        main_layout.addWidget(self.username)
        main_layout.addWidget(self.password)
        main_layout.addWidget(self.confirm_password)
        main_layout.addWidget(self.email)
        main_layout.addLayout(code_layout)
        main_layout.addWidget(login_button)

    def register(self):
        # 有username值返回username，没有返回空
        self.username_text = self.username.text()
        self.password_text = self.password.text()
        cp = self.confirm_password.text()
        email = self.email.text()
        value = self.code.text()
        self.request_api = Requests_Api(self.username_text, self.password_text)
        url = "http://127.0.0.1:8000/user/register"
        request = self.request_api.resgiter(url, self.username_text, self.password_text, cp, email, value)
        # 验证码不对提示
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
        self.request_api = Requests_Api(self.username_text, self.password_text)
        email = self.email.text()
        self.request_api.get_code(email)


class LoginMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("登录注册窗口")
        self.resize(800, 600)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)
        self.loginWidget = LoginWin()
        self.stack.addWidget(self.loginWidget)
        self.registerWidget = ResWindow()
        self.stack.addWidget(self.registerWidget)
        self.loginButton = QPushButton('还没有账号，去注册', self)
        self.loginButton.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        layout.addWidget(self.loginButton)
        self.registerButton = QPushButton('已经有账号，去登陆', self)
        self.registerButton.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        layout.addWidget(self.registerButton)