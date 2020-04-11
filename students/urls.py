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
from rest_framework.routers import DefaultRouter

from .apiviews import StudentCreate, StudentLogin, StudentViewSet, CertViewSet, CertDetailViewSet

router = DefaultRouter()

router.register(r'v1/api/students', StudentViewSet, basename='student')
router.register(r'v1/api/certificates', CertViewSet, basename='certificates')
router.register(r'v1/api/certificates', CertDetailViewSet, basename='certificates')

urlpatterns = [
    path("v1/api/students/register", StudentCreate.as_view(), name="student_create"),
    path("v1/api/students/login", StudentLogin.as_view(), name="student_login")
]

urlpatterns = urlpatterns + router.urls