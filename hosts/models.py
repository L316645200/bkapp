# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.


class Host(models.Model):
    bk_host_name = models.CharField(max_length=100)
    bk_host_innerip = models.CharField(max_length=32, null=False, unique=True)
    bk_biz_name = models.CharField(max_length=100)  # 业务名称
    bk_os_name = models.CharField(max_length=100)  # 系统名称
    bk_inst_name = models.CharField(max_length=100)  # 云区域
    remark = models.CharField(max_length=255)

    class Meta:
        db_table = 'host'


class HostManager(models.Manager):
    @staticmethod
    def search_host(ip=None):
        host = Host.objects.all()
        if ip:
            host = host.filter(bk_host_innerip__icontains=ip)
        return host

    @staticmethod
    def update_host(remark):
        pass
