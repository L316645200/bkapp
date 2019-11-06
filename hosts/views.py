# -*- coding: utf-8 -*-
import datetime
import json
# Create your views here.
import time

from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_mako_context, render_json
from hosts import models
from hosts.models import HostManager


# 主机主页
def home(request):
    hosts = HostManager.search_host()

    data = []
    for host in hosts:
        data.append(dict(
            bk_host_id=host.id,
            bk_host_name=host.bk_host_name,
            bk_host_innerip=host.bk_host_innerip,
            bk_biz_name=host.bk_biz_name,
            bk_os_name=host.bk_os_name,
            bk_inst_name=host.bk_inst_name,
            remark=host.remark,
        ))
    return render_mako_context(request, '/hosts/home.html/', {'hosts': data})


# 查询主机（本地）
def search_host(request):
    ip = request.GET.get('ip', '')
    hosts = HostManager.search_host(ip=ip)

    data = []
    for host in hosts:
        data.append(dict(
            bk_host_id=host.id,
            bk_host_name=host.bk_host_name,
            bk_host_innerip=host.bk_host_innerip,
            bk_biz_name=host.bk_biz_name,
            bk_os_name=host.bk_os_name,
            bk_inst_name=host.bk_inst_name,
            remark=host.remark,
        ))

    result = {'result': True, 'data': data, 'code': 0}
    return render_json(result)


# 添加主机
def add_host(request):
    ip = request.POST.get('ip', '')
    if not ip:
        return render_json({'result': False, 'message': u'主机不存在'})
    condition = [{
        "bk_obj_id": "biz",
        "fields": [],
        "condition": []
    }]
    ipc = {"flag": "bk_host_innerip|bk_host_outerip", "exact": 1, "data": [ip]}
    kwargs = {'ip': ipc, 'condition': condition}
    client = get_client_by_request(request)
    resp = client.cc.search_host(**kwargs)

    host_obj = host_object_output(resp)
    if not host_obj:
        raise Exception('The host does not exist.')
    try:
        models.Host.objects.create(
            bk_host_name=host_obj.get('bk_host_name'),
            bk_host_innerip=host_obj.get('bk_host_innerip'),
            bk_biz_name=host_obj.get('bk_biz_name'),
            bk_os_name=host_obj.get('bk_os_name'),
            bk_inst_name=host_obj.get('bk_inst_name'),
        )
        result = {'result': True, 'message': u'保存成功'}
    except Exception, e:
        result = {'result': False, 'message': u'保存失败, %s' % e}
    return render_json(result)


# 查询主机对象输出字典
def host_object_output(host_list):
    host_obj = {}
    if host_list.get('data'):
        data = host_list.get('data', {})
        info = data.get('info', {})
        _i = info[0]

        host = _i.get('host', {})
        biz = _i.get('biz', {})
        cloud = host.get('bk_cloud_id', {})
        host_obj = {
            'bk_host_name': host.get('bk_host_name'),
            'bk_host_innerip': host.get('bk_host_innerip'),
            'bk_biz_name': biz[0].get('bk_biz_name') if biz else '',
            'bk_os_name': host.get('bk_os_name'),
            'bk_inst_name': cloud[0].get('bk_inst_name') if cloud else '',
        }
    return host_obj


# 通过业务查询主机（蓝鲸API）
def get_host_by_biz(request):
    bk_biz_id = request.GET.get('bk_biz_id', '')
    condition = [{
        "bk_obj_id": "biz",
        "fields": [],
        "condition": [{
            'field': 'bk_biz_id',
            'operator': '$eq',
            'value': int(bk_biz_id) if bk_biz_id else '',
        }]
    }]
    kwargs = {'ip': {}, 'condition': condition}
    client = get_client_by_request(request)
    resp = client.cc.search_host(**kwargs)
    host_list = []
    if resp.get('data'):
        data = resp.get('data', {})
        info = data.get('info', {})
        host_list = [{'bk_host_innerip': _i['host']['bk_host_innerip'], 'bk_host_id': _i['host']['bk_host_id']} for _i in info]

    result = {'result': resp.get('result'), 'data': host_list, 'code': 0}
    return render_json(result)


# 查询业务
def search_business(request):
    kwargs = {}
    client = get_client_by_request(request)
    resp = client.cc.search_business(**kwargs)

    data = resp.get('data', {})
    info = data.get('info', [])

    biz_list = [{'bk_biz_name': biz['bk_biz_name'], 'bk_biz_id':biz['bk_biz_id']} for biz in info]
    result = {'result': resp.get('result'), 'data': biz_list, 'code': 0}
    return render_json(result)


# 更新主机备注
def update_host(request):
    ip = request.POST.get('ip', '')
    remark = request.POST.get('remark', '')
    result = HostManager.update_host(ip=ip, remark=remark)
    return render_json(result)


# 删除主机
def del_host(request):
    host_id = request.POST.get('host_id', '')
    result = HostManager.del_host(host_id=host_id)
    return render_json(result)


# 测试API
def test(request):
    username = request.user.username
    return render_json({'username': username, 'result': 'OK'})


BK_BIZ_ID = 2
DISK_JOB_ID = 2
FREE_JOB_ID = 4
LOAD_JOB_ID = 5


# 执行作业
def execute_job(request, bk_job_id):
    host_ip = request.GET.get('host_ip')
    client = get_client_by_request(request)
    kwargs = {'bk_biz_id': BK_BIZ_ID, 'bk_job_id': bk_job_id}
    resp = client.job.get_job_detail(**kwargs)

    ip_list = resp['data']['steps'][0]['ip_list']
    for _ip in ip_list:
        if _ip['ip'] == host_ip:
            resp['data']['steps'][0]['ip_list'] = [_ip]
            break
    else:
        raise Exception('job ip error')
    steps = resp['data']['steps']
    kwargs.update({'steps': steps})
    resp_execute = client.job.execute_job(**kwargs)
    return resp_execute


