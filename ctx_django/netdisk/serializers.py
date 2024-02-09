from rest_framework import serializers

from .models import File, Folder


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ("dir",)


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'
        read_only_fields = ('id', 'create_time')


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file_save', 'upload_time')
