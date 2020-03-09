# -*- coding: utf-8 -*-
"""
@Author    : Jess
@Email     : 2482003411@qq.com
@License   : Copyright(C), Jess
@Time      : 2020/3/4 14:43
@File      : auth.py
@Version   : 1.0
@Description: 
"""
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication
from schools.models import SchoolToken, School

class SchoolAuthentication(BasicAuthentication):
    def authenticate(self, request):
        key = request.headers.get("Api-Http-Authorization")
        if key is None:
            exceptions.AuthenticationFailed({"code": 1002, "msg": "操作失败",
                                             "data": {"error": "缺少 API-HTTP-AUTHORIZATION 请求头"}})
        token = SchoolToken.objects.filter(key=key).first()
        if token:
            student = School.objects.filter(id=token.school_id).first()
            return (student, token)
        else:
            raise exceptions.AuthenticationFailed({"code": 1002, "msg":"操作失败",
                                                   "data": {"error": "API-HTTP-AUTHORIZATION 请求头无效"}})

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return 'Basic realm=API'