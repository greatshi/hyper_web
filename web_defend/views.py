# coding=utf-8

import time
import json
from django.shortcuts import render, redirect
from django.views.decorators.csrf import (csrf_exempt, csrf_protect)
from django.http import HttpResponse

from util import process


# Create your views here.
@csrf_exempt
def web_api_v1(request):
    method = request.POST.get('method', None)
    status = 0
    data = 'None'
    if (method == 'send_web_tx'):
        status, data = process.send_web_tx(request)
    elif (method == 'get_web_tx'):
        status, data = process.get_web_tx(request)
    elif (method == 'update_trans'):
        status, data = process.update_trans(request)
    elif (method == 'update_record'):
        status, data = process.update_record(request)
    else:
        method = request.GET.get('method', None)
        if (method == 'update_one_record'):
            return process.update_record(request)
        elif(method == 'get_one_tx'):
            return process.get_one_tx(request)
        else:
            status, data = process.server_info(request)
    info = {}
    info['status'] = status
    info['data'] = data
    response = HttpResponse()
    # response['Content-Type'] = "text/javascript"
    response['Access-Control-Allow-Origin'] = '*'
    rjson = json.dumps(info)
    response.write(rjson)
    return response


def index(request):
    return render(request, 'index.html', locals())
