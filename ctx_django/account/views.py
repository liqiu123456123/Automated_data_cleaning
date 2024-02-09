from django.contrib.auth import login
import random

from ctx_django.settings import EMAIL_HOST_USER  # 从配置中导入发件人
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse  # ajax接收json返回的数据
from django.shortcuts import render, redirect
from django.urls import reverse
from netdisk.models import Folder
import datetime
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
    # 判断请求方式是否为post，如果是继续执行
    if request.method == 'POST':
        # 有username值返回username，没有返回空
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        # cp是重复输入的第二次密码
        cp = request.POST.get('cp', '')
        email = request.POST.get('email')  # 获取注册邮箱
        code = request.POST.get('value')  # 获取输入的验证码
        db_email = EmailValid.objects.filter(email_address=email).order_by('-times').first()
        # print("email", email)
        # print("code", code)
        # print("db_email",db_email.value)
        if UserModel.objects.filter(username=u):
            tips = '用户已存在'
        elif cp != p:
            tips = '两次密码输入不一致'
        elif code != db_email.value:
            tips = '验证码错误'
            print("验证码错误")
        else:
            print("注册成功111")

            d = {
                'username': u, 'password': p,
                'is_superuser': 1, 'is_staff': 1,
                'email': email,
            }

            # 插入数据库，create_user注册用户方法
            user = UserModel.objects.create_user(**d)
            # 保存
            tips = '注册成功，请登录'

            logout(request)  # Django内置登出函数，封装了清理session的操作
            return redirect(reverse('user_login'))  # reverse函数：根据url名称解析为对应的url地址  redirect函数：重定向到指定的视图函数或URL
            # 这里是登录完成后重定向到登录界面
    return render(request, 'user.html', locals())  # render作用：将数据渲染到一个指定的模板中，然后将渲染后的页面返回给浏览器。user.html为模板文件名字。
    # render(request, template_name, context=None, content_type=None, status=None, using=None)，请求对象，模板文件名，向模板传递的上下文变量。
    # 两种方式传参,一是：context={‘title’:title}，二使用locals()：对所有局部变量的名称与值进行映射


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
            # authenticate：Django自带的用户认证系统
            user = authenticate(username=u, password=p)
            if user:
                if user.is_active:
                    login(request, user)
                kwargs = {'id': request.user.user_id}
                print("account.views登陆成功")
                user = UserModel.objects.get(username=u)
                print("user.user_id", user.user_id)
                # 创建root文件夹

                try:
                    record = Folder.objects.get(name="root", owner_id=user.user_id)  # 根据您的模型定义进行修改
                except:
                    record = Folder()
                    # 设置字段值（根据您的模型字段进行修改）
                    record.name = "root"  # 设置字段1的值
                    record.path = "root"  # 设置字段2的值
                    record.owner_id = user.user_id  # 设置字段2的值
                    record.parent_id = None  # 设置字段2的值
                    # ... 添加其他字段 ...

                    # 保存记录到数据库
                    record.save()

                return redirect(reverse("netdisk:folder_show", kwargs={"path": "root"}))

            else:
                tips = '账号密码错误，请重新输入'
        else:
            tips = '用户不存在，请注册'
    else:
        pass
        # if request.user.username:
        #     # kwargs = {'id': request.user.id, 'page': 1}
        #     # reverse：返回路由地址，redirect：重定向
        #     # 登陆成功跳转首页
        #     print(111111)
        #     kwargs = {'id': request.user.user_id}
        #     print(request.user.user_id)
        #     return redirect(reverse('about', kwargs=kwargs))
        # # render：返回渲染后的请求对象
    return render(request, 'user.html', locals())


def index(request):
    """首页

    :param request: 请求对象，path函数传递
    :return: HttpResponse对象
    """
    # if request.META.has_key('HTTP_X_FORWARDED_FOR'):
    #     ip =  request.META['HTTP_X_FORWARDED_FOR']
    # else:
    #     ip = request.META['REMOTE_ADDR']
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
    # print(request_data)

    return render(request, 'xmind.html')


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
        print(333333333333333)
        u = request.POST.get('username', '')
        p = request.POST.get('phone', '')
        # d = request.POST.get('birth_date', '')
        print(u, p)
        user = UserModel.objects.filter(user_id=id)
        user.update(username=u, phone=p)
        return render(request, 'update.html', locals())
    return render(request, 'update.html', locals())


def sendMessage(request):
    recver = request.GET.get('email')
    print("recver",recver)
    send_email.delay(recver)
    print("recver", recver)
    result = {"staue": "error", "data": ""}  # ajax的返回值
    result['statue'] = 'success'
    result['data'] = '发送成功'
    return JsonResponse(result)

# def sendMessage(request):
#     result = {"staue": "error", "data": ""}  # ajax的返回值
#     if request.method == 'GET' and request.GET:  # 确定是否有get请求
#         recver = request.GET.get('email')  # 获取前端输入的注册邮箱，也就是发件人
#         subject = "测试邮件"  # 邮件主题
#         text_content = ""  # 发送的文本内容
#         value = getRandomData()  # 通过验证码函数获取验证码是
#         # 带有html样式的文本内容
#         html_content = """
#                     <div>
#                         <p>
#                             尊敬的ADC用户，您的用户验证码是:%s,打死不要告诉别人。
#                         </p>
#                     </div>
#                     """ % value
#         # 确认邮件信息：主题、内容、发件人、收件人（可多人）
#         message = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [recver])
#         message.attach_alternative(html_content, "text/html")  # 添加带html样式的内容
#         message.send()  # 发送
#         result['statue'] = 'success'
#         result['data'] = '发送成功'
#
#         e = EmailValid()  # 实例化表
#         e.email_address = recver  # 存入注册邮箱
#         e.value = value  # 存入验证码
#         e.times = datetime.datetime.now()  # 存入时间
#         e.save()  # 保存入数据库
#
#     return JsonResponse(result)  # 返回
