# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import simplejson

import cmds

# Web pages

def battery(request):
    template = loader.get_template('sysinfo/sysinfo.html')
    context = RequestContext(request, {
        'id': 'battery',
        'title': 'Battery',
        'refresh_ms': 120000
    })
    return HttpResponse(template.render(context))

def wifi(request):
    template = loader.get_template('sysinfo/sysinfo.html')
    context = RequestContext(request, {
        'id': 'wifi',
        'title': 'Wifi',
        'refresh_ms': 5000
    })
    return HttpResponse(template.render(context))


# Json API

def battery_info(request):
    res = cmds.battery()
    labels = ['Status', 'Level', 'Remaining']
    values = res['data'][0]
    res['data'] = { x: values[i] for i, x in enumerate(labels) }
    return HttpResponse(simplejson.dumps(res),
        content_type='application/json; charset=utf-8')


def wifi_info(request):
    res = cmds.wifi()
    return HttpResponse(simplejson.dumps(res),
        content_type="application/json; charset=utf-8")