# 获取日志
def get_logs(request, task):
    if int(task) == 1:
        job_instance = execute_job(request, DISK_JOB_ID)
    elif int(task) == 3:
        job_instance = execute_job(request, LOAD_JOB_ID)
    else:
        job_instance = execute_job(request, FREE_JOB_ID)
    if job_instance.get('data'):
        job_instance_id = job_instance['data']['job_instance_id']
    else:
        raise Exception('job run error')
    kwargs = {'bk_biz_id': BK_BIZ_ID, 'job_instance_id': job_instance_id}

    client = get_client_by_request(request)
    for i in range(10):
        status = client.job.get_job_instance_status(**kwargs)
        if status['data']['is_finished'] is True:
            resp = client.job.get_job_instance_log(**kwargs)
            break
        else:
            time.sleep(0.1)
    else:
        raise Exception('log error')

    ip_log = resp['data'][0]['step_results'][0]['ip_logs'][0]
    # ip = ip_log['ip']
    logs = ip_log['log_content']

    logs = logs.split('\n')
    logs = [_l.split(' ') for _l in logs]
    logs_data = []
    if int(task) == 3:
        return logs
    for log in logs[1:]:
        _l_new = [_l for _l in log if _l != '']
        if _l_new and len(_l_new) >= 5:
            logs_data.append({
                'Filesystem': _l_new[0],  # total used free shared buff/cache available
                'Size': _l_new[1],
                'Used': _l_new[2],
                'Avail': _l_new[3],
                'Use%': _l_new[4],
                'Mounted': _l_new[5],
            })

    return logs_data


# 查看主机性能页面
def host_performance(request):
    host_ip = request.GET.get('host_ip')
    return render_mako_context(request, '/hosts/host_performance.html', {'host_ip': host_ip})


# 获取磁盘日志
def get_capacity(request):
    capacity_data = get_logs(request, 1)

    return render_json({'items': capacity_data[1:]})


# 获取内存日志
def get_mem(request):
    men_data = get_logs(request, 2)
    return render_json({'code': 0, 'result': True, 'message': 'success',
                        'data': {'title': '',
                                 'series': [{'category': u'剩余内存容量(G)', 'value': float(men_data[1]['Size']) - float(men_data[1]['Used'])},
                                            {'category': u'已用内存容量(G)', 'value': float(men_data[1]['Used'])}]}})


def host_load(request):
    host_ip = request.GET.get('host_ip')
    date_now = request.GET.get('to_time')
    hour_ago = request.GET.get('from_time')

    date_now = datetime.datetime.strptime(date_now.replace("&nbsp;", " ").replace("/", "-") + ':00', '%Y-%m-%d %H:%M:%S') if date_now else datetime.datetime.now()
    hour_ago = datetime.datetime.strptime(hour_ago.replace("&nbsp;", " ").replace("/", "-") + ':00', '%Y-%m-%d %H:%M:%S') if hour_ago else date_now - datetime.timedelta(hours=1)

    loads = HostManager.search_host_load(host_ip, date_now, hour_ago)
    is_true = True
    if len(loads) > 90:
        is_true = False
    if not loads:
        data = []
        categories = []
    else:
        data, categories = zip(*[(_load.load, str(_load.create_at)) for _load in loads])

    result = {"code": 0, "result": is_true, "message": "success", "data": {
        "series": [{
            "color": "#f9ce1d",
            "name": "五分钟平均负载(近一小时)",
            "data": list(data),
        }],
        "categories": list(categories),
    }}
    return render_json(result)



# -*- coding: utf-8 -*-
from django.shortcuts import render
# Create your views here.
from django.shortcuts import render_to_response
from django.http import JsonResponse

from account.decorators import login_exempt
from hosts.models import Host


@login_exempt
def api_disk_usage(request):
    """
    磁盘使用率API接口 api/get_dfusage_bay1
    """
    ip = request.GET.get('ip', '')
    ip = '172.16.150.37'
    if ip:
        hosts = Host.objects.filter(bk_host_innerip=ip)

    else:
        return JsonResponse({
            "result": False,
            "data": [],
            "message": '参数不完整'
        })

    data_list = []
    for _data in hosts:
        disk_usages = _data.DiskUsage.all()
        memory_usages = _data.MemoryUsage.all()
        disk_usage_add_time, disk_usage_value = model_data_format(disk_usages)
        memory_usage_add_time, memory_usage_value = model_data_format(memory_usages)

        data_list.append(
            {
                'ip': _data.bk_host_innerip,
                'system': _data.bk_os_name,
                'disk_usage': {
                    "xAxis": disk_usage_add_time,
                    "series": [
                        {
                            "name": "磁盘使用率",
                            "type": "line",
                            "data": disk_usage_value
                        }
                    ]
                },
                'memory_usage': {
                    "xAxis": memory_usage_add_time,
                    "series": [
                        {
                            "name": "内存使用率",
                            "type": "line",
                            "data": memory_usage_value
                        }
                    ]
                }
            }
        )

    return JsonResponse({
        "result": True,
        "data": data_list,
        "message": 'ok'
    })


def model_data_format(usages):
    usage_add_time = []
    usage_value = []
    for usage in usages:
        usage_add_time.append(usage.add_time.strftime("%Y/%m/%d %H:%M:%S"))
        usage_value.append(usage.value)
    return usage_add_time, usage_value