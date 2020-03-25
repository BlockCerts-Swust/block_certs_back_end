# -*- coding: utf-8 -*-
"""
@Author    : Jess
@Email     : 2482003411@qq.com
@License   : Copyright(C), Jess
@Time      : 2020/2/27 14:30
@File      : api apiviews.py
@Version   : 1.0
@Description: 
"""
from rest_framework import generics, status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from students.auth import StudentAuthentication
from students.models import Student, StudentToken
from .serializers import StudentSerializer
from students.hashers import check_password


class StudentCreate(generics.CreateAPIView):
    # Note the authentication_classes = () and permission_classes = () to exempt UserCreate
    # from global authentication scheme.
    permission_classes = (BasePermission,)
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"code": 1000, "msg": "操作成功", "data": {"student": serializer.data}},
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class StudentLogin(APIView):
    permission_classes = (BasePermission,)
    parser_classes = (JSONParser,)

    def post(self, request):
        email_address = request.data.get("email_address")
        password = request.data.get("password")
        try:
            if email_address is None or password is None:
                return Response({
                    "code": 1001, "msg": "操作失败", "data": {"error": "账号或密码不能为空"}
                }, status=status.HTTP_401_UNAUTHORIZED, content_type="application/json")
            student = Student.objects.filter(email_address=email_address).first()
            if not student:
                return Response({
                    "code": 1001, "msg": "操作失败", "data": {"error": "账号或密码错误"}
                }, status=status.HTTP_401_UNAUTHORIZED, content_type="application/json")

            result = check_password(password, student.password)

            if result is not True:
                return Response({
                    "code": 1001, "msg": "操作失败", "data": {"error": "账号或密码错误"}
                }, status=status.HTTP_401_UNAUTHORIZED, content_type="application/json")

            StudentToken.objects.update_or_create(student=student)
            return Response({"code": 1000, "msg": "操作成功", "data": {"student": {
                "email_address": student.email_address,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "student_num": student.student_num,
                "chain_address": student.chain_address,
                "register_date": student.register_date
            },
                "token": student.studenttoken.key
            }}, content_type="application/json")
        except Exception as e:
            return Response({"code": 1001, "msg": "操作失败", "data": {
                "error": e
            }}, content_type="application/json")


class StudentAuthenticationTest(APIView):
    authentication_classes = (StudentAuthentication,)
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

class StudentViewSet(viewsets.ModelViewSet):
    authentication_classes = (StudentAuthentication,)
    permission_classes = (BasePermission, )
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"code": 1000, "msg": "操作成功", "data": {"student":serializer.data}})

