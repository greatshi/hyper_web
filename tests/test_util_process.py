# coding=utf-8

import time
import pathmagic

from util import process
from hyper_web import config_x


ACCESS_TOKEN = '5UBMZBMUOC2TCTRBAPQJFQ'
ABI = '[{"constant":false,"inputs":[],"name":"getInfo","outputs":[{"name":"","type":"string"},{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_name","type":"string"},{"name":"_age","type":"uint256"}],"name":"setInfo","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"name":"name","type":"string"},{"indexed":false,"name":"age","type":"uint256"}],"name":"Instructor","type":"event"}]'
FROM = '0xa37c8deaa18c7798331428dfd33726d2e0419bfa'
TO = '0xea6ba439af852e4d9b9a219eef8e392cac3605eb'

ABI = '[{"constant":false,"inputs":[{"name":"_page_hash","type":"string"},{"name":"_page_name","type":"string"},{"name":"_last_page_hash","type":"string"},{"name":"timestamp","type":"uint256"},{"name":"_page_content","type":"string"}],"name":"sendWebTx","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_page_name","type":"string"}],"name":"getWebTx","outputs":[{"name":"","type":"address"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"uint256"},{"name":"","type":"string"}],"payable":false,"type":"function"}]'
FROM = '0xa37c8deaa18c7798331428dfd33726d2e0419bfa'
TO = '0x4dfac982d1b2414c8fa9ee4240ea3cdb7dd62485'


def test_token_gtoken():
    phone = config_x.phone_num
    password = config_x.password_site
    client_id = '497b31c9-88d6-4937-b26b-114f52a026e1'
    client_secret = '5617d6ji87V3TzkQ4ir6929RK3627b2a'
    rst = process.token_gtoken(phone, password, client_id, client_secret)
    print(rst)


def test_token_rtoken():
    refresh_token = 'K5QY494VXPWNTWGRTCR7JG'
    client_id = '497b31c9-88d6-4937-b26b-114f52a026e1'
    client_secret = '5617d6ji87V3TzkQ4ir6929RK3627b2a'
    rst = process.token_rtoken(refresh_token, client_id, client_secret)
    print(rst)


def test_dev_payload():
    access_token = ACCESS_TOKEN
    abi = ABI
    # args = ["xia0shi", "27"]
    # func_name = "setInfo"
    # args = []
    # func_name = "getInfo"
    # args = ["123413241234abc", "web_01", "123413241234aaa", "{}".format(int(time.time())), "xia0shi~~"]
    # func_name = "sendWebTx"
    args = ["web_01"]
    func_name = "getWebTx"
    rst = process.dev_payload(access_token, abi, args, func_name)
    # print(rst)
    return rst


def test_dev_contract_invokesync():
    access_token = ACCESS_TOKEN
    from_ = FROM
    const = False
    payload = test_dev_payload()
    to = TO
    rst = process.dev_contract_invokesync(access_token, from_, const, payload, to)
    print(rst)
    rst = rst['DecodeRet']
    print(rst)


def test_exec_contract_func():
    access_token = ACCESS_TOKEN
    abi = ABI
    from_ = FROM
    to = TO
    # args = ["123413241234abc", "web_01", "123413241234aaa", "{}".format(int(time.time())), "xia0shi~"]
    # func_name = "sendWebTx"
    args = ["web_01"]
    func_name = "getWebTx"
    rst = process.exec_contract_func(access_token, abi, from_, to, args, func_name)
    print(rst)


def main():
    test_token_gtoken()
    # test_token_rtoken()
    # test_dev_payload()
    # test_dev_contract_invokesync()
    # test_exec_contract_func()
    pass


if __name__ == '__main__':
    main()
