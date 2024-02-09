# coding = utf-8
# Dragon's Python3.8 code
# Created at 2021/5/8 21:50
# Edit with PyCharm
import hashlib
import os
import shutil
import uuid

from django.conf import settings
from netdisk.models import File, Digest

MEDIA_ROOT = os.path.join(settings.MEDIA_ROOT,'netdisk')

def check_path_exits(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def remove_blank(text:str):
    return text.replace(" ","")


def handle_upload_files(files, parent_obj, owner=None):
    # 获取当前目录内的文件
    # file_list = File.objects.filter(dir=parent_obj,owner=owner)
    # 检查目录是否存在
    check_path_exits(MEDIA_ROOT)

    for file in files:
        digest = hashlib.md5()
        # 防止文件重名
        name = remove_blank(file.name)
        #unique_name = get_unique_file_name(name, file_list)
        temp_name = os.path.join(MEDIA_ROOT, file.name)
        ## 计算文件的MD5并作为文件名保存至MEDIA_ROOT
        with open(temp_name, 'wb+') as destination:
            for chunk in file.chunks(chunk_size=1024):
                destination.write(chunk)
                destination.flush()
                digest.update(chunk)

        digest = digest.hexdigest()
        file_path = os.path.join(MEDIA_ROOT, digest)
        digest_obj, created = Digest.objects.get_or_create(digest=digest)
        # 创建文件对象
        File.objects.create(name=name,
                            dir=parent_obj,
                            owner=owner,
                            size=file.size)
        # 重命名文件
        shutil.move(temp_name,file_path)


def get_unique_folder_name(name, content_list):
    ## 检查是否有重名的文件夹并按顺序生成新名称
    folder_list = [content.name for content in content_list]
    if name in folder_list:
        cont = 1
        while f'{name}({cont})' in folder_list:
            cont += 1
        name = f'{name}({cont})'
    return name


def get_unique_file_name(name, content_list):
    ## 检查是否有重名的文件夹并按顺序生成新名称
    prefix, suffix = os.path.splitext(name)
    folder_list = [content.name for content in content_list]
    if name in folder_list:
        cont = 1
        while f'{prefix}({cont}){suffix}' in folder_list:
            cont += 1
        name = f'{prefix}({cont}){suffix}'
    return name


def path_to_link(folder):
    path_link = []
    while folder.parent:
        path_link.append(("/"+folder.name, folder.path))
        folder = folder.parent
    path_link.append((folder.name,folder.path))
    return reversed(path_link)
