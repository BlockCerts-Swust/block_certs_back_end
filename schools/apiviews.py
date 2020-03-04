# -*- coding: utf-8 -*-
"""
@Author    : Jess
@Email     : 2482003411@qq.com
@License   : Copyright(C), Jess
@Time      : 2020/2/27 15:59
@File      : apiviews.py
@Version   : 1.0
@Description: 
"""

from rest_framework import generics
from .serializers import SchoolSerializer


class SchoolCreate(generics.CreateAPIView):
    # Note the authentication_classes = () and permission_classes = () to exempt UserCreate
    # from global authentication scheme.
    authentication_classes = ()
    permission_classes = ()

    serializer_class = SchoolSerializer