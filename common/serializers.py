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

from rest_framework_mongoengine import serializers as mongoengine_serializers
from rest_framework import serializers
from common.models import File, Cert


class FileSerializer(mongoengine_serializers.DocumentSerializer):

    class Meta:
        model = File
        fields = '__all__'


class CertSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cert
        fields = '__all__'