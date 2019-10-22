# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'hosts.views',
    (r'^$', 'home'),
    # 表单下拉数据获取及渲染
    (r'^api/test/$', 'test'),
    (r'^search_host/$', 'search_host'),
    (r'^add_host/$', 'add_host'),

    (r'^search_business/$', 'search_business'),
    (r'^get_host/$', 'get_host_by_biz'),

)
