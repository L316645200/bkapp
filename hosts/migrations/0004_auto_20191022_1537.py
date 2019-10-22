# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0003_auto_20191022_1534'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='biz_name',
            new_name='bk_biz_name',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='host_ip',
            new_name='bk_host_innerip',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='host_name',
            new_name='bk_host_name',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='inst_name',
            new_name='bk_inst_name',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='os_name',
            new_name='bk_os_name',
        ),
    ]
