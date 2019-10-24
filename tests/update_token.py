# coding=utf-8
import os
import time
import pathmagic

from util import process

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hyper_web.settings")
import django
django.setup()

from web_defend.models import User


def update_token():
    users = User.objects.all()
    now_time = time.time()-1000
    for user in users:
        expires_in = user.expires_in
        if (now_time > expires_in):
            phone = user.phone_num
            password = user.password_site
            client_id = user.client_id
            client_secret = user.client_secret
            rst = process.token_gtoken(phone, password, client_id, client_secret)
            print(time.time(), rst)
            access_token = rst.get('access_token', '')
            expires_in = rst.get('expires_in', 0)
            user.access_token = access_token
            user.expires_in = int(time.time()) + expires_in
            user.save()
        time.sleep(3)


def main():
    while True:
        try:
            update_token()
            time.sleep(3)
        except Exception as e:
            print(e)
            time.sleep(3)



if __name__ == '__main__':
    main()
