# Generated by Django 3.1.5 on 2021-05-13 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('developer_test', '0002_auto_20210512_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='username',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]