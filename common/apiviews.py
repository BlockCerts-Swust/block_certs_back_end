# Create your views here.
from rest_framework import status
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework_mongoengine import viewsets as mongoengine_viewsets
from common.models import File, Cert, CertDetail
from common.serializers import FileSerializer
import hashlib
from common.cert_verifier.verifier import verify_certificate_json


class FileViewSet(mongoengine_viewsets.ModelViewSet):
    permission_classes = (BasePermission,)
    queryset = File.objects()
    serializer_class = FileSerializer
    lookup_field = 'wsid'

    # post request, file upload
    def create(self, request, *args, **kwargs):
        # try:
        # , content_type=files.content_type
        files = request.data['file']
        md5_obj = hashlib.md5()
        obj = File()
        obj.file.put(files, content_type=files.content_type)
        for chunk in files.chunks():
            md5_obj.update(chunk)
        hash_code = md5_obj.hexdigest()
        file_wsid = 'file_wsid_' + str(hash_code).lower()
        obj.name = files.name
        obj.wsid = file_wsid
        file_detail_url = "/v1/api/files/" + file_wsid
        file_download_url = "/v1/api/files/" + file_wsid + "/download"
        obj.file_detail_url = file_detail_url
        obj.file_download_url = file_download_url
        obj.save()
        return Response({"code": 1000, "msg": "操作成功", "data":
            {'wsid': file_wsid, 'name': files.name, 'detail_url': file_detail_url, 'download_url': file_download_url}},
                        content_type="application/json",
                        status=status.HTTP_201_CREATED)

    # delete request, /v1/api/file/file_wsid_d4c92a999ba116cb4b2947896dbfe34f/delete
    @action(methods=['DELETE'], detail=True, url_path='delete', url_name='delete')
    def file_delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # get request, /v1/api/file/file_wsid_d4c92a999ba116cb4b2947896dbfe34f/download
    # https://github.com/MongoEngine/django-mongoengine/blob/master/example/tumblelog/tumblelog/views.py
    @action(methods=['get'], detail=True, url_path='download', url_name='download')
    def file_download(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.file.seek(0)
        files = instance.file.read()
        return HttpResponse(
            files,
            content_type=instance.file.content_type,
        )


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def certificate_verify(request):
    cert_id = request.data["cert_id"]
    cert = Cert.objects.filter(cert_id=cert_id).first()
    if cert is None:
        return Response({"code": 1001, "msg": "操作失败", "data": {"err": "证书不存在"}})
    if cert.status == 0:
        return Response({"code": 1001, "msg": "操作失败", "data": {"err": "证书没有发布, 无法验证"}})
    block_cert = CertDetail.objects.filter(wsid = cert_id).first()
    if block_cert is None:
        return Response({"code": 1001, "msg": "操作失败", "data": {"err": "获取证书详细失败"}})
    result = verify_certificate_json(block_cert.block_cert)
    return Response({"code": 1000, "msg": "操作成功", "data":result})