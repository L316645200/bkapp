# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response


def home(request):
    return render_to_response('disk/home.html')


from django.http import JsonResponse

from blueking.component.shortcuts import get_client_by_request


def get_usage_data(request):
    """
    调用自主接入接口api
    """
    if request.method == 'GET':
        client = get_client_by_request(request)
        kwargs = {'ip': request.GET.get('ip', '')}
        usage = client.self_server.get_usage_disk(kwargs)
        return JsonResponse(usage)
