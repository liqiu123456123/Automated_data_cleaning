import os

from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import File, Folder, UserModel
from .serializers import FileSerializer, FolderSerializer
from .utils import handle_upload_files


def index(request):
    if request.method == "GET":
        Folder.create_root(request.user)
        return redirect(reverse("netdisk:folder_show", kwargs={"path": "root"}))


def upload(request, path):
    if request.method == "POST":
        files = request.FILES.getlist("files")
        parent = get_object_or_404(Folder, path=path, owner=request.user)
        handle_upload_files(files, parent, request.user)
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

    elif request.method == 'PUT':
        #  利用put请求删除文件
        if "size" in request.data:
            file = File.objects.get(id=request.data["id"])
            if "del_file" in request.data["name"]:
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
        # 删除文件夹
        folder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)