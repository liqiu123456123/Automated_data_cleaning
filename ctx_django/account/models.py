from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=15, verbose_name="用户名", unique=True, default='匿名用户')
    password = models.CharField(max_length=15, verbose_name="密码")
    nickname = models.CharField(max_length=13, verbose_name="昵称", null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码", default='暂无信息')
    birth_date = models.DateField(verbose_name="出生日期", default='1900-01-01')
    email = models.EmailField(verbose_name="邮箱", default='暂无信息')
    register_time = models.DateTimeField(auto_now_add=True, verbose_name="注册时间")
    last_login_time = models.DateTimeField(auto_now=True, verbose_name="最后登录时间")
    is_active = models.BooleanField(default=True, verbose_name="用户状态")
    register_ip = models.CharField(max_length=20, verbose_name="注册ip")
    last_login_ip = models.CharField(max_length=20, verbose_name="最后登录ip")
    picture = models.ImageField(upload_to="Store/user_picture", verbose_name="用户头像", null=True, blank=True)
    USERNAME_FIELD = 'username'  # 使用authenticate验证时使用的验证字段，可以换成其他字段，但验证字段必须是唯一的，即设置了unique=True
    REQUIRED_FIELDS = ['email']  # 创建用户时必须填写的字段，除了该列表里的字段还包括password字段以及USERNAME_FIELD中的字段
    EMAIL_FIELD = 'email'  # 发送邮件时使用的字段


class EmailValid(models.Model):
    value = models.CharField(max_length = 32)
    email_address = models.EmailField()
    times = models.DateTimeField()
