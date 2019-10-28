# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0007_hostload_load'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostload',
            name='create_at',
            field=models.DateTimeField(),
        ),
    ]
