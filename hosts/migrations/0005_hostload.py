# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0004_auto_20191022_1537'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostLoad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host_ip', models.CharField(max_length=32)),
                ('create_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
