from django.http import HttpResponse
from django.utils import simplejson

def fake_battery(request):
    return HttpResponse(simplejson.dumps({
        'capacity': 100,
        'level': 54,
        'remaining': 60
    }))

def fake_wifi(request):
    return HttpResponse(simplejson.dumps({
        'networks': ['net0', 'net1', 'net2']
    }))

