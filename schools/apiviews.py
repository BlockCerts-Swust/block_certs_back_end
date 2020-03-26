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

from rest_framework import generics, status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
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
        data = request.data
        data["id_url"] = "/v1/api/schools/"+data["public_key"] + "/issue/info"
        # "introduction_url": "http://www.swust.edu.cn/intro/",
        data["introduction_url"] = request.data["official_website"] + "intro/" if request.data["official_website"].endswith('/') else "/intro/"
        data["revocation_list"] = "/v1/api/schools/" + data["public_key"] + "/certificates/revocations"
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
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            if email is None or password is None:
                return Response({
                    "code": 1001, "msg": "操作失败", "data": {"error": "账号或密码不能为空"}
                }, status=status.HTTP_401_UNAUTHORIZED, content_type="application/json")
            school = School.objects.filter(email=email).first()
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
                "context": school.context,
                "type": school.type,
                "name": school.name,
                "email": school.email,
                "official_website": school.official_website,
                "id_url": school.id_url,
                "revocation_list": school.revocation_list,
                "introduction_url": school.introduction_url,
                "public_key": school.public_key,
                "job_title": school.job_title,
                "signature_name": school.signature_name,
                "signature_file_wsid": school.signature_file_wsid,
                "logo_file_wsid": school.logo_file_wsid,
                "register_date": school.register_date
            },
                "token": school.schooltoken.key
            }}, content_type="application/json")
        except Exception as e:
            return Response({"code": 1001, "msg": "操作失败", "data": {
                "error": e
            }}, content_type="application/json")

class SchoolViewSet(viewsets.ModelViewSet):
    authentication_classes = (SchoolAuthentication,)
    permission_classes = (BasePermission, )
    serializer_class = SchoolSerializer
    lookup_field = "public_key"
    queryset = School.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"code": 1000, "msg": "操作成功", "data": {"school":serializer.data}})

    @action(methods=['get'], detail=True, url_path='issue/info', url_name='issue-info')
    def issue_info(self, request, *args, **kwargs):
        from common.common_function import get_image_base_64,get_full_url
        import ast
        instance = self.get_object()
        ls_f = get_image_base_64(instance.logo_file_wsid)
        return Response({
            "@context":ast.literal_eval(instance.context),
            "type": instance.type,
            "id": get_full_url(instance.id_url),
            "name": instance.name,
            "url": instance.official_website,
            "introductionURL": instance.introduction_url,
            "publicKey": [
                {
                    "id":"ecdsa-koblitz-pubkey:"+instance.public_key,
                    "created": ""
                }
            ],
            "revocationList": get_full_url(instance.revocation_list),
            "image": "data:image/png;base64,"+ls_f,
            "email": instance.email
        })