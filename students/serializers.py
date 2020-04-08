# -*- coding: utf-8 -*-
"""
@Author    : Jess
@Email     : 2482003411@qq.com
@License   : Copyright(C), Jess
@Time      : 2020/2/27 14:20
@File      : serializers.py
@Version   : 1.0
@Description: 
"""
from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongoengine_serializers
from students.models import StudentToken, Student, UnsignCert


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create(self, validated_data):
        student = Student(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email_address=validated_data['email_address'],
            student_num=validated_data['student_num'],
            chain_address=validated_data['chain_address'],
            password=validated_data['password']
        )
        # setting the raw password as the hash
        student.set_password(validated_data['password'])
        student.save()
        # ensure that tokens are created when user is created in UserCreate view
        StudentToken.objects.create(student=student)
        return student


class UnsignCertSerializer(mongoengine_serializers.DynamicDocumentSerializer):

    class Meta:
        model = UnsignCert
        fields = "__all__"