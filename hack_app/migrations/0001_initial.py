# Generated by Django 3.0.6 on 2020-06-01 05:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TravelReimbursement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('travel_date', models.DateField(blank=True)),
                ('from_place', models.CharField(max_length=255)),
                ('to_place', models.CharField(max_length=255)),
                ('total_fare', models.PositiveIntegerField()),
                ('upload_bill', models.ImageField(blank=True, upload_to='bill_images')),
                ('time_generated', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sellers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('checkin', models.BooleanField(default=0)),
                ('time_generated', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hackathon_reg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=255, unique=True)),
                ('member1', models.CharField(blank=True, max_length=255)),
                ('member2', models.CharField(blank=True, max_length=255)),
                ('member3', models.CharField(blank=True, max_length=255)),
                ('college', models.CharField(max_length=255)),
                ('project_title', models.CharField(max_length=255)),
                ('project_desciption', models.TextField()),
                ('approve', models.BooleanField(default=False)),
                ('time_generated', models.DateTimeField(auto_now_add=True)),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hack_app.ProjectCategory')),
            ],
        ),
    ]
