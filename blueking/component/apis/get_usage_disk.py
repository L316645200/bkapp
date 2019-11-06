# -*- coding: utf-8 -*-
from ..base import ComponentAPI


class CollectionsGetDfusage(object):
    """Collections of get_dfusage_bay1 APIS"""

    def __init__(self, client):
        self.client = client
        # 测试环境
        self.get_usage_disk = ComponentAPI(
            client=self.client, method='GET',
            path='/t/bkapp/api/c/compapi/v2/get_usage_disk/',
            description=u'获取指定磁盤容量'
        )