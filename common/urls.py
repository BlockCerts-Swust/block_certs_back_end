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
# from common.apiviews import FileUpload
from common.apiviews import FileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'v1/api/file', FileViewSet, basename='file')

# ^ ^v1/api/file/$ [name='file-list']
# ^ ^v1/api/file\.(?P<format>[a-z0-9]+)/?$ [name='file-list']
# ^ ^v1/api/file/(?P<id>[^/.]+)/$ [name='file-detail']
# ^ ^v1/api/file/(?P<id>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='file-detail']
# ^ ^v1/api/file/(?P<id>[^/.]+)/(?P<wsid>[^/.]+)/delete/$ [name='file-delete']
# ^ ^v1/api/file/(?P<id>[^/.]+)/(?P<wsid>[^/.]+)/delete\.(?P<format>[a-z0-9]+)/?$ [name='file-delete']
# ^ ^v1/api/file/(?P<id>[^/.]+)/(?P<wsid>[^/.]+)/download/$ [name='file-download']
# ^ ^v1/api/file/(?P<id>[^/.]+)/(?P<wsid>[^/.]+)/download\.(?P<format>[a-z0-9]+)/?$ [name='file-download']
# ^ ^v1/api/file/(?P<id>[^/.]+)/upload/$ [name='file-upload']
# ^ ^v1/api/file/(?P<id>[^/.]+)/upload\.(?P<format>[a-z0-9]+)/?$ [name='file-upload']

urlpatterns = router.urls