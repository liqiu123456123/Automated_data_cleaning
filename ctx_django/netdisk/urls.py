from django.urls import re_path
from . import views

app_name = 'netdisk'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^upload/(?P<path>(\S+/?)*)$', views.upload, name='upload'),
    re_path(r'^download/(?P<path>(\S+/?)*)$', views.download, name='download'),
    re_path(r'^folder/(?P<path>([\S]+/?)*)$', views.folder_show, name='folder_show'),
    re_path(r'^folder_all/$', views.folder_list, name='folder_all'),
]