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
from schools.models import School, SchoolToken
from rest_framework import serializers


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create(self, validated_data):
        school = School(
            school_name=validated_data["school_name"],
            address = validated_data["address"],
            official_website = validated_data["official_website"],
            public_key = validated_data["public_key"],
            email_address = validated_data["email_address"],
            password = validated_data["password"]
        )
        # setting the raw password as the hash
        school.set_password(validated_data['password'])
        school.save()
        # ensure that tokens are created when user is created in UserCreate view
        SchoolToken.objects.create(school=school)
        return school
