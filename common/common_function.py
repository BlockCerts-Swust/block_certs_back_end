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
import requests as req
from io import BytesIO
from block_certs_back_end.settings import BASE_URL
def get_image_base_64(file_wsid):
    response = req.get(BASE_URL+'/v1/api/files/' + file_wsid + '/download')
    ls_f = base64.b64encode(BytesIO(response.content).read()).decode('utf-8')
    # 打印出这个base64编码
    return ls_f

def get_full_url(path):
    return BASE_URL+ path

def get_file_download_url(file_wsid):
    return BASE_URL+'/v1/api/files/' + file_wsid + '/download'