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
from rest_framework.settings import APISettings, DEFAULTS, IMPORT_STRINGS
from rest_framework.views import APIView
from rest_framework.decorators import action
from schools.auth import SchoolAuthentication
from schools.serializers import SchoolSerializer, RevocationSerializer
from schools.models import School, SchoolToken, Revocation
from students.hashers import check_password
from common.common_function import get_image_base_64, get_full_url
import ast


class SchoolCreate(generics.CreateAPIView):
    # Note the authentication_classes = () and permission_classes = () to exempt UserCreate
    # from global authentication scheme.
    permission_classes = (BasePermission, )
    serializer_class = SchoolSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data["id_url"] = "/v1/api/schools/"+data["public_key"] + "/issue/info"
        # "introduction_url": "http://www.swust.edu.cn/intro/",
        if request.data["official_website"].endswith('/'):
            introduction_url = request.data["official_website"] + "intro/"
        else:
            introduction_url = request.data["official_website"] + "/intro/"
        data["introduction_url"] = introduction_url
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
    # authentication_classes = (SchoolAuthentication,)
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
                    "created": instance.register_date
                }
            ],
            "revocationList": get_full_url(instance.revocation_list),
            "image": "data:image/png;base64,"+ls_f,
            "email": instance.email
        })

api_settings = APISettings(None, DEFAULTS, IMPORT_STRINGS)

class RevocationView(APIView):
    permission_classes = (BasePermission, )
    serializer_class = RevocationSerializer
    lookup_field = "public_key"
    queryset = Revocation.objects.all()

    def get_authenticators(self):
        """
        Instantiates and returns the list of authenticators that this view can use.
        """
        if self.request.method == 'PUT':
            authentication_classes = (SchoolAuthentication,)
        elif self.request.method == 'POST':
            authentication_classes = (SchoolAuthentication,)
        elif self.request.method == 'DELETE':
            authentication_classes = (SchoolAuthentication,)
        else:
            authentication_classes = ()

        return [auth() for auth in authentication_classes]


    def post(self, request, public_key):
        data = request.data
        data["public_key"] = public_key
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"code": 1000, "msg": "操作成功", "data": {"revocation": serializer.data}},
                        status=status.HTTP_201_CREATED,
                        headers=headers)


    def put(self, request, public_key):
        uuid = request.data["uuid"]
        obj = Revocation.objects.filter(uuid=uuid).filter(public_key=public_key).first()
        if obj is None:
            return Response({"code": 1001, "msg": "操作失败", "data": {"err": "证书ID不存在"}},
                            status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        data["public_key"] = public_key
        serializer = self.get_serializer(obj, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(obj, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            obj._prefetched_objects_cache = {}

        return Response({"code": 1000, "msg": "操作成功", "data": {"revocation": serializer.data}},
                        status=status.HTTP_200_OK)

    def get(self, request, public_key):
        school = School.objects.filter(public_key=public_key).first()
        if school is None:
            Response({"code": 1001, "msg": "操作失败", "data": {"err": "学校不存在"}})
        revocations = Revocation.objects.filter(public_key=public_key).all()
        revocation_list = []
        for revocation in revocations:
            detail = {
                "id": revocation.uuid,
                "revocationReason": revocation.revocationReason
            }
            revocation_list.append(detail)
        return Response({
            "@context": ast.literal_eval(school.context),
            "id": get_full_url(school.revocation_list),
            "type": "RevocationList",
            "issuer": get_full_url(school.id_url),
            "revokedAssertions": revocation_list
        })

    def delete(self, request, public_key):
        uuid = request.data["uuid"]
        obj = Revocation.objects.filter(uuid=uuid).filter(public_key=public_key).first()
        if obj is None:
            return Response({"code": 1001, "msg": "操作失败", "data": {"err": "证书ID不存在"}},
                            status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(obj)
        return Response({"code": 1000, "msg": "操作成功", "data": {"uuid": uuid}}, status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def perform_update(self, serializer):
        serializer.save()

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.

        You may want to override this if you need to provide different
        serializations depending on the incoming request.

        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def perform_destroy(self, instance):
        instance.delete()