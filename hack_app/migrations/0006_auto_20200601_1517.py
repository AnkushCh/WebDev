# Generated by Django 3.0.6 on 2020-06-01 09:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hack_app', '0005_auto_20200601_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regmodel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
