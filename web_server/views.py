import time
from django.shortcuts import render


# Create your views here.
def add_page_balance(page_name):
    try:
        with open('tests/page_balance.txt', 'r') as f:
            page_balance = eval(f.read())
    except:
        page_balance = []
    page_balance.append({'page_name': page_name,
                        'timestamp': int(time.time())})
    with open('tests/page_balance.txt', 'w+') as f:
        f.write(str(page_balance))


def web_01(request):
    page_name = 'web_01'
    add_page_balance(page_name)
    return render(request, '2ndex.html', locals())


def web_02(request):
    page_name = 'web_01'
    add_page_balance(page_name)
    return render(request, 'reg.html', locals())
