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
from .apiviews import StudentCreate, StudentLogin, StudentAuthenticationTest

urlpatterns = [
    path("v1/api/student/register", StudentCreate.as_view(), name="student_create"),
    path("v1/api/student/login", StudentLogin.as_view(), name="student_login"),
    path("v1/api/student/test", StudentAuthenticationTest.as_view(), name="student_test"),
]