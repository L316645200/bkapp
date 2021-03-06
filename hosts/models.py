# -*- coding: utf-8 -*-
from django.db import models


# Create your models here.


class Host(models.Model):
    bk_host_name = models.CharField(max_length=100)
    bk_host_innerip = models.CharField(max_length=32, unique=True)
    bk_biz_name = models.CharField(max_length=100)  # 业务名称
    bk_os_name = models.CharField(max_length=100)  # 系统名称
    bk_inst_name = models.CharField(max_length=100)  # 云区域
    remark = models.CharField(max_length=255)

    class Meta:
        db_table = 'host'


class HostManager(models.Manager):
    @staticmethod
    def search_host(ip=None):
        hosts = Host.objects.all()
        if ip:
            hosts = hosts.filter(bk_host_innerip__icontains=ip)

        return hosts

    @staticmethod
    def update_host(ip, remark):
        host = Host.objects.filter(bk_host_innerip=ip).first()
        try:
            host.remark = remark
            host.save()
            result = {'result': True, 'message': u'更改成功'}
        except Exception, e:
            result = {'result': False, 'message': u'更改失败, %s' % e}
        return result

    @staticmethod
    def del_host(host_id):
        host = Host.objects.get(id=host_id)
        try:
            host.delete()
            result = {'result': True, 'message': u'删除成功'}
        except Exception, e:
            result = {'result': False, 'message': u'删除失败, %s' % e}
        return result

    @staticmethod
    def add_host_load(ip, load, now=None):
        try:
            HostLoad.objects.create(
                host_ip=ip,
                load=load,
                create_at=now,
            )
        except Exception, e:
            pass

    @staticmethod
    def search_host_load(host_ip, date_now, hour_ago):
        loads = HostLoad.objects.filter(host_ip=host_ip, create_at__range=(hour_ago, date_now)).order_by('create_at')
        return loads


class HostLoad(models.Model):
    host_ip = models.CharField(max_length=32)
    load = models.FloatField()
    create_at = models.DateTimeField()

    class Meta:
        db_table = 'host_load'
