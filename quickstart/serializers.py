from typing import Any, Dict, Optional, Type, TypeVar
from django.contrib.auth.models import Group, User, update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.cache import cache
from django_jwt_.settings import SIMPLE_JWT


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 增加想要加到token中的信息
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        expire_time = int(SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME").total_seconds())
        cache.set(data["access"], str(self.user.email), expire_time)
        update_last_login(None, self.user)
        return data