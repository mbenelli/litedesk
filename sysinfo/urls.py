from django.conf.urls import patterns, url

from sysinfo import views

urlpatterns = patterns('',
    url(r'^battery', views.battery, name='battery'),
    url(r'^wifi', views.wifi, name='wifi'),
    url(r'^api/battery', views.battery_info, name='battery_info'),
    url(r'^api/wifi', views.wifi_info, name='wifi_info'),
)
