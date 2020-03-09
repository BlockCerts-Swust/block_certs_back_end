# -*- coding: utf-8 -*-
"""
@Author    : Jess
@Email     : 2482003411@qq.com
@License   : Copyright(C), Jess
@Time      : 2020/2/27 14:14
@File      : urls.py
@Version   : 1.0
@Description: 
"""

from django.urls import path
from schools.apiviews import SchoolCreate, SchoolLogin, SchoolAuthenticationTest

urlpatterns = [
    path("v1/api/school/register", SchoolCreate.as_view(), name="school_create"),
    path("v1/api/school/login", SchoolLogin.as_view(), name="school_login"),
    path("v1/api/school/test", SchoolAuthenticationTest.as_view(), name="school_test"),
]