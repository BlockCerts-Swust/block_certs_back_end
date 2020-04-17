# -*- coding: utf-8 -*-
"""
@Author    : Jess
@Email     : 2482003411@qq.com
@License   : Copyright(C), Jess
@Time      : 2020/3/22 20:44
@File      : urls.py
@Version   : 1.0
@Description: 
"""
from django.urls import path
from common.apiviews import FileViewSet, certificate_verify, CertVerifyViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'v1/api/files', FileViewSet, basename='file')

router.register(r'v1/api/certificate/verify_list', CertVerifyViewSet, basename='cert-verify')

urlpatterns = [
    path(r'v1/api/certificate/verify',certificate_verify)
]
urlpatterns = router.urls + urlpatterns