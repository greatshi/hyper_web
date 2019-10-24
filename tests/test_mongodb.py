# coding=utf-8
import os
import pymongo
import pathmagic

from hyper_web import config_x

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hyper_web.settings")
import django
django.setup()

from web_defend.models import User


def create_db():
    con = pymongo.MongoClient(config_x.MONGODB_HOST, 27017)
    dao_trade = con[config_x.MONGODB_NAME]  # new a database
    dao_trade.add_user(config_x.MONGODB_USER, config_x.MONGODB_PWD)  # add a user


def add_user():
    user = User()
    user.user_name = config_x.user_name
    user.phone_num = config_x.phone_num
    user.phone_zone_code = config_x.phone_zone_code
    user.password = config_x.password

    user.address = config_x.address
    user.password_site = config_x.password_site
    user.client_id = config_x.client_id
    user.client_secret = config_x.client_secret
    user.save()


def main():
    create_db()
    add_user()


if __name__ == '__main__':
    main()
