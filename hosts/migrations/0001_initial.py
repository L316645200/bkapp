# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_name', models.CharField(max_length=100)),
                ('host_ip', models.CharField(max_length=32)),
                ('biz_name', models.CharField(max_length=100)),
                ('os_name', models.CharField(max_length=100)),
                ('inst_name', models.CharField(max_length=100)),
                ('remark', models.CharField(max_length=255)),
            ],
        ),
    ]
