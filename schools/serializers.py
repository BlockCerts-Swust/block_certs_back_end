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
from schools.models import School, SchoolToken, Revocation
from rest_framework import serializers


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create(self, validated_data):
        school = School(
            name=validated_data["name"],
            email=validated_data["email"],
            official_website = validated_data["official_website"],
            id_url = validated_data["id_url"],
            revocation_list = validated_data["revocation_list"],
            introduction_url=validated_data["introduction_url"],
            public_key = validated_data["public_key"],
            job_title= validated_data["job_title"],
            signature_name=validated_data["signature_name"],
            signature_file_wsid=validated_data["signature_file_wsid"],
            logo_file_wsid = validated_data["logo_file_wsid"],
            password = validated_data["password"]
        )
        # setting the raw password as the hash
        school.set_password(validated_data['password'])
        school.save()
        # ensure that tokens are created when user is created in UserCreate view
        SchoolToken.objects.create(school=school)
        return school

class RevocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Revocation
        fields = "__all__"