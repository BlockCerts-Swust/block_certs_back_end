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

from schools.apiviews import SchoolCreate, SchoolLogin, SchoolViewSet
router = DefaultRouter()

router.register(r'v1/api/schools', SchoolViewSet, basename='school')

urlpatterns = [
    path("v1/api/schools/register", SchoolCreate.as_view(), name="school_create"),
    path("v1/api/schools/login", SchoolLogin.as_view(), name="school_login")
]

urlpatterns = urlpatterns + router.urls