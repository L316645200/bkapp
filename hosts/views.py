# -*- coding: utf-8 -*-
import json
# Create your views here.
from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_mako_context, render_json
from hosts import models
from hosts.models import HostManager


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


def search_business(request):
    kwargs = {}
    client = get_client_by_request(request)
    resp = client.cc.search_business(**kwargs)

    data = resp.get('data', {})
    info = data.get('info', [])

    biz_list = [{'bk_biz_name': biz['bk_biz_name'], 'bk_biz_id':biz['bk_biz_id']} for biz in info]
    result = {'result': resp.get('result'), 'data': biz_list, 'code': 0}
    return render_json(result)


def update_host(request):
    ip = request.POST.get('ip', '')
    remark = request.POST.get('remark', '')
    result = HostManager.update_host(ip=ip, remark=remark)
    return render_json(result)


def del_host(request):
    host_id = request.POST.get('host_id', '')
    result = HostManager.del_host(host_id=host_id)
    return render_json(result)
# def get_app(request):
#     """
#     获取所有业务
#     """
#     app_list = []
#     client = get_client_by_request(request)
#     kwargs = {}
#     resp = client.cc.get_app_list(**kwargs)
#
#     if resp.get('result'):
#         data = resp.get('data', {})
#         for _d in data:
#             app_list.append({
#                 'name': _d.get('ApplicationName'),
#                 'id': _d.get('ApplicationID'),
#             })
#
#     result = {'result': resp.get('result'), 'data': app_list}
#     return render_json(result)
#
#
# def get_ip_by_appid(request):
#     app_id = request.GET.get('app_id')
#     client = get_client_by_request(request)
#     kwargs = {'app_id': app_id}
#     resp = client.cc.get_app_host_list(**kwargs)
#
#     ip_list = []
#     if resp.get('result'):
#         data = resp.get('data', [])
#         for _d in data:
#             if _d.get('InnerIP') not in ip_list:
#                 ip_list.append(_d.get('InnerIP'))
#     ip_all = [{'ip': _ip} for _ip in ip_list]
#     result = {'result': resp.get('result'), 'data': ip_all}
#     return render_json(result)
#
#
# def get_task_id_by_appid(request):
#     app_id = request.GET.get('app_id')
#     client = get_client_by_request(request)
#     kwargs = {'app_id': app_id}
#     resp = client.job.get_task(**kwargs)
#
#     task_list = []
#     if resp.get('result'):
#         data = resp.get('data', [])
#         for _d in data:
#             task_list.append({
#                 'task_id': _d.get('id'),
#                 'task_name': _d.get('name'),
#             })
#     result = {'result': resp.get('result'), 'data': task_list}
#     return render_json(result)


def test(request):
    username = request.user.username
    return render_json({'username': username, 'result': 'OK'})
