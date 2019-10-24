#coding=utf-8

import time
import json
import random
import chardet
import hashlib
import requests

from bson.objectid import ObjectId
from django.shortcuts import render, redirect

from hyper_web import config_x
from web_defend.models import (User, WebTxLocal)


ABI = '[{"constant":false,"inputs":[{"name":"_page_name","type":"string"}],"name":"getWebTx","outputs":[{"name":"","type":"address"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_page_hash","type":"string"},{"name":"_page_name","type":"string"},{"name":"_last_page_hash","type":"string"},{"name":"timestamp","type":"uint256"}],"name":"sendWebTx","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"}]'
TO = config_x.TO


def send_web_tx(request):
    web_id = request.POST.get('web_id', None)
    status = 1
    if web_id == '01':
        url = 'http://127.0.0.1:8000/web_server/web_01/'
        page_name = 'web_01'
    elif web_id == '02':
        url = 'http://127.0.0.1:8000/web_server/web_02/'
        page_name = 'web_02'
    elif web_id == '03':
        url = 'http://int.hbu.cn/index.asp'
        page_name = 'index.asp'
    elif web_id == '04':
        url = 'http://int.hbu.cn/content/?138.html'
        page_name = 'download'
    else:
        status = 0
        data = 'None'
        return status, data

    page_content = get_page_content(url)
    page_hash = compute_hash(page_content)
    try:
        last_web_tx_local = WebTxLocal.objects.filter(page_name=page_name).order_by('-timestamp')[0]
        last_page_hash = last_web_tx_local.page_hash
    except:
        last_page_hash = page_hash
    timestamp = int(time.time())

    user_name = 'xia0shi'
    user = User.objects.get(user_name=user_name)
    sender = user.address

    web_tx_local = WebTxLocal()
    web_tx_local.sender = sender
    web_tx_local.page_hash = page_hash
    web_tx_local.page_name = page_name
    web_tx_local.last_page_hash = last_page_hash
    web_tx_local.timestamp = timestamp
    web_tx_local.page_content = page_content
    web_tx_local.save()

    args = ["{}".format(page_hash), "{}".format(page_name), "{}".format(last_page_hash), "{}".format(timestamp)]
    func_name = "sendWebTx"
    rst = exec_contract_func(user_name, args, func_name)
    decode_ret = rst.get('DecodeRet', [])
    data = decode_ret[0]['value']
    print(rst)
    return status, data


def get_web_tx(request):
    web_id = request.POST.get('web_id', None)
    status = 1
    if web_id == '01':
        page_name = 'web_01'
    elif web_id == '02':
        page_name = 'web_02'
    elif web_id == '03':
        page_name = 'index.asp'
    elif web_id == '04':
        page_name = 'download'
    else:
        status = 0
        data = 'None'
        return status, data

    user_name = 'xia0shi'

    args = ["{}".format(page_name)]
    func_name = "getWebTx"
    rst = exec_contract_func(user_name, args, func_name)
    print(rst)
    decode_ret = rst.get('DecodeRet', [])
    print(decode_ret)
    data = str(decode_ret)
    return status, data


def get_page_content(url):
    session = requests.Session()
    session.trust_env = False
    page_content = session.get(url).content
    mychar = chardet.detect(page_content)['encoding']
    page_content = page_content.decode(mychar, 'ignore')
    return page_content


def page_info(page_name, url):
    last_web_tx_local = WebTxLocal.objects.filter(page_name=page_name).order_by('-timestamp')[0]
    last_page_hash = last_web_tx_local.page_hash

    page_content = get_page_content(url)
    page_hash = compute_hash(page_content)

    diff = ''
    if page_hash != last_page_hash:
        last_page_content = last_web_tx_local.page_content
        diff = page_diff(page_content, last_page_content)

    page_balance_r = page_balance(page_name)

    resp = {'page_hash': page_hash, 'page_name': last_web_tx_local.page_name,
            'last_hash': last_web_tx_local.page_hash,
            'timestamp': last_web_tx_local.timestamp,
            'diff': diff, 'page_balance': page_balance_r}
    return resp


def update_trans(request):
    status = 1
    data = ''
    page_dict_list = []
    page_dict = {}
    page_dict['page_name'] = 'web_01'
    page_dict['url'] = 'http://127.0.0.1:8000/web_server/web_01/'
    page_dict_list.append(page_dict)
    page_dict = {}
    page_dict['page_name'] = 'web_02'
    page_dict['url'] = 'http://127.0.0.1:8000/web_server/web_02/'
    page_dict_list.append(page_dict)
    page_dict = {}
    page_dict['page_name'] = 'index.asp'
    page_dict['url'] = 'http://int.hbu.cn/index.asp'
    page_dict_list.append(page_dict)
    page_dict = {}
    page_dict['page_name'] = 'download'
    page_dict['url'] = 'http://int.hbu.cn/content/?138.html'
    page_dict_list.append(page_dict)

    trans_resp = []
    for page_dict in page_dict_list:
        page_name = page_dict['page_name']
        url = page_dict['url']
        try:
            resp = page_info(page_name, url)
            trans_resp.append(resp)
        except Exception as e:
            # raise
            pass
    data = trans_resp
    return status, data


