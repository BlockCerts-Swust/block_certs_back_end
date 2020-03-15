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

from rest_framework import generics, status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from schools.auth import SchoolAuthentication
from schools.serializers import SchoolSerializer
from schools.models import School, SchoolToken
from students.hashers import check_password


class SchoolCreate(generics.ListCreateAPIView):
    # Note the authentication_classes = () and permission_classes = () to exempt UserCreate
    # from global authentication scheme.
    permission_classes = (BasePermission, )
    serializer_class = SchoolSerializer

    def queryset(self):
        School.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"code": 1000, "msg": "操作成功", "data": {"school": serializer.data}},
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class SchoolLogin(APIView):
    permission_classes = (BasePermission, )
    parser_classes = (JSONParser, )

    def post(self, request):
        email_address = request.data.get("email_address")
        password = request.data.get("password")
        try:
            if email_address is None or password is None:
                return Response({
                    "code": 1001, "msg": "操作失败", "data": {"error": "账号或密码不能为空"}
                }, status=status.HTTP_401_UNAUTHORIZED, content_type="application/json")
            school = School.objects.filter(email_address=email_address).first()
            if not school:
                return Response({
                    "code": 1001, "msg": "操作失败", "data": {"error": "账号或密码错误"}
                }, status=status.HTTP_401_UNAUTHORIZED, content_type="application/json")

            result = check_password(password, school.password)

            if result is not True:
                return Response({
                    "code": 1001, "msg": "操作失败", "data": {"error": "账号或密码错误"}
                }, status=status.HTTP_401_UNAUTHORIZED, content_type="application/json")

            SchoolToken.objects.update_or_create(school=school)
            return Response({"code": 1000, "msg": "操作成功", "data": {"school":{
                "school_name": school.school_name,
                "address": school.address,
                "official_website": school.official_website,
                "email_address": school.email_address,
                "register_date": school.register_date,
            },
                "token": school.schooltoken.key
            }}, content_type="application/json")
        except Exception as e:
            return Response({"code": 1001, "msg": "操作失败", "data": {
                "error": e
            }}, content_type="application/json")



class SchoolAuthenticationTest(APIView):
    authentication_classes = (SchoolAuthentication, )
    permission_classes = (BasePermission,)
    parser_classes = (JSONParser,)

    def get(self, request):
        return Response({
            "code": 1000,
            "msg": "操作成功",
            "data": {
                "message": "Good Work!"
            }
        })