import psutil
from django.http import HttpResponse
from django.shortcuts import render
from prometheus_client import start_http_server, Gauge

net_io_counters = Gauge('net_io_counters', 'Network I/O counters', ['direction'])
cpu_percent = Gauge('cpu_percent', 'CPU percent')
mem_percent = Gauge('mem_percent', 'Memory percent')
disk_percent = Gauge('disk_percent', 'Disk percent')


def index(request):
    return render(request, '../templates/index.html')


def metrics(request):
    net_io_counters.labels(direction='sent').set(psutil.net_io_counters().bytes_sent)
    net_io_counters.labels(direction='recv').set(psutil.net_io_counters().bytes_recv)
    cpu_percent.set(psutil.cpu_percent())
    mem_percent.set(psutil.virtual_memory().percent)
    disk_percent.set(psutil.disk_usage('/').percent)
    return HttpResponse("Metrics updated")


start_http_server(8001)
