# Generated by Django 3.2.4 on 2024-01-13 09:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('netdisk', '0002_auto_20240113_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='owner',
            field=models.ForeignKey(default='用户none', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
        migrations.AlterField(
            model_name='folder',
            name='owner',
            field=models.ForeignKey(default='用户none', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]
