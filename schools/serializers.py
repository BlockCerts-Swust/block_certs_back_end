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
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        # setting the raw password as the hash
        user.set_password(validated_data['password'])
        user.save()
        # ensure that tokens are created when user is created in UserCreate view
        Token.objects.create(user=user)
        return user
