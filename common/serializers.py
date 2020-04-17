# -*- coding: utf-8 -*-
"""
@Author    : Jess
@Email     : 2482003411@qq.com
@License   : Copyright(C), Jess
@Time      : 2020/3/23 19:46
@File      : serializers.py.py
@Version   : 1.0
@Description: 
"""
import django_filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_mongoengine import serializers as mongoengine_serializers
from rest_framework import serializers
from common.models import File, Cert, CertDetail


class FileSerializer(mongoengine_serializers.DocumentSerializer):

    class Meta:
        model = File
        fields = '__all__'


class CertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cert
        fields = "__all__"

class CertDetailSerializer(mongoengine_serializers.DynamicDocumentSerializer):

    class Meta:
        model = CertDetail
        fields = "__all__"


class MyLimitOffset(LimitOffsetPagination):
     # 每页默认几条
     default_limit = 10
     # url中指定页码的参数
     page_query_param = "page"
     # url中指定传入条数的参数
     limit_query_param = 'limit'
     # url中指定位置的参数
     offset_query_param = 'offset'
     max_limit = 999

class CertFilter(django_filters.rest_framework.FilterSet):
    school_name = django_filters.CharFilter(lookup_expr="icontains")
    certificate_title = django_filters.CharFilter(lookup_expr="icontains")
    student_name = django_filters.CharFilter(lookup_expr="icontains")
    # 最新价格
    min_time = django_filters.DateTimeFilter(field_name="create_time", lookup_expr='gte')
    # 最大价格
    max_time = django_filters.DateTimeFilter(field_name="create_time", lookup_expr='lte')
    class Meta:
        model = Cert
        fields = ['certificate_title', 'student_name', 'school_name', 'status', 'student_pubkey']

class CertVerifySerializer(serializers.ModelSerializer):

    class Meta:
        model = Cert
        exclude = ['cert_image_wsid', 'id']