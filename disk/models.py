# -*- coding: utf-8 -*-

from django.db import models
# Create your models here.
from hosts.models import Host


class DiskUsage(models.Model):
    value = models.IntegerField('磁盘使用率')
    add_time = models.DateTimeField('录入时间', auto_now=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="DiskUsage")


class MemoryUsage(models.Model):
    value = models.IntegerField('内存使用率')
    add_time = models.DateTimeField('录入时间', auto_now=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, related_name="MemoryUsage")

