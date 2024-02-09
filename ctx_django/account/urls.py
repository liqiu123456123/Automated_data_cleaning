from django.urls import path
from .views import *

urlpatterns = [
    path('register', register, name='register'),  # 注册
    path('login', user_login, name='user_login'),  # 登录
    path('', index, name="index"),  # 首页
    path('about/<int:id>', about, name='about'),
    path('update/<int:id>', user_update, name="update"),  # 首页
    path('sendemail/', sendMessage)
]
