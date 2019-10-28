# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0006_auto_20191028_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostload',
            name='load',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
