from rest_framework import serializers

from .models import UserProfile


class UserSerializer(serializers.Serializer):
    email=serializers.EmailField()
    username=serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model= UserProfile
        fields = ['id', 'user', 'phone', 'birth_date', 'profile_pic']