from django.shortcuts import render

# Create your views here.
from common.mymako import render_mako_context, render_json
from iwork.models import WorkRecord


def home(request):
    return render_mako_context(request, '/iwork/home.html')


def save_record(request):
    theme = request.POST.get('theme', '')
    content = request.POST.get('content', '')

    data = dict(
        theme=theme,
        content=content,
        username=request.user.username
    )
    result = WorkRecord.objects.save_record(data)
    return render_json(result)


def records(request):
    records = WorkRecord.objects.all().order_by('-id')
    data = []
    for record in records:
        data.append(dict(
            id=record.id,
            theme=record.theme,
            content=record.content,
            operator=record.operator
        ))
    return render_json({'code': 0, 'message': 'success', 'data': data})
