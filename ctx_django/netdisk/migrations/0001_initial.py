# Generated by Django 3.2.4 on 2023-12-13 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Digest',
            fields=[
                ('digest', models.CharField(max_length=32, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='文件夹名称')),
                ('path', models.CharField(max_length=2048, verbose_name='文件夹路径')),
                ('creat_time', models.DateField(auto_now_add=True)),
                ('owner', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='netdisk.folder')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='文件名')),
                ('size', models.IntegerField(default=0)),
                ('upload_time', models.DateField(auto_now_add=True)),
                ('digest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='netdisk.digest')),
                ('dir', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='netdisk.folder')),
                ('owner', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
