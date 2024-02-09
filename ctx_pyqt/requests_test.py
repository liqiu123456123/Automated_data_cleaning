import json
import mimetypes
import re

import requests
from bs4 import BeautifulSoup


class Requests_Api:
    def __init__(self, username, password):
        self.session = requests.Session()
        self.username = username
        self.password = password

    def login_decorator(func):
        def wrapper(self, *args, **kwargs):
            self.session = requests.Session()
            login_url = "http://127.0.0.1:8000/login"
            res = self.session.get(login_url)
            soup = BeautifulSoup(res.text, "lxml")
            token_label = soup.find(type="hidden")
            token = token_label.attrs["value"]
            data = {"csrfmiddlewaretoken": token, "username": self.username, "password": self.password,
                    "Submit": "登录"}
            res_login = self.session.post(login_url, data)
            result = func(self, *args, **kwargs)
            return result

        return wrapper

    def login(self, url, username, password):
        self.session = requests.Session()
        url = url
        res = self.session.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        token_label = soup.find(type="hidden")
        token = token_label.attrs["value"]
        data = {"csrfmiddlewaretoken": token, "username": username, "password": password, "Submit": "登录"}
        res_login = self.session.post(url, data)
        return res_login

    def resgiter(self, url, username, password, cp, email, value):
        session = requests.Session()
        url = url
        res = session.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        token_label = soup.find(type="hidden")
        token = token_label.attrs["value"]
        data = {"csrfmiddlewaretoken": token, "username": username, "password": password, "Submit": "注册",
                "cp": cp, "email": email, "value": value}
        res_res = session.post(url, data)
        return res_res

    @login_decorator
    def get_folder_file(self, url):
        # 处理成{'folders': [], 'files': ['bbb.html', 'athlete_events.csv'], 'path': 'root/123'}格式
        # 考虑新用户全为空的情况
        path = re.search(r'root(.*?\?)', url).group(0)[:-1]
        res = self.session.get(url)
        res_dict = json.loads(res.text)
        folder_list = []
        # 文件只有一个是字典，多个时为列表
        try:
            for item in res_dict["folder"]:
                folder_list.append(item["path"])
        except TypeError:
            folder_list.append(res_dict["folder"]["path"])
        file_list = []
        file = res_dict["files"]
        for item in file:
            file_list.append(item["name"])
        context = {"folders": folder_list, "files": file_list, "path": path}
        return context

    @login_decorator
    def get_folder_all(self):
        url = "http://127.0.0.1:8000/netdisk/folder_all/"
        res = self.session.get(url)
        res_dict = json.loads(res.text)
        return res_dict

    @login_decorator
    def get_url(self, url):
        res = self.session.get(url)
        res_dict = json.loads(res.text)
        return res_dict

    @login_decorator
    def new_folder(self, name, path, parent, owner):
        url = "http://127.0.0.1:8000/netdisk/folder_all/"
        res = self.session.get(url)
        token = self.get_token()
        header = {"X-CSRFTOKEN": token}
        data = {
            "name": name,
            "path": path,
            "parent": parent,
            "owner": owner
        }
        res = self.session.post(url=url, data=data, headers=header)
        print("新建")
        if "200" in res:
            print("新建成功")

    @login_decorator
    def get_token(self):

        url = "http://127.0.0.1:8000/login"
        res = self.session.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        token_label = soup.find(type="hidden")
        token = token_label.attrs["value"]
        return token

    @login_decorator
    def upload_file(self, url, file_path):
        # self.login("http://127.0.0.1:8000/login", "liqile_update", "qq674658532")
        url_1 = "http://127.0.0.1:8000/login"
        res = self.session.get(url_1)
        soup = BeautifulSoup(res.text, "lxml")
        token_label = soup.find(type="hidden")
        token = token_label.attrs["value"]
        header = {"X-CSRFTOKEN": token}
        url = url
        fileObject = {'files': (file_path, open(file_path, 'rb'), mimetypes.guess_type(file_path)[0])}

        # 发送POST请求上传文件
        # token = self.get_token()
        response = self.session.post(url, headers=header, files=fileObject)

        # 检查响应
        if response.status_code == 200:
            print('文件上传成功！')
        else:
            print('文件上传失败，状态码：', response.status_code)
            print('响应内容：', response.text)

    @login_decorator
    def down_file(self, url, file_path):
        # url = 'http://127.0.0.1:8000/netdisk/download/root/详细全面的鱼小铺开通方法2.pdf'  # 替换为您要下载的文件的URL
        url = url
        response = self.session.get(url, stream=True)
        with open(file_path, 'wb') as code:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    code.write(chunk)
        print("下载完成")

    @login_decorator
    def update_name(self, url, data):
        url1 = "http://127.0.0.1:8000/netdisk/folder_all/"
        res = self.session.get(url1)
        token = self.get_token()
        header = {"X-CSRFTOKEN": token}
        res = self.session.put(url, data=data, headers=header)
        print("修改文件夹名完成")

    @login_decorator
    def update_file_name(self, url, data):
        url1 = "http://127.0.0.1:8000/netdisk/folder_all/"
        res = self.session.get(url1)
        token = self.get_token()
        header = {"X-CSRFTOKEN": token}
        res = self.session.put(url, data=data, headers=header)

    def get_code(self, email):
        url = "http://127.0.0.1:8000/user/sendemail/?" + "email=" + email
        requests.get(url)

    @login_decorator
    def delete_folder(self, url):
        url1 = "http://127.0.0.1:8000/netdisk/folder_all/"
        res = self.session.get(url1)
        token = self.get_token()
        header = {"X-CSRFTOKEN": token}
        res = self.session.delete(url, headers=header)

    @login_decorator
    def delete_file(self, url, data):
        url1 = "http://127.0.0.1:8000/netdisk/folder_all/"
        res = self.session.get(url1)
        token = self.get_token()
        header = {"X-CSRFTOKEN": token}
        res = self.session.put(url, data=data, headers=header)
        print("删除文件res", res)
        print("删除文件完成")



if __name__ == '__main__':
    demo = Requests_Api()
    demo.upload_file()
