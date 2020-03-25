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

from schools.apiviews import SchoolCreate, SchoolLogin, SchoolAuthenticationTest, SchoolIssuerJson, SchoolViewSet
router = DefaultRouter()

router.register(r'v1/api/schools', SchoolViewSet, basename='school')

urlpatterns = [
    path("v1/api/schools/register", SchoolCreate.as_view(), name="school_create"),
    path("v1/api/schools/login", SchoolLogin.as_view(), name="school_login"),
    path("v1/api/schools/test", SchoolAuthenticationTest.as_view(), name="school_test"),
    path("v1/api/schools/issuer/testnet", SchoolIssuerJson.as_view(), name="school_issuer_testnet"),
]

urlpatterns = urlpatterns + router.urls