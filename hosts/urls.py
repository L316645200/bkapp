# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'hosts.views',
    (r'^$', 'home'),
    # 表单下拉数据获取及渲染
    # 主机增删改查操作
    (r'^api/test/$', 'test'),
    (r'^search_host/$', 'search_host'),
    (r'^add_host/$', 'add_host'),
    (r'^search_business/$', 'search_business'),
    (r'^get_host/$', 'get_host_by_biz'),
    (r'^update_host/$', 'update_host'),
    (r'^del_host/$', 'del_host'),

    # 获取作业详情
    # (r'^get_job/$', 'execute_job'),
    # (r'^get_job_2/$', 'execute_free_job'),
    (r'^get_capacity/$', 'get_capacity'),
    (r'^get_mem/$', 'get_mem'),
    (r'^host_per/$', 'host_performance'),

)
