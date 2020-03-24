# Create your views here.
import json

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework_mongoengine import viewsets
from common.models import File
from common.serializers import FileSerializer
import hashlib


class FileViewSet(viewsets.ModelViewSet):
    permission_classes = (BasePermission,)
    queryset = File.objects()
    serializer_class = FileSerializer
    lookup_field = 'wsid'

    # post request, file upload
    def create(self, request, *args, **kwargs):
        # try:
        files = request.FILES['file']
        md5_obj = hashlib.md5()
        obj = File()
        for chunk in files.chunks():
            obj.file.put(chunk)
            md5_obj.update(chunk)
        hash_code = md5_obj.hexdigest()
        file_wsid = 'file_wsid_' + str(hash_code).lower()
        obj.name = files.name
        obj.wsid = file_wsid
        obj.save()
        return Response({"code": 1000, "msg": "操作成功", "data": {'wsid': file_wsid, 'name': files.name}},
                        content_type="application/json",
                        status=status.HTTP_201_CREATED)

    # delete request, /v1/api/file/file_wsid_d4c92a999ba116cb4b2947896dbfe34f/delete
    @action(methods=['DELETE'], detail=True, url_path='delete', url_name='delete')
    def file_delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # get request, /v1/api/file/file_wsid_d4c92a999ba116cb4b2947896dbfe34f/download
    @action(methods=['get'], detail=True, url_path='download', url_name='download')
    def file_download(self, request, *args, **kwargs):
        instance = self.get_object()
        response = FileResponse(instance.file.read())
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{file_name}"'.format(file_name=instance.name)
        return response
