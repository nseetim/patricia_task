# Generated by Django 3.1.5 on 2021-05-12 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('developer_test', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='api_key',
            field=models.CharField(max_length=400),
        ),
    ]
