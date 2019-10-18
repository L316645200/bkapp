# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_mako_context, render_json


def home(request):
    # return render_json({'hello': 'world'})
    return render_mako_context(request, '/hosts/home.html/')


def search_host(request):
    ip = request.GET.get('ip', '')
    kwargs = {'ip': {"flag": "bk_host_innerip|bk_host_outerip", "exact": 0, "data": [ip]}}
    client = get_client_by_request(request)
    resp = client.cc.search_host(**kwargs)
    host_list = []
    if resp.get('data'):
        data = resp.get('data', {})
        info = data.get('info', {})
        for _i in info:
            host = _i.get('host', {})
            biz = _i.get('biz', {})
            cloud = host.get('bk_cloud_id', {})
            host_list.append({
                'name': host.get('bk_host_name'),
                'ip': host.get('bk_host_innerip'),
                'os_name': host.get('bk_os_name'),
                'biz_name': biz[0].get('bk_biz_name') if biz else '',
                'cloud_name': cloud[0].get('bk_inst_name') if cloud else '',
            })

    result = {'result': resp.get('result'), 'data': host_list, 'code': 0}
    return render_json(result)


def add_host(request):
    kwargs = {'ip': {"flag": "bk_host_innerip|bk_host_outerip", "exact": 0, "data": [ip]}}
    client = get_client_by_request(request)
    resp = client.cc.add_host_to_resource(**kwargs)
    return render_mako_context(request, '/hosts/home.html/')


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
