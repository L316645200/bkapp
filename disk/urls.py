# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'disk.views',
    # (r'^$', 'home'),

    (r'$', 'get_usage_data'),

)
