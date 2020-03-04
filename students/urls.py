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
    path("api/v1/student/register", StudentCreate.as_view(), name="student_create"),
    path("api/v1/student/login", StudentLogin.as_view(), name="student_login"),
    path("api/v1/student/test", StudentAuthenticationTest.as_view(), name="student_test"),
]