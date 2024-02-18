import random
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import JsonResponse  # ajax接收json返回的数据
from django.shortcuts import render, redirect
from django.urls import reverse
from netdisk.models import Folder

from .models import *
from .tasks import send_email


def getRandomData():
    result = str(random.randint(1000, 9999))
    return result


def register(request):
    """用户注册函数

    :param request: 请求对象，path函数传递
    :return:HttpResponse对象
    """
    tab_title = '用户注册'
    page_title = '用户注册'
    confirm_password = True
    button = '注册'
    url_text = '用户登录'
    url_name = 'user_login'
    if request.method == 'POST':
        # 有username值返回username，没有返回空
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password_two = request.POST.get('cp', '')
        email = request.POST.get('email')  # 获取注册邮箱
        code = request.POST.get('value')  # 获取输入的验证码
        db_email = EmailValid.objects.filter(email_address=email).order_by('-times').first()
        if UserModel.objects.filter(username=username):
            tips = '用户已存在'
        elif password_two != password:
            tips = '两次密码输入不一致'
        elif code != db_email.value:
            tips = '验证码错误'
        else:
            user_dict = {
                'username': username, 'password': password,
                'is_superuser': 1, 'is_staff': 1,
                'email': email,
            }

            # 插入数据库，create_user注册用户方法
            user = UserModel.objects.create_user(**user_dict)
            # 保存
            tips = '注册成功，请登录'
            logout(request)  # Django内置登出函数，封装了清理session的操作
            return redirect(reverse('user_login'))  # reverse函数：根据url名称解析为对应的url地址  redirect函数：重定向到指定的视图函数或URL
    return render(request, 'user.html', locals())



def user_login(request):
    """登录函数

    :param request: 请求对象，path函数传递
    :return: HttpResponse对象
    """
    tab_title = '用户登录'
    page_title = '用户登录'
    button = '登录'
    url_text = '用户注册'
    url_name = 'register'
    if request.method == 'POST':
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        if UserModel.objects.filter(username=u):
            user = authenticate(username=u, password=p)
            if user:
                if user.is_active:
                    login(request, user)
                kwargs = {'id': request.user.user_id}
                user = UserModel.objects.get(username=u)
                # 创建root文件夹
                # 新用户自动创建root文件夹
                try:
                    record = Folder.objects.get(name="root", owner_id=user.user_id)  # 根据您的模型定义进行修改
                except:
                    record = Folder()
                    # 设置字段值（根据您的模型字段进行修改）
                    record.name = "root"  # 设置字段1的值
                    record.path = "root"  # 设置字段2的值
                    record.owner_id = user.user_id  # 设置字段2的值
                    record.parent_id = None  # 设置字段2的值
                    # 保存记录到数据库
                    record.save()

                return redirect(reverse("netdisk:folder_show", kwargs={"path": "root"}))

            else:
                tips = '账号密码错误，请重新输入'
        else:
            tips = '用户不存在，请注册'
    else:
        pass
    return render(request, 'user.html', locals())


def index(request):
    """首页

    :param request: 请求对象，path函数传递
    :return: HttpResponse对象
    """
    request_data = {}
    if request.environ.get("HTTP_X_REAL_IP", False):
        # 从环境信息获取
        request_data['ip'] = request.environ.get("HTTP_X_REAL_IP", None)
    elif request.headers.get("X-Real-Ip", False):
        # 从头部信息获取
        request_data['ip'] = request.headers.get("X-Real-Ip", None)
    else:
        # 获取一般的地址
        request_data['ip'] = request.META['REMOTE_ADDR']

    return render(request, 'home.html')


def about(request, id):
    user = UserModel.objects.filter(user_id=id).first()
    return render(request, 'about.html', locals())


def user_update(request, id):
    tab_title = '信息修改'
    page_title = '信息修改'
    button = '修改'
    url_text = '确认修改'
    url_name = 'register'
    if request.method == 'POST':
        u = request.POST.get('username', '')
        p = request.POST.get('phone', '')
        user = UserModel.objects.filter(user_id=id)
        user.update(username=u, phone=p)
        return render(request, 'update.html', locals())
    return render(request, 'update.html', locals())


def sendMessage(request):
    recver = request.GET.get('email')
    send_email.delay(recver)
    result = {"staue": "error", "data": ""}  # ajax的返回值
    result['statue'] = 'success'
    result['data'] = '发送成功'
    return JsonResponse(result)
