# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0002_auto_20191021_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='host_ip',
            field=models.CharField(unique=True, max_length=32),
        ),
    ]
