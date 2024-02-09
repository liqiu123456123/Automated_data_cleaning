from celery import shared_task
from .models import *
import time
from ctx_django.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse  # ajax接收json返回的数据
import datetime
import random
def getRandomData():
    result = str(random.randint(1000, 9999))
    return result

@shared_task
def send_email(recver):
    print("开始发送")
    subject = "测试邮件"  # 邮件主题
    text_content = ""  # 发送的文本内容
    value = getRandomData()  # 通过验证码函数获取验证码是
    # 带有html样式的文本内容
    html_content = """    
                    <div>
                        <p>
                            尊敬的ADC用户，您的用户验证码是:%s,打死不要告诉别人。
                        </p>
                    </div>
                    """ % value
    # 确认邮件信息：主题、内容、发件人、收件人（可多人）
    message = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [recver])
    message.attach_alternative(html_content, "text/html")  # 添加带html样式的内容
    message.send()  # 发送

    e = EmailValid()  # 实例化表
    e.email_address = recver  # 存入注册邮箱
    e.value = value  # 存入验证码
    e.times = datetime.datetime.now()  # 存入时间
    e.save()  # 保存入数据库
    print("发送完成")
    return 'Done'



@shared_task
def timing():
    now = time.strftime("%H:%M:%S")
    with open("d:\\output.txt", "a") as f:
        f.write("The time is " + now)
        f.write("\n")
        f.close()
def sendMessage(request):
    result = {"staue": "error", "data": ""}  # ajax的返回值
    if request.method == 'GET' and request.GET:  # 确定是否有get请求
        recver = request.GET.get('email')  # 获取前端输入的注册邮箱，也就是发件人
        subject = "测试邮件"  # 邮件主题
        text_content = ""  # 发送的文本内容
        value = getRandomData()  # 通过验证码函数获取验证码是
        # 带有html样式的文本内容
        html_content = """    
                    <div>
                        <p>
                            尊敬的ADC用户，您的用户验证码是:%s,打死不要告诉别人。
                        </p>
                    </div>
                    """ % value
        # 确认邮件信息：主题、内容、发件人、收件人（可多人）
        message = EmailMultiAlternatives(subject, text_content, EMAIL_HOST_USER, [recver])
        message.attach_alternative(html_content, "text/html")  # 添加带html样式的内容
        message.send()  # 发送
        result['statue'] = 'success'
        result['data'] = '发送成功'

        e = EmailValid()  # 实例化表
        e.email_address = recver  # 存入注册邮箱
        e.value = value  # 存入验证码
        e.times = datetime.datetime.now()  # 存入时间
        e.save()  # 保存入数据库

    return JsonResponse(result)  # 返回