from django.urls import re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from rest_framework import routers
# from .views import UploadedFileViewSet
app_name = 'netdisk'

# router = routers.DefaultRouter()
# router.register(r'uploaded-files', UploadedFileViewSet)

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'back/$', views.prev_folder, name='prev_folder'),
    re_path(r'^create/(?P<path>(\S+/?)*)$', views.create, name='create'),
    re_path(r'^upload/(?P<path>(\S+/?)*)$', views.upload, name='upload'),
    re_path(r'^preview/(?P<path>([\S]+/?)*)$', views.preview, name='preview'),
    re_path(r'^download/(?P<path>(\S+/?)*)$', views.download, name='download'),
    re_path(r'^folder/(?P<path>([\S]+/?)*)$', views.folder_show, name='folder_show'),
    re_path(r'^folder_all/$', views.folder_list, name='folder_all'),
    # re_path(r'^articles/$', views.article_list),
    # re_path(r'^articles/(?P<pk>[0-9]+)$', views.article_detail),
    re_path(r'^delete/(?P<type>(file|folder))&(?P<path>([\S]+/?)*)$', views.delete, name='delete'),
    re_path(r'^rename/(?P<type>(file|folder))&(?P<path>([\S]+/?)*)$', views.rename, name='rename'),
    # path('api/', views.uplode_list),
    path("api/uploaded-files/",views.UpFileAPIView.as_view())
]


#rlpatterns = format_suffix_patterns(urlpatterns)