def server_info(request):
    server_info =[
    {
        "name": "File Server",
        "data": [{"x": 1893456000, "y": 77}, {"x": 1893456101, "y": 87},
                 {"x": 1893456202, "y": 97}, {"x": 1893456303, "y": 57},
                 {"x": 1893456404, "y": 67}, {"x": 1893456501, "y": 87},
                 {"x": 1893456602, "y": 77},
                 {"x": 1893456703, "y": random.randint(67, 100)},
                 {"x": 1893456804, "y": 97}, {"x": 1893456901, "y": 57},
                 {"x": 1893457002, "y": random.randint(67, 100)},
                 {"x": 1893457103, "y": 67}, {"x": 1893457204, "y": 87}]
    }, {
        "name": "Mail Server",
        "data": [{"x": 1893456000, "y": 87}, {"x": 1893456101, "y": 87},
                 {"x": 1893456202, "y": 87}, {"x": 1893456303, "y": 57},
                 {"x": 1893456404, "y": random.randint(67, 100)},
                 {"x": 1893456501, "y": random.randint(67, 100)},
                 {"x": 1893456602, "y": 87}, {"x": 1893456703, "y": 67},
                 {"x": 1893456804, "y": random.randint(67, 100)},
                 {"x": 1893456901, "y": 79}, {"x": 1893457002, "y": 87},
                 {"x": 1893457103, "y": random.randint(67, 100)},
                 {"x": 1893457204, "y": random.randint(67, 100)}
                 ]
    }]
    status = 1
    data = server_info
    return status, data


def page_diff(page_content, last_page_content):
    page_one = page_content.split('\n')
    page_another = last_page_content.split('\n')

    diff = ''
    diff += 'now add: \n' + '*'*40 + '\n'
    for i in page_one:
        if i not in page_another:
            diff += i

    diff += '\n'+'*'*40 + '\n\nbefore: \n' + '*'*40 + '\n'
    for i in page_another:
        if i not in page_one:
            diff += i
    return diff


def page_diff_v2(page_content, last_page_content):
    page_one = page_content.split('\n')
    page_another = last_page_content.split('\n')

    after = ''
    for i in page_one:
        if i not in page_another:
            after += i

    before = ''
    for i in page_another:
        if i not in page_one:
            before += i
    return before, after


def page_balance(page_name):
    with open('tests/page_balance.txt', 'r') as f:
        page_balance_dict = eval(f.read())
    page_balance = 0
    for i in page_balance_dict:
        if ((i['page_name'] == page_name) and
           (time.time()- i['timestamp'] < 5)):
            page_balance += 1
    page_balance = page_balance/1.0
    if (page_balance > 100):
        page_balance = random.randint(95, 99)
    elif (page_balance == 0):
        page_balance = random.randint(13, 57)
    else:
        page_balance += random.randint(13, 57)
    return page_balance


def update_record(request):
    status = 1
    data = ''
    page_dict_list = []
    page_dict = {}
    page_dict['page_name'] = 'web_01'
    page_dict['url'] = 'http://127.0.0.1:8000/web_server/web_01/'
    page_dict_list.append(page_dict)
    page_dict = {}
    page_dict['page_name'] = 'web_02'
    page_dict['url'] = 'http://127.0.0.1:8000/web_server/web_02/'
    page_dict_list.append(page_dict)
    page_dict = {}
    page_dict['page_name'] = 'index.asp'
    page_dict['url'] = 'http://int.hbu.cn/index.asp'
    page_dict_list.append(page_dict)
    page_dict = {}
    page_dict['page_name'] = 'download'
    page_dict['url'] = 'http://int.hbu.cn/content/?138.html'
    page_dict_list.append(page_dict)

    page_name = request.POST.get('page_name', 'null')
    if (page_name == 'all'):
        new_tx_dict_list = []
        for page_dict in page_dict_list:
            try:
                page_name = page_dict['page_name']
                last_web_tx_local = WebTxLocal.objects.filter(page_name=page_name).order_by('-timestamp')[0]
                web_tx_local_dict = {}
                web_tx_local_dict['sender'] = 'xia0shi' # last_web_tx_local.sender
                web_tx_local_dict['page_name'] = last_web_tx_local.page_name
                web_tx_local_dict['page_hash'] = last_web_tx_local.page_hash
                web_tx_local_dict['time'] = shift_time(last_web_tx_local.timestamp)
                new_tx_dict_list.append(web_tx_local_dict)
            except Exception as e:
                pass
        data = new_tx_dict_list
    else:
        page_name = request.GET.get('page_name', 'web_01')
        web_tx_local_list = WebTxLocal.objects.filter(page_name=page_name).order_by('-timestamp')
        web_tx_local_dict_list = []
        for web_tx_local in web_tx_local_list:
            web_tx_local_dict = {}
            web_tx_local_dict['tx_id'] = web_tx_local.id
            web_tx_local_dict['sender'] = web_tx_local.sender
            web_tx_local_dict['page_name'] = web_tx_local.page_name
            web_tx_local_dict['page_hash'] = web_tx_local.page_hash
            web_tx_local_dict['time'] = shift_time(web_tx_local.timestamp)
            web_tx_local_dict_list.append(web_tx_local_dict)
        data = web_tx_local_dict_list
        index = '3'
        sender = 'xia0shi'
        timestamp = 'now'
        trans_num = '11'
        trans_list = web_tx_local_dict_list
        content = {'index': index, 'sender': sender,
                   'timestamp': timestamp, 'trans_list': trans_list,
                   'trans_num': trans_num}
        return render(request, 'block.html', content)
    return status, data


