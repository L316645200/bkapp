# -*- coding: utf-8 -*-
import time
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task
from blueking.component.shortcuts import get_client_by_user
from common.log import logger
from common.mymako import render_json

from hosts.models import HostManager
from hosts.views import get_logs


# 获取本地所有主机ip
def get_ip():
    hosts = HostManager.search_host()
    hosts_ip = [host.bk_host_innerip for host in hosts]
    return hosts_ip


BK_BIZ_ID = 2
LOAD_JOB_ID = 5

# 定时获取主机负载情况
@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def host_load():
    now = datetime.datetime.now()
    job_list = []
    client = get_client_by_user(user='admin')

    hosts_ip = get_ip()
    for ip in hosts_ip:
        kwargs = {'bk_biz_id': BK_BIZ_ID, 'bk_job_id': LOAD_JOB_ID}
        resp = client.job.get_job_detail(**kwargs)
        ip_list = resp['data']['steps'][0]['ip_list']
        for _ip in ip_list:
            if _ip['ip'] == ip:
                resp['data']['steps'][0]['ip_list'] = [_ip]
                break
        else:
            continue
        steps = resp['data']['steps']
        kwargs.update({'steps': steps})
        job_instance = client.job.execute_job(**kwargs)
        job_list.append({'ip': ip, 'job_id': job_instance['data']['job_instance_id']})

    for job in job_list:
        kws = {'bk_biz_id': BK_BIZ_ID, 'job_instance_id': job['job_id']}
        for i in range(10):
            status = client.job.get_job_instance_status(**kws)
            if status['data']['is_finished'] is True:
                resp = client.job.get_job_instance_log(**kws)
                break
            else:
                time.sleep(0.1)
        else:
            continue

        logs = resp['data'][0]['step_results'][0]['ip_logs'][0]['log_content']
        logs = logs.split('\n')
        logs = [_l.split(' ') for _l in logs]

        HostManager.add_host_load(ip=job['ip'], load=logs[1][1], now=now)
