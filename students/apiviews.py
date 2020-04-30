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
from django.db.models import QuerySet
from rest_framework import generics, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from common.common_function import get_full_url
from students.instantiate_v2_certificate_batch import instantiate_batch
from rest_framework_mongoengine.viewsets import GenericViewSet
from schools.models import School

from common import common_function
from common.models import Cert, CertDetail
from common.serializers import CertSerializer, CertDetailSerializer, MyLimitOffset, CertFilter
from students import helpers
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

            StudentToken.objects.get_or_create(student=student)
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


class StudentViewSet(viewsets.ModelViewSet):
    authentication_classes = (StudentAuthentication,)
    permission_classes = (BasePermission,)
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"code": 1000, "msg": "操作成功", "data": {"student": serializer.data}})


class CertDetailViewSet(mixins.RetrieveModelMixin,
                        GenericViewSet):
    authentication_classes = (StudentAuthentication,)
    permission_classes = (BasePermission,)
    serializer_class = CertDetailSerializer
    queryset = CertDetail.objects.all()
    lookup_field = 'wsid'

    @action(methods=['get'], detail=True, url_path='detail', url_name='cert-info')
    def cert_info(self, request, *args, **kwargs):
        instance = self.get_object()
        obj = Cert.objects.filter(cert_id=instance.wsid).first()
        if obj is None:
            return Response({"code": 1001, "msg": "操作失败", "data": {"err": "未查询到证书的创建者"}},
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json")
        if obj.student_pubkey != "ecdsa-koblitz-pubkey:" + self.request.user.chain_address:
            return Response({"code": 1001, "msg": "操作失败", "data": {"err": "没有权限, 您不是该证书的创建者"}},
                            status=status.HTTP_401_UNAUTHORIZED,
                            content_type="application/json")
        serializer = self.get_serializer(instance)
        data = serializer.data
        data["unsign_cert"]["badge"]["image"] = get_full_url(data["unsign_cert"]["badge"]["image"])
        data["unsign_cert"]["badge"]["issuer"]["id"] = get_full_url(data["unsign_cert"]["badge"]["issuer"]["id"])
        data["unsign_cert"]["badge"]["issuer"]["revocationList"] = get_full_url(
            data["unsign_cert"]["badge"]["issuer"]["revocationList"])
        if data["block_cert"]:
            data["block_cert"]["badge"]["image"] = get_full_url(data["unsign_cert"]["badge"]["image"])
            data["block_cert"]["badge"]["issuer"]["id"] = get_full_url(data["unsign_cert"]["badge"]["issuer"]["id"])
            data["block_cert"]["badge"]["issuer"]["revocationList"] = get_full_url(
                data["block_cert"]["badge"]["issuer"]["revocationList"])
        return Response(data)

    def create(self, request, *args, **kwargs):
        pass

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass


class CertViewSet(viewsets.ModelViewSet):
    authentication_classes = (StudentAuthentication,)
    permission_classes = (BasePermission,)
    serializer_class = CertSerializer
    queryset = Cert.objects.all()
    filter_backends = (DjangoFilterBackend,OrderingFilter)
    filter_class = CertFilter
    lookup_field = 'cert_id'

    def create(self, request, *args, **kwargs):
        cert_image_wsid = request.data["cert_image_wsid"]
        cert = Cert.objects.filter(cert_image_wsid=cert_image_wsid,
                                   student_pubkey="ecdsa-koblitz-pubkey:" + self.request.user.chain_address).first()
        if cert:
            return Response({"code": 1001, "msg": "操作失败", "data": {"err": "证书已存在"}},
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json"
                            )
        issuer_name = request.data["issuer_name"]
        result, msg = self.create_conf(issuer_name, request.data)
        if result is False:
            return Response({"code": 1001, "msg": "操作失败", "data": msg},
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json"
                            )
        certs = instantiate_batch(msg)
        response_data = []
        for uid in certs.keys():
            # 存在mongodb里面的数据
            unsign_cert_data = {"unsign_cert": certs[uid]}
            cert_detail = CertDetail(**unsign_cert_data)
            cert_detail.save()
            # 存在mysql里面的证书信息
            cert_data = self.create_cert_data(certs[uid], cert_detail.wsid, cert_image_wsid, issuer_name)
            serializer = self.get_serializer(data=cert_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response_data.append(serializer.data)
        return Response({"code": 1000, "msg": "操作成功", "data": response_data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance is None:
            return Response({"code": 1001, "msg": "操作失败", "data": {"err": "证书不存在"}},
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json"
                            )
        if instance.student_pubkey != "ecdsa-koblitz-pubkey:" + self.request.user.chain_address:
            return Response({"code": 1001, "msg": "操作失败", "data": {"err": "没有权限, 您不是该证书的创建者"}},
                            status=status.HTTP_401_UNAUTHORIZED,
                            content_type="application/json")
        if instance.status == 1:
            return Response({"code": 1001, "msg": "操作失败", "data": {"err": "证书已经发布，无法修改"}},
                            status=status.HTTP_401_UNAUTHORIZED,
                            content_type="application/json")

        issuer_name = request.data["issuer_name"]
        result, msg = self.create_conf(issuer_name, request.data)
        print("template conf", msg)
        if result is False:
            return Response({"code": 1001, "msg": "操作失败", "data": msg},
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json"
                            )
        old_cert = CertDetail.objects.filter(wsid=instance.cert_id).first()
        print("old_cert", old_cert)
        if old_cert is None:
            return Response({"code": 1001, "msg": "操作失败", "data": {"err": "证书不存在"}},
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json"
                            )
        certs = instantiate_batch(msg)
        response_data = []
        print("create certs", certs)
        for uid in certs.keys():
            # unsign_cert = UnsignCert(**certs[uid])
            print("id", instance.cert_id)
            new_unsign_cert_data = {"unsign_cert": certs[uid]}
            old_cert.update(**new_unsign_cert_data)
            cert_data = self.create_cert_data(certs[uid], old_cert.wsid,
                                              request.data["cert_image_wsid"], issuer_name)
            serializer = self.get_serializer(instance, data=cert_data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            response_data.append(serializer.data)
        return Response({"code": 1000, "msg": "操作成功", "data": response_data}, status=status.HTTP_201_CREATED)
        # return Response({"code": 1000, "msg": "操作成功", "data": conf}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page_obj = MyLimitOffset()
        page_certs = page_obj.paginate_queryset(queryset=queryset, request=request, view=self)
        serializer = self.get_serializer(page_certs, many=True)
        return page_obj.get_paginated_response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if "ecdsa-koblitz-pubkey:" + instance.student_pubkey != self.request.user.chain_address:
                Response({"code": 1001, "msg": "操作失败", "data": {"err": "没有权限, 您不是该证书的创建者"}},
                         status=status.HTTP_401_UNAUTHORIZED,
                         content_type="application/json")
            if instance.status == 1:
                return Response({"code": 1001, "msg": "操作失败", "data": {"err": "证书已经发布，无法删除"}},
                                status=status.HTTP_401_UNAUTHORIZED,
                                content_type="application/json")
            old_cert = CertDetail.objects.filter(wsid=instance.cert_id).first()
            old_cert.delete()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response(data={"code": 1001, "msg": "删除失败", "data": {"err": "证书不存在"}},
                            status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if "ecdsa-koblitz-pubkey:" + instance.student_pubkey != self.request.user.chain_address:
            Response({"code": 1001, "msg": "操作失败", "data": {"err": "没有权限, 您不是该证书的创建者"}},
                     status=status.HTTP_401_UNAUTHORIZED,
                     content_type="application/json")
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        """
        Get the list of items for this view.
        This must be an iterable, and may be a queryset.
        Defaults to using `self.queryset`.

        This method should always be used rather than accessing `self.queryset`
        directly, as `self.queryset` gets evaluated only once, and those results
        are cached for all subsequent requests.

        You may want to override this if you need to provide different
        querysets depending on the incoming request.

        (Eg. return a list of items that is specific to the user)
        """
        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            user = self.request.user
            queryset = queryset.filter(student_pubkey="ecdsa-koblitz-pubkey:" + user.chain_address).all()
        return queryset

    def perform_destroy(self, instance):
        instance.delete()

    def create_conf(self, issuer_name, data, badge_id=""):
        issuer = School.objects.filter(name=issuer_name).first()
        print("issuer", issuer)
        if not issuer:
            return False, {"err": "学校不存在"}
        issuer_image = helpers.png_prefix + common_function.get_image_base_64(issuer.logo_file_wsid)
        issuer_id = issuer.id_url
        issuer_url = issuer.official_website
        issuer_email = issuer.email
        issuer_public_key = "ecdsa-koblitz-pubkey:" + issuer.public_key
        issuer_job_title = issuer.job_title
        signature_name = issuer.signature_name
        signature_image_wsid = issuer.signature_file_wsid
        revocation_list = issuer.revocation_list
        issuer_signature_lines = []
        issuer_signature_lines.append(
            {
                "signature_image": helpers.png_prefix + common_function.get_image_base_64(signature_image_wsid),
                "job_title": issuer_job_title,
                "name": signature_name
            })
        recipients = [
            {
                "identity": self.request.user.email_address,
                "name": self.request.user.first_name + " " + self.request.user.last_name,
                "pubkey": self.request.user.chain_address,
                "additional_fields": ""
            }
        ]
        cert_image ='/v1/api/files/' + data["cert_image_wsid"] + '/download'
        conf = {
            "badge_id": badge_id.replace("urn:uuid:", ""),
            "cert_image": cert_image,
            "issuer_logo": issuer_image,
            "certificate_title": data["certificate_title"],
            "certificate_description": data["certificate_description"],
            "issuer_id": issuer_id,
            "issuer_name": issuer_name,
            "issuer_url": issuer_url,
            "issuer_email": issuer_email,
            "issuer_public_key": issuer_public_key,
            "revocation_list": revocation_list,
            "criteria_narrative": data["criteria_narrative"],
            "issuer_signature_lines": issuer_signature_lines,
            "hash_emails": data["hash_emails"],
            "display_html": data["display_html"],
            "additional_global_fields": data["additional_global_fields"],
            "additional_per_recipient_fields": data["additional_per_recipient_fields"],
            "recipients": recipients,
            "filename_format": data["filename_format"]
        }
        return True, conf

    def create_cert_data(self, data, cert_wsid, cert_image_wsid, issuer_name):
        return {
            "cert_image_wsid": cert_image_wsid,
            "certificate_description": data["badge"]["description"],
            "certificate_title": data["badge"]["name"],
            "criteria_narrative": data["badge"]["criteria"]["narrative"],
            "cert_id": cert_wsid,
            "student_name": data["recipientProfile"]["name"],
            "student_pubkey": data["recipientProfile"]["publicKey"],
            "email": data["recipient"]["identity"],
            "school_pubkey": data["verification"]["publicKey"],
            "school_name": issuer_name,
            "status": 0
        }

    def data_check(self):
        pass