def get_one_tx(request):
    tx_id = request.GET.get('tx_id', '')
    tx_id = ObjectId(tx_id)
    web_tx_local = WebTxLocal.objects.get(id=tx_id)
    page_name = web_tx_local.page_name
    sender = web_tx_local.sender
    page_content = web_tx_local.page_content
    timestamp = shift_time(web_tx_local.timestamp)
    last_page_hash = web_tx_local.last_page_hash

    web_tx_local_last = WebTxLocal.objects.filter(page_hash=last_page_hash)[0]
    last_page_content = web_tx_local_last.page_content
    before, after = page_diff_v2(page_content, last_page_content)

    content = {'before': before, 'after': after,
               'page_name': page_name, 'sender': sender,
               'timestamp': timestamp
               }
    return render(request, 'trans.html', content)


def shift_time(timestamp):
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(timestamp)
    return time.strftime(format, value)


def compute_hash(message):
    return hashlib.sha256(message.encode("utf8")).hexdigest()


def json_request(api, access_token, data, headers={}):
    url = "https://api.hyperchain.cn/v1/{}".format(api)
    if (headers == {}):
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        headers['Authorization'] = access_token
    response = requests.post(url, headers=headers, data=data)
    return response.json()


def token_gtoken(phone, password, client_id, client_secret):
    api = 'token/gtoken/'
    headers = {}
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Accept'] = 'text/plain'
    access_token = ''
    data = {}
    data['phone'] = phone
    data['password'] = password
    data['client_id'] = client_id
    data['client_secret'] = client_secret
    return json_request(api, access_token, data, headers)


def token_rtoken(refresh_token, client_id, client_secret):
    api = 'token/rtoken/'
    headers = {}
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers['Accept'] = 'Accept: application/json'
    access_token = ''
    data = {}
    data['refresh_token'] = refresh_token
    data['client_id'] = client_id
    data['client_secret'] = client_secret
    return json_request(api, access_token, data, headers)


def dev_payload(access_token, abi, args, func_name):
    api = 'dev/payload'
    data = {}
    data["Abi"] = abi
    data["Args"] = args
    data["Func"] = func_name
    data = json.dumps(data)
    return json_request(api, access_token, data)


def dev_contract_invokesync(access_token, from_, const, payload, to):
    api = 'dev/contract/invokesync'
    data = {}
    data['From'] = from_
    data['Const'] = const
    data['Payload'] = payload
    data['To'] = to
    data = json.dumps(data)
    return json_request(api, access_token, data)


def exec_contract_func(user_name, args, func_name):
    user = User.objects.get(user_name=user_name)
    access_token = user.access_token
    from_ = user.address
    abi = ABI
    to = TO
    payload = dev_payload(access_token, abi, args, func_name)
    const = False
    rst = dev_contract_invokesync(access_token, from_, const, payload, to)
    status = rst.get('Status', '')
    if (status == 'invalid access token'):
        phone = user.phone_num
        password = user.password_site
        client_id = user.client_id
        client_secret = user.client_secret
        rst = token_gtoken(phone, password, client_id, client_secret)
        print(rst)
        access_token = rst.get('access_token', '')
        expires_in = rst.get('expires_in', 0)
        user.access_token = access_token
        user.expires_in = int(time.time()) + expires_in
        user.save()
        payload = dev_payload(access_token, abi, args, func_name)
        rst = dev_contract_invokesync(access_token, from_, const, payload, to)
    return rst
