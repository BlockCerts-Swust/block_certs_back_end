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
from .apiviews import SchoolCreate

urlpatterns = [
    path("schools/register", SchoolCreate.as_view(), name="school_create")
]