# -*- coding: utf-8 -*-
"""
@Author    : Jess
@Email     : 2482003411@qq.com
@License   : Copyright(C), Jess
@Time      : 2020/3/26 13:34
@File      : common_function.py
@Version   : 1.0
@Description: 
"""

import base64
import hashlib
import time

import requests as req
from io import BytesIO
from block_certs_back_end.settings import BASE_URL
from block_certs_back_end.settings import SECRET_KEY

def get_image_base_64(file_wsid):
    try:
        response = req.get('http://web:8000/v1/api/files/' + file_wsid + '/download')
        ls_f = base64.b64encode(BytesIO(response.content).read()).decode('utf-8')
        # 打印出这个base64编码
        return ls_f
    except Exception as e:
        print(e)
        return False

def get_full_url(path):
    if BASE_URL not in path:
        return BASE_URL+ path
    return path

def get_file_download_url(file_wsid):
    try:
        url = BASE_URL+'/v1/api/files/' + file_wsid + '/download'
        response = req.get(url)
        if response.status_code == 200:
            return url
        return False
    except Exception as e:
        print(e)
        return False

def md5(username):
    m = hashlib.md5(bytes(username, encoding='utf-8'))
    m.update(bytes(SECRET_KEY + str(time.time()), encoding='utf-8'))
    return m.hexdigest()
