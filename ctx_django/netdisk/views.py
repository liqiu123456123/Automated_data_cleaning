# Create your views here.
import os

from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import File, Folder, UserModel
from .serializers import FileSerializer, FolderSerializer
from .utils import handle_upload_files, get_unique_folder_name, remove_blank


def index(request):
    if request.method == "GET":
        Folder.create_root(request.user)
        return redirect(reverse("netdisk:folder_show", kwargs={"path": "root"}))


def upload(request, path):
    if request.method == "POST":
        files = request.FILES.getlist("files")
        print("request.post", request.FILES)
        print("upload", request.user)
        parent = get_object_or_404(Folder, path=path, owner=request.user)
        handle_upload_files(files, parent, request.user)
        print("handle_upload_files", files, parent, request.user)
        return render(request, 'pageJump.html', {'message': '上传成功'})


def download(request, path):
    if request.method == 'GET':
        name = os.path.basename(path)
        dir = os.path.dirname(path)
        file = get_object_or_404(File, name=name, dir__path=dir, owner=request.user)
        response = FileResponse(open(file.get_file_path(), 'rb'))
        response["Content-Length"] = file.size
        response['Content-Disposition'] = f'attachment;filename="{name}"'
        return response


def preview(request, path):
    if request.method == 'GET':
        name = os.path.basename(path)
        dir = os.path.dirname(path)
        file = get_object_or_404(File, name=name, dir__path=dir, owner=request.user)
        return render(request, 'preview.html', context={'file': file})


# def folder_show(request, path):
#     if request.method == 'GET':
#         if path == "":
#             path = "root"
#         # 获取所有数据
#         all_data = Folder.objects.all()
#
#         # 遍历数据并输出
#         # for data in all_data:
#         #     print(data.name, data.path, data.parent, data.owner, data.creat_time)
#         basedir = get_object_or_404(Folder, path=path, owner=request.user)
#         # 获取要展示的文件夹和文件
#         folder = Folder.objects.filter(parent=basedir, owner=request.user)
#         files = File.objects.filter(dir=basedir, owner=request.user)
#         # 用于直接返回多层目录
#         path_link = path_to_link(basedir)
#         context = {'folders': folder, 'files': files, 'path': path, 'path_link': path_link}
#         # print("context", context)
#         return render(request, "netdisk/folder.html", context)

# class UploadedFileViewSet(viewsets.ModelViewSet):
#     print(222222222222222)
#     queryset = File.objects.all()
#     print("queryset",queryset)
#     serializer_class = UploadedFileSerializer
#     print("serializer_class",serializer_class)

class UpFileAPIView(APIView):
    def create(self, request, format=None):
        file_obj = request.FILES.get('file')
        print(file_obj)
        # 在这里可以将上传的文件保存到服务器上
        return Response({'status': 'success'})




@api_view(['GET', 'POST'])
def folder_list(request, format=None):
    """
    展示当前用户所有的文件夹。不应该跨用户
    """
    if request.method == 'GET':
        # 查询当前用户所有的文件夹，包括子文件夹
        folder = Folder.objects.filter(owner_id=request.user)
        serializer = FolderSerializer(folder, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            user_tmp = get_object_or_404(UserModel, user_id=request.data["owner"])
            serializer.save(owner=user_tmp)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def folder_show(request, path, format=None):
    try:
        folder = Folder.objects.get(path=path, owner_id=request.user)
    except Folder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = FolderSerializer(folder)
        basedir = get_object_or_404(Folder, path=path, owner=request.user)
        # 获取要展示的文件夹和文件
        folder = Folder.objects.filter(parent=basedir, owner=request.user)
        serializer = FolderSerializer(folder, many=True)
        files = File.objects.filter(dir=basedir, owner=request.user)
        serializer_file = FileSerializer(files, many=True)  # 使用many=True来处理多个文件
        return Response({
            'folder': serializer.data,
            'files': serializer_file.data
        })

    # return Response(serializer.data)

    elif request.method == 'PUT':
        #  利用put请求删除文件
        if "size" in request.data:
            print("进入更新/删除文件函数")
            file = File.objects.get(id=request.data["id"])
            if "del_file" in request.data["name"]:
                print("开始删除文件")
                file.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                serializer = FileSerializer(file, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
        else:
            folder = Folder.objects.get(id=request.data["id"])
            serializer = FolderSerializer(folder, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        print("进入删除views")
        folder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def create(request, path):
    #  POST：新建
    if request.method == 'POST':
        parent = get_object_or_404(Folder, path=path, owner=request.user)
        name = remove_blank(request.POST.get("folder_name"))
        # 检查是否有重名
        folder_list = Folder.objects.filter(parent=parent, owner=request.user)
        unique_name = get_unique_folder_name(name, folder_list)
        # 创建文件夹
        path = "/".join([path, unique_name])
        Folder.objects.create(name=unique_name, path=path, parent=parent, owner=request.user)

        return redirect(reverse("netdisk:folder_show", kwargs={"path": parent.path}))


def rename(request, type, path):
    if request.method == 'POST':
        new_name = remove_blank(request.POST.get("new_name"))
        if type == 'folder':
            obj = Folder.objects.get(path=path, owner=request.user)
            folder_list = Folder.objects.filter(parent=obj.parent, owner=request.user)
            unique_name = get_unique_folder_name(new_name, folder_list)
            obj.name = unique_name
            obj.path = "/".join([os.path.dirname(obj.path), unique_name])
            obj.save()
            message = "文件夹：{}重命名为{}".format(path, obj.path)

        elif type == 'file':
            name = os.path.basename(path)
            suffix = os.path.splitext(name)[1]
            dir = os.path.dirname(path)
            file = get_object_or_404(File, name=name, dir__path=dir, owner=request.user)
            if not os.path.splitext(new_name)[1]:  # 新名称不含后缀名时添加后缀
                new_name += suffix
            file_list = File.objects.filter(dir=file.dir)
            new_name = get_unique_folder_name(new_name, file_list)
            file.name = new_name
            file.save()
            message = "文件：{}重命名为{}".format(name, new_name)

        return render(request, 'pageJump.html', {'message': message})


def delete(request, type, path):
    if request.method == 'POST':
        if type == 'folder':
            obj = Folder.objects.get(path=path, owner=request.user)
            obj.delete()  # 删除文件夹及其所有子文件夹与文件
            message = "文件夹：{}删除成功".format(path)
        elif type == 'file':
            name = os.path.basename(path)
            dir = os.path.dirname(path)
            file = get_object_or_404(File, name=name, dir__path=dir, owner=request.user)
            file.delete()
            message = "文件：{} 删除成功".format(name)
        return render(request, 'pageJump.html', {'message': message})


def prev_folder(request):
    if request.method == 'GET':
        back_path = os.path.dirname(request.META.get('HTTP_REFERER'))
        return redirect(back_path)
