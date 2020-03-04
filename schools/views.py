# Create your views here.
from django.http import HttpResponse
from rest_framework.views import APIView

class MyAuthenticate(object):

    def is_authenticate(self):
        pass


class Student(APIView):
    authentication_classes = [MyAuthenticate, ]
    def get(self):
        return HttpResponse("get请求")

    def post(self):
        return HttpResponse("post请求")

    def delete(self):
        return HttpResponse("删除请求")