# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0008_auto_20191028_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiskUsage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(verbose_name=b'\xe7\xa3\x81\xe7\x9b\x98\xe4\xbd\xbf\xe7\x94\xa8\xe7\x8e\x87')),
                ('add_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe5\xbd\x95\xe5\x85\xa5\xe6\x97\xb6\xe9\x97\xb4')),
                ('host', models.ForeignKey(related_name='DiskUsage', to='hosts.Host')),
            ],
        ),
        migrations.CreateModel(
            name='MemoryUsage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(verbose_name=b'\xe5\x86\x85\xe5\xad\x98\xe4\xbd\xbf\xe7\x94\xa8\xe7\x8e\x87')),
                ('add_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe5\xbd\x95\xe5\x85\xa5\xe6\x97\xb6\xe9\x97\xb4')),
                ('host', models.ForeignKey(related_name='MemoryUsage', to='hosts.Host')),
            ],
        ),
    ]
